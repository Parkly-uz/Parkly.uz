// =====================================================================
//  CS-1-23 SMART PARKING — MARKAZ (ESP8266 NodeMCU v2)
//  SoftAP + veb-sayt + WebSocket + holat + OLED + chiqish shlagbaumi
// =====================================================================
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Servo.h>
#include "config.h"
#include "web_page.h"

#define TOTAL_SPOTS (SPOT_COUNT * 2)
#define EVENT_COUNT 30
#define EVENT_LEN   40
#define CAR_MAX     12
#define PLATE_LEN   12

static bool irActive(uint8_t pin) {
  return digitalRead(pin) == (IR_ACTIVE_LOW ? LOW : HIGH);
}

// ---------------- Qurilmalar ----------------
enum { N_A, N_B, N_CAM, N_COUNT };
struct Node {
  const char* name;
  uint8_t ip[4];
  uint32_t lastSeen;   // 0 = hali kelmagan
  int rssi;
  uint32_t up;
  uint32_t heap;
  bool online;
};
static Node nodes[N_COUNT] = {
  {"SENSOR A", {IP_SENSOR_A}, 0, 0, 0, 0, false},
  {"SENSOR B", {IP_SENSOR_B}, 0, 0, 0, 0, false},
  {"KIRISH (ESP32-CAM)", {IP_CAM}, 0, 0, 0, 0, false},
};

// ---------------- Joylar ----------------
struct Spot {
  int8_t occ;          // -1 noma'lum (hali hisobot yo'q), 0 bo'sh, 1 band
  bool raw;            // sensorning xom holati
  uint32_t changedAt;  // oxirgi o'zgarish (millis), 0 = yo'q
};
static Spot spots[TOTAL_SPOTS];

// ---------------- Hodisalar jurnali (halqa bufer) ----------------
struct Event { uint32_t t; char msg[EVENT_LEN]; };
static Event events[EVENT_COUNT];
static uint8_t evHead = 0, evCount = 0;

// ---------------- Shlagbaum ----------------
struct Gate {
  Servo servo;
  uint8_t pin;
  bool open = false;
  bool attached = false;
  int angle = SERVO_CLOSED_DEG;
  uint32_t openedAt = 0, lastIr = 0, holdUntil = 0, movedAt = 0;
};
static Gate exitGate;

struct Debounce {
  uint8_t pin;
  bool stable = false, last = false;
  uint32_t since = 0;
  bool update(uint32_t now, uint32_t ms) {
    bool v = irActive(pin);
    if (v != last) { last = v; since = now; }
    else if (v != stable && now - since >= ms) stable = v;
    return stable;
  }
};
static Debounce exitIr;
static bool exitArmed = true;   // IR bo'shamaguncha qayta ochilmaydi

// Kirish shlagbaumi holati (kamera heartbeat'idan)
static bool camIr = false, camGateOpen = false;
static int camServo = SERVO_CLOSED_DEG;

// ---------------- Umumiy ----------------
static Adafruit_SSD1306 oled(128, 64, &Wire, -1);
static bool oledOk = false;
static AsyncWebServer server(80);
static AsyncWebSocket ws("/ws");

static volatile bool reqOpenEntry = false, reqOpenExit = false;
static bool dirty = true;
static uint32_t noSpaceUntil = 0;
static uint32_t lastPush = 0, lastOled = 0, lastCheck = 0, lastCleanup = 0;
static uint8_t lastStations = 0;

// ---------------------------------------------------------------------
static void logEvent(const char* fmt, ...) {
  Event& e = events[evHead];
  va_list ap;
  va_start(ap, fmt);
  vsnprintf(e.msg, EVENT_LEN, fmt, ap);
  va_end(ap);
  e.t = millis();
  evHead = (evHead + 1) % EVENT_COUNT;
  if (evCount < EVENT_COUNT) evCount++;
  Serial.printf_P(PSTR("[CENTER] EVENT: %s\n"), e.msg);
  dirty = true;
}

static void spotName(uint8_t i, char* buf) {
  sprintf_P(buf, PSTR("%c%02u"), i < SPOT_COUNT ? 'A' : 'B', (i % SPOT_COUNT) + 1);
}

// ---------------- Mashinalar tarixi (parkovkadagi mashinalar) ----------------
// Kirishda yaratiladi, chiqib ketgach o'chiriladi. Nomer saytda qo'lda kiritiladi.
struct Car {
  uint16_t id;          // 0 = bo'sh katak
  char plate[PLATE_LEN];
  uint32_t in;          // kirgan vaqt (millis)
  int8_t spot;          // biriktirilgan joy, -1 = hali yo'q
  bool leaving;         // joyidan chiqdi, chiqish shlagbaumini kutyapti
};
static Car cars[CAR_MAX];
static uint16_t nextCarId = 1;
static bool exitAsk = false;    // chiqqan mashinani operator tanlashi kerak

static void carLabel(const Car& c, char* buf, size_t n) {
  if (c.plate[0]) snprintf(buf, n, "%s", c.plate);
  else snprintf_P(buf, n, PSTR("#%u"), c.id);
}

static void addCar() {
  Car* slot = nullptr;
  for (auto& c : cars) if (!c.id) { slot = &c; break; }
  if (!slot) {   // to'lgan bo'lsa eng eskisini almashtiramiz
    slot = &cars[0];
    for (auto& c : cars) if (c.in < slot->in) slot = &c;
  }
  memset(slot, 0, sizeof(Car));
  slot->id = nextCarId++;
  if (!nextCarId) nextCarId = 1;
  slot->in = millis();
  slot->spot = -1;
  logEvent("Mashina #%u kirdi", slot->id);
}

static void removeCar(Car& c) {
  char lb[PLATE_LEN + 2];
  carLabel(c, lb, sizeof(lb));
  logEvent("%s chiqdi (%lu daq)", lb, (unsigned long)((millis() - c.in) / 60000));
  c.id = 0;
  bool any = false;
  for (auto& x : cars) if (x.id) any = true;
  if (!any) exitAsk = false;
}

static void carSpotChanged(uint8_t spot, bool busy) {
  if (busy) {
    for (auto& c : cars) if (c.id && c.spot == (int8_t)spot && c.leaving) { c.leaving = false; return; }
    Car* best = nullptr;   // joy hali biriktirilmagan eng eski mashina
    for (auto& c : cars) if (c.id && c.spot < 0 && (!best || c.in < best->in)) best = &c;
    if (best) best->spot = spot;
  } else {
    for (auto& c : cars) if (c.id && c.spot == (int8_t)spot) c.leaving = true;
  }
}

static void onExitOpened() {
  Car* best = nullptr;
  for (auto& c : cars) if (c.id && c.leaving && (!best || c.in < best->in)) best = &c;
  if (best) { removeCar(*best); return; }
  for (auto& c : cars) if (c.id) { exitAsk = true; return; }
}

// Joyning samarali holati: plata oflayn bo'lsa noma'lum
static int8_t spotState(uint8_t i) {
  const Node& n = nodes[i < SPOT_COUNT ? N_A : N_B];
  return n.online ? spots[i].occ : -1;
}

static void countSpots(uint8_t& freeN, uint8_t& busyN) {
  freeN = busyN = 0;
  for (uint8_t i = 0; i < TOTAL_SPOTS; i++) {
    int8_t s = spotState(i);
    if (s == 0) freeN++;
    else if (s == 1) busyN++;
  }
}

static void touchNode(uint8_t idx, AsyncWebServerRequest* r) {
  Node& n = nodes[idx];
  n.lastSeen = millis();
  if (n.lastSeen == 0) n.lastSeen = 1;
  if (r->hasArg("rssi")) n.rssi = r->arg("rssi").toInt();
  if (r->hasArg("up"))   n.up = r->arg("up").toInt();
  if (r->hasArg("heap")) n.heap = r->arg("heap").toInt();
  if (!n.online) {
    n.online = true;
    logEvent("%s onlayn", n.name);
  }
}

// ---------------- Shlagbaum mantig'i ----------------
static void gateMove(Gate& g, int angle) {
  if (!g.attached) { g.servo.attach(g.pin, SERVO_MIN_US, SERVO_MAX_US); g.attached = true; }
  g.servo.write(angle);
  g.angle = angle;
  g.movedAt = millis();
}

static void gateOpen(Gate& g, uint32_t minHold) {
  uint32_t now = millis();
  g.openedAt = now;
  g.lastIr = now;
  g.holdUntil = now + minHold;
  if (!g.open) {
    g.open = true;
    gateMove(g, SERVO_OPEN_DEG);
    logEvent("Chiqish shlagbaumi ochildi");
    onExitOpened();
  }
}

static void gateUpdate(Gate& g, bool ir) {
  uint32_t now = millis();
  if (g.open) {
    if (ir) g.lastIr = now;
    bool cleared = !ir && now - g.lastIr >= GATE_CLOSE_DELAY_MS && (int32_t)(now - g.holdUntil) >= 0;
    bool timeout = now - g.openedAt >= GATE_MAX_OPEN_MS;
    if (cleared || timeout) {
      g.open = false;
      gateMove(g, SERVO_CLOSED_DEG);
      logEvent(timeout ? "Chiqish yopildi (15s limit)" : "Chiqish shlagbaumi yopildi");
    }
  }
  if (SERVO_DETACH_MS > 0 && g.attached && now - g.movedAt >= SERVO_DETACH_MS) {
    g.servo.detach();
    g.attached = false;
  }
}

// ---------------- JSON holat ----------------
static void buildState(String& out) {
  uint32_t now = millis();
  uint8_t freeN, busyN;
  countSpots(freeN, busyN);

  JsonDocument doc;
  doc["total"] = TOTAL_SPOTS;
  doc["free"] = freeN;
  doc["busy"] = busyN;
  doc["noSpace"] = (int32_t)(noSpaceUntil - now) > 0;

  JsonArray sp = doc["spots"].to<JsonArray>();
  char name[4];
  for (uint8_t i = 0; i < TOTAL_SPOTS; i++) {
    JsonObject o = sp.add<JsonObject>();
    spotName(i, name);
    o["id"] = name;
    o["s"] = spotState(i);
    o["r"] = spots[i].raw ? 1 : 0;
    o["ch"] = spots[i].changedAt ? (long)((now - spots[i].changedAt) / 1000) : -1;
  }

  JsonArray nd = doc["nodes"].to<JsonArray>();
  JsonObject c = nd.add<JsonObject>();
  c["n"] = "MARKAZ";
  c["on"] = true;
  c["ip"] = "192.168.4.1";
  c["rssi"] = nullptr;
  c["up"] = now / 1000;
  c["hb"] = 0;
  c["heap"] = ESP.getFreeHeap();
  for (uint8_t i = 0; i < N_COUNT; i++) {
    const Node& n = nodes[i];
    JsonObject o = nd.add<JsonObject>();
    o["n"] = n.name;
    o["on"] = n.online;
    o["ip"] = IPAddress(n.ip[0], n.ip[1], n.ip[2], n.ip[3]).toString();
    o["rssi"] = n.rssi;
    o["up"] = n.up;
    o["hb"] = n.lastSeen ? (long)((now - n.lastSeen) / 1000) : -1;
    o["heap"] = n.heap;
  }

  JsonObject w = doc["wifi"].to<JsonObject>();
  w["ssid"] = WIFI_SSID;
  w["ch"] = WIFI_CHANNEL;
  w["n"] = WiFi.softAPgetStationNum();

  JsonObject ge = doc["entry"].to<JsonObject>();
  ge["open"] = camGateOpen;
  ge["ang"] = camServo;
  ge["ir"] = camIr;
  ge["on"] = nodes[N_CAM].online;
  JsonObject gx = doc["exit"].to<JsonObject>();
  gx["open"] = exitGate.open;
  gx["ang"] = exitGate.angle;
  gx["ir"] = exitIr.stable;
  gx["on"] = true;

  doc["oled"] = oledOk;
  doc["cam"] = CAM_URL;

  doc["exitAsk"] = exitAsk;
  JsonArray cs = doc["cars"].to<JsonArray>();
  for (const auto& cr : cars) {
    if (!cr.id) continue;
    JsonObject o = cs.add<JsonObject>();
    o["id"] = cr.id;
    o["p"] = cr.plate;
    o["in"] = (now - cr.in) / 1000;
    if (cr.spot >= 0) { spotName(cr.spot, name); o["sp"] = name; } else o["sp"] = "";
    o["lv"] = cr.leaving;
  }

  JsonArray ev = doc["ev"].to<JsonArray>();
  for (uint8_t k = 0; k < evCount; k++) {   // eng yangisi birinchi
    const Event& e = events[(evHead + EVENT_COUNT - 1 - k) % EVENT_COUNT];
    JsonObject o = ev.add<JsonObject>();
    o["t"] = (now - e.t) / 1000;
    o["m"] = e.msg;
  }
  serializeJson(doc, out);
}

// ---------------- HTTP handler'lar (bloklovchi ish YO'Q) ----------------
static void handleReport(AsyncWebServerRequest* r) {
  if (!r->hasArg("node") || !r->hasArg("mask")) { r->send(400, F("text/plain"), F("bad")); return; }
  char node = r->arg("node").charAt(0);
  if (node != 'A' && node != 'B') { r->send(400, F("text/plain"), F("node")); return; }
  String mask = r->arg("mask");
  String raw = r->hasArg("raw") ? r->arg("raw") : mask;
  if (mask.length() != SPOT_COUNT) { r->send(400, F("text/plain"), F("mask")); return; }

  uint8_t nIdx = node == 'A' ? N_A : N_B;
  uint8_t base = node == 'A' ? 0 : SPOT_COUNT;
  touchNode(nIdx, r);
  uint32_t now = millis();
  char name[4];
  for (uint8_t i = 0; i < SPOT_COUNT; i++) {
    Spot& s = spots[base + i];
    int8_t v = mask.charAt(i) == '1' ? 1 : 0;
    bool rv = raw.length() == SPOT_COUNT && raw.charAt(i) == '1';
    if (rv != s.raw) { s.raw = rv; dirty = true; }
    if (v != s.occ) {
      if (s.occ != -1) {
        spotName(base + i, name);
        logEvent(v ? "%s band bo'ldi" : "%s bo'shadi", name);
        carSpotChanged(base + i, v);
      }
      s.occ = v;
      s.changedAt = now;
      dirty = true;
    }
  }
  Serial.printf_P(PSTR("[CENTER] report %c ok mask=%s\n"), node, mask.c_str());
  r->send(200, F("text/plain"), F("ok"));
}

static void handleCam(AsyncWebServerRequest* r) {
  touchNode(N_CAM, r);
  bool ir = r->hasArg("ir") && r->arg("ir") == "1";
  int ang = r->hasArg("servo") ? r->arg("servo").toInt() : SERVO_CLOSED_DEG;
  bool open = r->hasArg("gate") ? r->arg("gate") == "1" : ang != SERVO_CLOSED_DEG;
  if (open != camGateOpen) logEvent(open ? "Kirish shlagbaumi ochildi" : "Kirish shlagbaumi yopildi");
  if (ir != camIr || ang != camServo || open != camGateOpen) dirty = true;
  camIr = ir; camServo = ang; camGateOpen = open;
  r->send(200, F("text/plain"), F("ok"));
}

static void handleEntry(AsyncWebServerRequest* r) {
  touchNode(N_CAM, r);
  uint8_t freeN, busyN;
  countSpots(freeN, busyN);
  bool allow = freeN > 0;
  if (allow) {
    logEvent("Kirish ruxsat (bo'sh: %u)", freeN);
    addCar();
  } else {
    noSpaceUntil = millis() + NOSPACE_SHOW_MS;
    logEvent("Joy yo'q - kirish rad etildi");
  }
  char buf[40];
  snprintf_P(buf, sizeof(buf), PSTR("{\"allow\":%s,\"free\":%u}"), allow ? "true" : "false", freeN);
  r->send(200, F("application/json"), buf);
}

static void handleOpen(AsyncWebServerRequest* r) {
  String g = r->hasArg("gate") ? r->arg("gate") : "";
  if (g == "entry") reqOpenEntry = true;
  else if (g == "exit") reqOpenExit = true;
  else { r->send(400, F("application/json"), F("{\"ok\":false}")); return; }
  r->send(200, F("application/json"), F("{\"ok\":true}"));
}

static Car* findCar(AsyncWebServerRequest* r) {
  uint16_t id = r->hasArg("id") ? r->arg("id").toInt() : 0;
  if (!id) return nullptr;
  for (auto& c : cars) if (c.id == id) return &c;
  return nullptr;
}

// POST /api/plate?id=3&p=01A123BC — faqat A-Z, 0-9 qabul qilinadi
static void handlePlate(AsyncWebServerRequest* r) {
  Car* c = findCar(r);
  if (!c || !r->hasArg("p")) { r->send(404, F("application/json"), F("{\"ok\":false}")); return; }
  String in = r->arg("p");
  uint8_t k = 0;
  for (uint16_t i = 0; i < in.length() && k < PLATE_LEN - 1; i++) {
    char ch = toupper(in.charAt(i));
    if (isalnum(ch)) c->plate[k++] = ch;
  }
  c->plate[k] = 0;
  logEvent("#%u nomeri: %s", c->id, c->plate);
  r->send(200, F("application/json"), F("{\"ok\":true}"));
}

// POST /api/leave?id=3 — mashina chiqdi (id=0: faqat so'rovni bekor qilish)
static void handleLeave(AsyncWebServerRequest* r) {
  exitAsk = false;
  dirty = true;
  Car* c = findCar(r);
  if (c) removeCar(*c);
  r->send(200, F("application/json"), F("{\"ok\":true}"));
}

static void onWsEvent(AsyncWebSocket*, AsyncWebSocketClient* c, AwsEventType type, void*, uint8_t*, size_t) {
  if (type == WS_EVT_CONNECT) {
    Serial.printf_P(PSTR("[CENTER] ws client #%u ulandi\n"), c->id());
    dirty = true;
  }
}

// ---------------- OLED ----------------
static void drawOled() {
  if (!oledOk) return;
  uint32_t now = millis();
  uint8_t freeN, busyN;
  countSpots(freeN, busyN);
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.print(F("CS-1-23 PARKING"));
  oled.drawFastHLine(0, 10, 128, SSD1306_WHITE);

  oled.setTextSize(2);
  oled.setCursor(0, 15);
  bool noSpace = freeN == 0 || (int32_t)(noSpaceUntil - now) > 0;
  if (noSpace) {
    if ((now / 500) % 2 == 0) oled.print(F("JOY YO'Q"));
  } else {
    oled.printf_P(PSTR("BO'SH %u/%u"), freeN, TOTAL_SPOTS);
  }

  // Bo'sh joylar qisqa ro'yxati: A2 A3 B1 ...
  oled.setTextSize(1);
  oled.setCursor(0, 36);
  uint8_t shown = 0;
  for (uint8_t i = 0; i < TOTAL_SPOTS; i++) {
    if (spotState(i) == 0) {
      oled.printf_P(PSTR("%c%u "), i < SPOT_COUNT ? 'A' : 'B', (i % SPOT_COUNT) + 1);
      if (++shown == 7) oled.setCursor(0, 45);
    }
  }
  if (shown == 0) oled.print(F("-"));
  oled.setCursor(0, 56);
  oled.printf_P(PSTR("WiFi: %u qurilma"), WiFi.softAPgetStationNum());
  oled.display();
}

// ---------------- Loop'dagi ishlar ----------------
static void openEntryRemote() {
  WiFiClient client;
  HTTPClient http;
  http.setTimeout(HTTP_TIMEOUT_MS);
  if (!http.begin(client, F(CAM_URL "/open"))) return;
  int code = http.GET();
  http.end();
  if (code == 200) { logEvent("Kirish qo'lda ochildi"); addCar(); }
  else logEvent("Kirish ochilmadi (kamera %d)", code);
}

static void checkNodes(uint32_t now) {
  for (uint8_t i = 0; i < N_COUNT; i++) {
    Node& n = nodes[i];
    bool on = n.lastSeen && now - n.lastSeen < OFFLINE_TIMEOUT_MS;
    if (on != n.online) {
      n.online = on;
      if (!on) logEvent("%s oflayn", n.name);
    }
  }
  uint8_t st = WiFi.softAPgetStationNum();
  if (st != lastStations) { lastStations = st; dirty = true; }
}

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println(F("\n[CENTER] CS-1-23 SMART PARKING - MARKAZ"));

  for (uint8_t i = 0; i < TOTAL_SPOTS; i++) spots[i] = {-1, false, 0};

  pinMode(CENTER_EXIT_IR, INPUT_PULLUP);
  exitIr.pin = CENTER_EXIT_IR;
  exitGate.pin = CENTER_EXIT_SERVO;
  gateMove(exitGate, SERVO_CLOSED_DEG);

  Wire.begin(CENTER_SDA_PIN, CENTER_SCL_PIN);
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  Serial.printf_P(PSTR("[CENTER] OLED %s\n"), oledOk ? "ok" : "XATO (I2C)");

  WiFi.persistent(false);
  WiFi.mode(WIFI_AP);
  IPAddress ip(IP_CENTER), mask(IP_SUBNET);
  WiFi.softAPConfig(ip, ip, mask);
  bool ap = WiFi.softAP(WIFI_SSID, WIFI_PASS, WIFI_CHANNEL, false, WIFI_MAX_CONN);
  Serial.printf_P(PSTR("[CENTER] SoftAP %s: %s ch%d ip=%s\n"), ap ? "ok" : "XATO",
                  WIFI_SSID, WIFI_CHANNEL, WiFi.softAPIP().toString().c_str());

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);
  server.on("/", HTTP_GET, [](AsyncWebServerRequest* r) {
    r->send_P(200, "text/html", INDEX_HTML);
  });
  server.on("/api/report", HTTP_GET, handleReport);
  server.on("/api/cam", HTTP_GET, handleCam);
  server.on("/api/entry", HTTP_GET, handleEntry);
  server.on("/api/open", HTTP_POST, handleOpen);
  server.on("/api/plate", HTTP_POST, handlePlate);
  server.on("/api/leave", HTTP_POST, handleLeave);
  server.on("/api/state", HTTP_GET, [](AsyncWebServerRequest* r) {
    String s;
    buildState(s);
    r->send(200, F("application/json"), s);
  });
  server.onNotFound([](AsyncWebServerRequest* r) { r->send(404, F("text/plain"), F("404")); });
  server.begin();

  logEvent("Markaz ishga tushdi");
}

void loop() {
  uint32_t now = millis();

  // Chiqish: IR mashinani sezsa — shartsiz ochiladi
  bool ir = exitIr.update(now, GATE_IR_DEBOUNCE_MS);
  static bool lastIrState = false;
  if (ir != lastIrState) { lastIrState = ir; dirty = true; }
  if (!ir) exitArmed = true;
  if (ir && exitArmed && !exitGate.open) { exitArmed = false; gateOpen(exitGate, 0); }
  gateUpdate(exitGate, ir);

  // Saytdan qo'lda boshqarish (flag -> loop)
  if (reqOpenExit) { reqOpenExit = false; gateOpen(exitGate, GATE_MANUAL_OPEN_MS); }
  if (reqOpenEntry) { reqOpenEntry = false; openEntryRemote(); }

  if (now - lastCheck >= 200) { lastCheck = now; checkNodes(now); }

  // WebSocket: o'zgarishda darhol (min pauza bilan) va har 1 s
  if ((dirty && now - lastPush >= WS_MIN_GAP_MS) || now - lastPush >= WS_PUSH_MS) {
    lastPush = now;
    dirty = false;
    if (ws.count() > 0 && ws.availableForWriteAll()) {
      String s;
      buildState(s);
      ws.textAll(s);
    }
  }
  if (now - lastCleanup >= 1000) { lastCleanup = now; ws.cleanupClients(); }

  if (now - lastOled >= OLED_REFRESH_MS) { lastOled = now; drawOled(); }
}
