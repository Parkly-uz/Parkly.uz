// =====================================================================
//  CS-1-23 SMART PARKING — MARKAZ (ESP8266) SOZLAMALARI (CONFIG)
// =====================================================================
#pragma once

// ---------------- Joylar soni ----------------
#define SPOT_COUNT          4        // Har bir zonada 4 ta joy (A1-A4, B1-B4 = Jami 8 ta)

// ---------------- Wi-Fi SoftAP Sozlamalari ----------------
#define WIFI_SSID           "Parkly_IoT_Network"
#define WIFI_PASS           "SecureParkingPassword2026"
#define WIFI_CHANNEL        1
#define WIFI_MAX_CONN       8

// ---------------- Statik IP Taqsimoti (192.168.4.x) ----------------
#define IP_CENTER           192, 168, 4, 1     // Markaziy NodeMCU AP IP
#define IP_SUBNET           255, 255, 255, 0
#define IP_CAM              192, 168, 4, 20    // ESP32-CAM IP
#define IP_SENSOR_A         192, 168, 4, 10    // Ultratovush/Infraqizil Sensor A
#define IP_SENSOR_B         192, 168, 4, 11    // Ultratovush/Infraqizil Sensor B

#define CAM_URL             "http://192.168.4.20"

// ---------------- Pinlar taqsimoti (NodeMCU v2) ----------------
#define CENTER_SDA_PIN      4        // D2 (I2C OLED displey uchun)
#define CENTER_SCL_PIN      5        // D1 (I2C OLED displey uchun)
#define CENTER_EXIT_IR      14       // D5 (Chiqish infraqizil datchigi)
#define CENTER_EXIT_SERVO   12       // D6 (Chiqish shlagbaumi servomotori)

#define IR_ACTIVE_LOW       true     // Datchik yopilganda LOW beradi
#define OLED_ADDR           0x3C     // SSD1306 OLED I2C manzili

// ---------------- Vaqt va Kechikishlar (Millisekund) ----------------
#define GATE_IR_DEBOUNCE_MS 150      // Datchik filtrlash
#define GATE_CLOSE_DELAY_MS 2500     // Chiqqandan keyin yopilish kechikishi
#define GATE_MAX_OPEN_MS    15000    // 15 soniya xavfsizlik limiti
#define GATE_MANUAL_OPEN_MS 5000     // Saytdan ochilganda 5s
#define SERVO_DETACH_MS     3000     // Motorni o'chirish (qizib ketmasligi uchun)
#define NOSPACE_SHOW_MS     4000     // "JOY YO'Q" ko'rsatish vaqti
#define OFFLINE_TIMEOUT_MS  10000    // 10 soniya signal kelmasa OFFLINE
#define HTTP_TIMEOUT_MS     3000     // HTTP so'rov taymauti
#define WS_MIN_GAP_MS       100      // WebSocket min pauza
#define WS_PUSH_MS          1000     // WebSocket 1s har sekundda push
#define OLED_REFRESH_MS     300      // OLED yangilanish davri

// ---------------- Servomotor Burchaklari ----------------
#define SERVO_MIN_US        500
#define SERVO_MAX_US        2400
#define SERVO_CLOSED_DEG    0        // Yopiq
#define SERVO_OPEN_DEG      90       // Ochiq
