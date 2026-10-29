// =====================================================================
//  CS-1-23 SMART PARKING — ESP32-CAM KIRISH SOZLAMALARI (CONFIG)
// =====================================================================
#pragma once

#include <esp_camera.h>

// ---------------- Wi-Fi Sozlamalari ----------------
#define WIFI_SSID           "Parkly_IoT_Network"
#define WIFI_PASS           "SecureParkingPassword2026"
#define WIFI_RETRY_MS       5000     // 5 soniyada qayta ulanish

// ---------------- Statik Tarmoq IP Konfiguratsiyasi ----------------
#define IP_CAM              192, 168, 1, 150   // ESP32-CAM kirish IP manzili
#define IP_CENTER           192, 168, 1, 100   // Markaziy Server (FastAPI / Center) IP
#define IP_SUBNET           255, 255, 255, 0

// ---------------- Markaziy Backend URL ----------------
#define CENTER_URL          "http://192.168.1.100:8000"
#define HTTP_TIMEOUT_MS     3000
#define HEARTBEAT_MS        5000     // Har 5 soniyada status yuborish

// ---------------- Pinlar va Datchiklar ----------------
#define CAM_ENTRY_IR        13       // Kirish infraqizil (IR) datchik pini
#define IR_ACTIVE_LOW       true     // Datchik nuri to'silganda LOW beradi
#define CAM_FLASH_LED       4        // Flash LED pini (doim o'chiq saqlanadi)
#define GATE_IR_DEBOUNCE_MS 150      // Datchik titrashini yo'qotish (ms)

// ---------------- Shlagbaum Servomotor Sozlamalari ----------------
#define CAM_ENTRY_SERVO     12       // Shlagbaum servomotor pini
#define SERVO_MIN_US        500      // 0 daraja impuls kengligi
#define SERVO_MAX_US        2400     // 180 daraja impuls kengligi
#define SERVO_CLOSED_DEG    0        // Yopiq holat burchagi
#define SERVO_OPEN_DEG      90       // Ochiq holat burchagi (90 daraja)
#define GATE_CLOSE_DELAY_MS 2500     // Mashina o'tgandan keyin yopilish kechikishi (ms)
#define GATE_MAX_OPEN_MS    15000    // Maksimal ochiq turish vaqti (15s xavfsizlik limiti)
#define GATE_MANUAL_OPEN_MS 5000     // Qo'lda ochilganda kutish vaqti (5s)
#define SERVO_DETACH_MS     3000     // Qizib ketmasligi uchun motorni ajratish (ms)

// ---------------- Kamera Sifati va Kadrlari ----------------
#define CAM_FRAME_SIZE      FRAMESIZE_VGA    // 640x480 (ANPR va Stream uchun optimal)
#define CAM_JPEG_QUALITY    12               // 10-63 (pastroq son = yuqori sifat)
