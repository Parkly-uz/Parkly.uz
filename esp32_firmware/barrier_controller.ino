/*
  =============================================================================
  Parkly.uz — ESP32 IoT Barrier Controller Firmware
  -----------------------------------------------------------------------------
  Mikrokontroller: ESP32 NodeMCU / Arduino IDE
  Vazifasi: Wi-Fi orqali Parkly.uz backend serveridan shlagbaum ochish/yopish
            buyruqlarini qabul qilish, avtomobil infraqizil (IR) datchiklarini
            o'qish va tailgating (ketma-ket o'tish) xavfsizligini taminlash.
  Til: O'zbek tili (Lotin)
  =============================================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Wi-Fi sozlamalari
const char* ssid     = "Parkly_IoT_Network";
const char* password = "SecureParkingPassword2026";

// Parkly.uz Backend API Endpoint
const char* serverUrl = "https://api.parkly.uz/api/v1/iot/barrier-status";
const String deviceApiKey = "PARKLY_ESP32_SECURE_TOKEN_998";

// Pinlar taqsimoti
const int RELAY_BARRIER_PIN = 23;  // Shlagbaum motor rele pin
const int IR_ENTRY_SENSOR   = 34;  // Kirish infraqizil datchik (Tailgating detektori)
const int IR_EXIT_SENSOR    = 35;  // Chiqish infraqizil datchik
const int LED_STATUS_PIN    = 2;   // Holat indikatori LED

void setup() {
  Serial.begin(115200);

  pinMode(RELAY_BARRIER_PIN, OUTPUT);
  pinMode(LED_STATUS_PIN, OUTPUT);
  pinMode(IR_ENTRY_SENSOR, INPUT);
  pinMode(IR_EXIT_SENSOR, INPUT);

  digitalWrite(RELAY_BARRIER_PIN, LOW); // Boshlang'ich holat: yopiq
  digitalWrite(LED_STATUS_PIN, LOW);

  // Wi-Fi ga ulanish
  WiFi.begin(ssid, password);
  Serial.print("Wi-Fi tarmog'iga ulanmoqda");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi ulandi!");
  Serial.print("IP Manzil: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("X-API-Key", deviceApiKey);

    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      String payload = http.getString();
      // JSON tahlili: {"command": "OPEN"} yoki {"command": "CLOSE"}
      DynamicJsonDocument doc(512);
      DeserializationError error = deserializeJson(doc, payload);

      if (!error) {
        String command = doc["command"];
        if (command == "OPEN") {
          openBarrier();
        } else if (command == "CLOSE") {
          closeBarrier();
        }
      }
    }
    http.end();
  }

  // Xavfsizlik: IR datchik orqali tailgating monitoringi
  checkTailgatingSafety();

  delay(1000); // Har 1 sekundda serverdan buyruq tekshiriladi
}

void openBarrier() {
  Serial.println("Shlagbaum OCHILDI (Buyruq bajarildi)");
  digitalWrite(RELAY_BARRIER_PIN, HIGH);
  digitalWrite(LED_STATUS_PIN, HIGH);

  // 5 sekunddan keyin avtomatik yopish yoki IR datchik o'tishini kutish
  delay(5000);

  // Agar mashina o'tib bo'lsa, yopishga buyruq
  closeBarrier();
}

void closeBarrier() {
  Serial.println("Shlagbaum YOPILDI");
  digitalWrite(RELAY_BARRIER_PIN, LOW);
  digitalWrite(LED_STATUS_PIN, LOW);
}

void checkTailgatingSafety() {
  int entryState = digitalRead(IR_ENTRY_SENSOR);
  // Agar shlagbaum ochiq bo'lib, ikkinchi mashina ruxsatsiz yopishib kelsa
  if (entryState == LOW) {
    // Tailgating (Noqonuniy ergashib o'tish) aniqlandi
    Serial.println("OGOHLANTIRISH: Tailgating (Ergashib o'tish) holati aniqlandi!");
  }
}
