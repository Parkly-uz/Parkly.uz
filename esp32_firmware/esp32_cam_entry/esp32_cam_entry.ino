// =====================================================================
//  CS-1-23 SMART PARKING — KIRISH (ESP32-CAM AI-Thinker)
//  Kamera oqimi (port 81) + boshqaruv (port 80) + kirish shlagbaumi
// =====================================================================
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <esp_camera.h>
#include <esp_http_server.h>
#include <ESP32Servo.h>
#include "config.h"

// ---------------- AI-Thinker kamera pinlari ----------------
#define PWDN_GPIO_NUM   32
#define RESET_GPIO_NUM  -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM   26
#define SIOC_GPIO_NUM   27
#define Y9_GPIO_NUM     35
#define Y8_GPIO_NUM     34
#define Y7_GPIO_NUM     39
#define Y6_GPIO_NUM     36
#define Y5_GPIO_NUM     21
#define Y4_GPIO_NUM     19
#define Y3_GPIO_NUM     18
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM  25
#define HREF_GPIO_NUM   23
#define PCLK_GPIO_NUM   22

static bool camOk = false;
static httpd_handle_t ctrlHttpd = nullptr, streamHttpd = nullptr;

// httpd task'lari va loop() o'rtasidagi umumiy holat
static volatile bool reqManualOpen = false;
static volatile bool gateIsOpen = false, irNow = false;
static volatile int servoAngle = SERVO_CLOSED_DEG;

// ---------------- Shlagbaum ----------------
static Servo servo;
static bool servoAttached = false;
static uint32_t openedAt = 0, lastIr = 0, holdUntil = 0, movedAt = 0;
static bool entryArmed = true;
static bool irStable = false, irLast = false;
static uint32_t irSince = 0;
static bool needHeartbeat = true;
static uint32_t lastHb = 0, lastWifiTry = 0;
static bool wasConnected = false;

static bool readIr() {
  return digitalRead(CAM_ENTRY_IR) == (IR_ACTIVE_LOW ? LOW : HIGH);
}

static void servoMove(int angle) {
  if (!servoAttached) { servo.attach(CAM_ENTRY_SERVO, SERVO_MIN_US, SERVO_MAX_US); servoAttached = true; }
  servo.write(angle);
  servoAngle = angle;
  movedAt = millis();
  needHeartbeat = true;
}

static void gateOpen(uint32_t minHold) {
  uint32_t now = millis();
  openedAt = now;
  lastIr = now;
  holdUntil = now + minHold;
  if (!gateIsOpen) {
    gateIsOpen = true;
    servoMove(SERVO_OPEN_DEG);
    Serial.println(F("[CAM] shlagbaum OCHILDI"));
  }
}

static void gateUpdate(bool ir) {
  uint32_t now = millis();
  if (gateIsOpen) {
    if (ir) lastIr = now;
    bool cleared = !ir && now - lastIr >= GATE_CLOSE_DELAY_MS && (int32_t)(now - holdUntil) >= 0;
    bool timeout = now - openedAt >= GATE_MAX_OPEN_MS;
    if (cleared || timeout) {
      gateIsOpen = false;
      servoMove(SERVO_CLOSED_DEG);
      Serial.printf("[CAM] shlagbaum YOPILDI%s\n", timeout ? " (15s limit)" : "");
    }
  }
  if (SERVO_DETACH_MS > 0 && servoAttached && now - movedAt >= SERVO_DETACH_MS) {
    servo.detach();
    servoAttached = false;
  }
}

// ---------------- Kamera ----------------
static bool cameraInit() {
  camera_config_t c = {};
  c.ledc_channel = LEDC_CHANNEL_0;   // kamera XCLK: timer 0 / channel 0
  c.ledc_timer = LEDC_TIMER_0;
  c.pin_d0 = Y2_GPIO_NUM; c.pin_d1 = Y3_GPIO_NUM; c.pin_d2 = Y4_GPIO_NUM; c.pin_d3 = Y5_GPIO_NUM;
  c.pin_d4 = Y6_GPIO_NUM; c.pin_d5 = Y7_GPIO_NUM; c.pin_d6 = Y8_GPIO_NUM; c.pin_d7 = Y9_GPIO_NUM;
  c.pin_xclk = XCLK_GPIO_NUM; c.pin_pclk = PCLK_GPIO_NUM;
  c.pin_vsync = VSYNC_GPIO_NUM; c.pin_href = HREF_GPIO_NUM;
  c.pin_sccb_sda = SIOD_GPIO_NUM; c.pin_sccb_scl = SIOC_GPIO_NUM;
  c.pin_pwdn = PWDN_GPIO_NUM; c.pin_reset = RESET_GPIO_NUM;
  c.xclk_freq_hz = 20000000;
  c.pixel_format = PIXFORMAT_JPEG;
  c.frame_size = CAM_FRAME_SIZE;
  c.jpeg_quality = CAM_JPEG_QUALITY;
  c.grab_mode = CAMERA_GRAB_LATEST;
  if (psramFound()) {
    c.fb_count = 2;
    c.fb_location = CAMERA_FB_IN_PSRAM;
  } else {
    c.fb_count = 1;
    c.fb_location = CAMERA_FB_IN_DRAM;
    c.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  }
  esp_err_t err = esp_camera_init(&c);
  if (err != ESP_OK) {
    Serial.printf("[CAM] kamera XATO 0x%x\n", err);
    return false;
  }
  Serial.printf("[CAM] kamera ok (PSRAM: %s)\n", psramFound() ? "bor" : "yo'q");
  return true;
}

// ---------------- HTTP handler'lar ----------------
#define PART_BOUNDARY "cs123frame"
static const char* STREAM_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char* STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";
static const char* STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

// Bloklovchi: alohida httpd (port 81) task'ida ishlaydi, loop() ga ta'sir qilmaydi
static esp_err_t streamHandler(httpd_req_t* req) {
  if (!camOk) { httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "camera"); return ESP_FAIL; }
  esp_err_t res = httpd_resp_set_type(req, STREAM_TYPE);
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  Serial.println(F("[CAM] stream boshlandi"));
  char part[64];
  while (res == ESP_OK) {
    camera_fb_t* fb = esp_camera_fb_get();
    if (!fb) { res = ESP_FAIL; break; }
    size_t hlen = snprintf(part, sizeof(part), STREAM_PART, fb->len);
    res = httpd_resp_send_chunk(req, STREAM_BOUNDARY, strlen(STREAM_BOUNDARY));
    if (res == ESP_OK) res = httpd_resp_send_chunk(req, part, hlen);
    if (res == ESP_OK) res = httpd_resp_send_chunk(req, (const char*)fb->buf, fb->len);
    esp_camera_fb_return(fb);
  }
  Serial.println(F("[CAM] stream tugadi"));
  return res;
}

static esp_err_t captureHandler(httpd_req_t* req) {
  if (!camOk) { httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "camera"); return ESP_FAIL; }
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) { httpd_resp_send_500(req); return ESP_FAIL; }
  httpd_resp_set_type(req, "image/jpeg");
  httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  esp_err_t res = httpd_resp_send(req, (const char*)fb->buf, fb->len);
  esp_camera_fb_return(fb);
  return res;
}

static esp_err_t openHandler(httpd_req_t* req) {
  reqManualOpen = true;   // servo loop() da harakatlanadi
  httpd_resp_set_type(req, "application/json");
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  return httpd_resp_sendstr(req, "{\"ok\":true}");
}

static esp_err_t statusHandler(httpd_req_t* req) {
  char buf[200];
  snprintf(buf, sizeof(buf),
           "{\"cam\":%s,\"psram\":%s,\"ir\":%d,\"gate\":%d,\"servo\":%d,\"rssi\":%d,\"up\":%lu,\"heap\":%u}",
           camOk ? "true" : "false", psramFound() ? "true" : "false", irNow ? 1 : 0, gateIsOpen ? 1 : 0,
           servoAngle, WiFi.RSSI(), (unsigned long)(millis() / 1000), ESP.getFreeHeap());
  httpd_resp_set_type(req, "application/json");
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  return httpd_resp_sendstr(req, buf);
}

static void startServers() {
  httpd_config_t cfg = HTTPD_DEFAULT_CONFIG();
  cfg.server_port = 80;
  cfg.ctrl_port = 32768;
  cfg.lru_purge_enable = true;
  if (httpd_start(&ctrlHttpd, &cfg) == ESP_OK) {
    httpd_uri_t cap = {"/capture", HTTP_GET, captureHandler, nullptr};
    httpd_uri_t opn = {"/open", HTTP_GET, openHandler, nullptr};
    httpd_uri_t opp = {"/open", HTTP_POST, openHandler, nullptr};
    httpd_uri_t st = {"/status", HTTP_GET, statusHandler, nullptr};
    httpd_register_uri_handler(ctrlHttpd, &cap);
    httpd_register_uri_handler(ctrlHttpd, &opn);
    httpd_register_uri_handler(ctrlHttpd, &opp);
    httpd_register_uri_handler(ctrlHttpd, &st);
    Serial.println(F("[CAM] port 80: /capture /open /status"));
  }
  cfg.server_port = 81;
  cfg.ctrl_port = 32769;
  if (httpd_start(&streamHttpd, &cfg) == ESP_OK) {
    httpd_uri_t str = {"/stream", HTTP_GET, streamHandler, nullptr};
    httpd_register_uri_handler(streamHttpd, &str);
    Serial.println(F("[CAM] port 81: /stream"));
  }
}

// ---------------- Markaz bilan aloqa (faqat loop'dan) ----------------
static int httpGet(const String& url, String* body) {
  HTTPClient http;
  http.setTimeout(HTTP_TIMEOUT_MS);
  http.setConnectTimeout(HTTP_TIMEOUT_MS);
  if (!http.begin(url)) return -1;
  int code = http.GET();
  if (code == 200 && body) *body = http.getString();
  http.end();
  return code;
}

static void sendHeartbeat() {
  char url[160];
  snprintf(url, sizeof(url), CENTER_URL "/api/cam?ir=%d&servo=%d&gate=%d&rssi=%d&up=%lu&heap=%u",
           irStable ? 1 : 0, (int)servoAngle, gateIsOpen ? 1 : 0, WiFi.RSSI(),
           (unsigned long)(millis() / 1000), ESP.getFreeHeap());
  int code = httpGet(url, nullptr);
  if (code != 200) Serial.printf("[CAM] heartbeat XATO (%d)\n", code);
}

// Kirishga ruxsat so'rash. Markazga ulanib bo'lmasa — ochilmaydi (xavfsiz holat)
static void requestEntry() {
  if (WiFi.status() != WL_CONNECTED) { Serial.println(F("[CAM] entry: Wi-Fi yo'q -> OCHILMAYDI")); return; }
  String body;
  int code = httpGet(CENTER_URL "/api/entry", &body);
  if (code != 200) { Serial.printf("[CAM] entry: markaz javob bermadi (%d) -> OCHILMAYDI\n", code); return; }
  bool allow = body.indexOf("\"allow\":true") >= 0;
  Serial.printf("[CAM] entry: %s\n", body.c_str());
  if (allow) gateOpen(0);
  else Serial.println(F("[CAM] JOY YO'Q -> ochilmaydi"));
}

static void wifiBegin() {
  WiFi.config(IPAddress(IP_CAM), IPAddress(IP_CENTER), IPAddress(IP_SUBNET), IPAddress(IP_CENTER));
  WiFi.begin(WIFI_SSID, WIFI_PASS);
}

static void wifiTick(uint32_t now) {
  bool ok = WiFi.status() == WL_CONNECTED;
  if (ok != wasConnected) {
    wasConnected = ok;
    if (ok) {
      Serial.printf("[CAM] Wi-Fi ulandi, IP=%s RSSI=%d\n", WiFi.localIP().toString().c_str(), WiFi.RSSI());
      needHeartbeat = true;
    } else {
      Serial.println(F("[CAM] Wi-Fi uzildi"));
    }
  }
  if (!ok && now - lastWifiTry >= WIFI_RETRY_MS) {
    lastWifiTry = now;
    Serial.println(F("[CAM] Wi-Fi qayta ulanish..."));
    WiFi.disconnect();
    wifiBegin();
  }
}

void setup() {
  pinMode(CAM_FLASH_LED, OUTPUT);
  digitalWrite(CAM_FLASH_LED, LOW);   // flash LED doim o'chiq
  Serial.begin(115200);
  delay(100);
  Serial.println(F("\n[CAM] CS-1-23 SMART PARKING - KIRISH (ESP32-CAM)"));

  pinMode(CAM_ENTRY_IR, INPUT_PULLUP);
  camOk = cameraInit();
  digitalWrite(CAM_FLASH_LED, LOW);

  // Kamera LEDC timer 0 ni ishlatadi — servo uchun 1..3 timerlar ajratiladi
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  servo.setPeriodHertz(50);
  servoMove(SERVO_CLOSED_DEG);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);            // stream barqaror bo'lishi uchun
  WiFi.setAutoReconnect(false);    // qayta ulanishni o'zimiz boshqaramiz (har 5 s)
  wifiBegin();
  lastWifiTry = millis();

  startServers();
}

void loop() {
  uint32_t now = millis();

  bool v = readIr();
  irNow = v;
  if (v != irLast) { irLast = v; irSince = now; }
  else if (v != irStable && now - irSince >= GATE_IR_DEBOUNCE_MS) {
    irStable = v;
    needHeartbeat = true;
    Serial.printf("[CAM] kirish IR -> %s\n", v ? "MASHINA" : "bo'sh");
  }

  if (!irStable) entryArmed = true;
  if (irStable && entryArmed && !gateIsOpen) {
    entryArmed = false;   // mashina ketmaguncha qayta so'ralmaydi
    requestEntry();
  }
  if (reqManualOpen) {
    reqManualOpen = false;
    Serial.println(F("[CAM] qo'lda ochish (5 s)"));
    gateOpen(GATE_MANUAL_OPEN_MS);
  }
  gateUpdate(irStable);

  wifiTick(now);
  if (WiFi.status() == WL_CONNECTED && (needHeartbeat || now - lastHb >= HEARTBEAT_MS)) {
    needHeartbeat = false;
    lastHb = now;
    sendHeartbeat();
  }
}
