# 📋 Parkly.uz — Master Backlog & 100-Task Structure

> **Loyiha:** Parkly.uz — Smart Parking Management System (Single Large Facility)  
> **Metodologiya:** Agile / Scrum (2 haftalik Sprintlar)  
> **To'lov Provayderlari:** Click, Payme, Uzum Pay  
> **Imtiyozlar:** Staff / Personnel (Tekin)  
> **Hardware:** ESP32 Microcontroller  

---

## 📌 EPIC-1: Infratuzilma, IoT va Robust ANPR Qatlami (Sprint 1)
*Maqsad: Ma'lumotlar bazasi, lokal muhit, universal kamera drayveri va tuman/qorong'ida ishlovchi ANPR vizual quvur liniyasini yaratish.*

- [ ] **TASK-101**: Python virtual environment (`venv`) va lokal ma'lumotlar bazasi (SQLite / PostgreSQL) muhitini sozlash (P0 - Must Have)
- [ ] **TASK-102**: Asosiy jadvallar sxemasini yaratish (`schema.sql`: `users`, `vehicles`, `parking_lots`, `parking_spots`, `parking_sessions`, `transactions`, `staff_personnel`) (P0 - Must Have)
- [ ] **TASK-103**: Ma'lumotlar bazasi indekslarini qo'shish (`plate_number`, `slot_number` bo'yicha qidiruvni tezlashtirish) (P1 - Should Have)
- [ ] **TASK-104**: FastAPI asosiy backend loyihasini ochish va `.env` konfiguratsiyasini sozlash (P0 - Must Have)
- [ ] **TASK-105**: Ulanish va bazaning sog'lomligini tekshiruvchi health-check endpoint yozish (P1 - Should Have)
- [ ] **TASK-201**: Multi-threading orqali ishlaydigan va Auto-reconnect xususiyatiga ega universal kamera drayverini yozish (`camera_stream.py`) (P0 - Must Have)
- [ ] **TASK-202**: Kadrlar buferi to'lib qolishining oldini olish uchun zero-latency kadrlar generatorini sozlash (P0 - Must Have)
- [ ] **TASK-203**: `frame_enhancer.py` moduliga CLAHE va Bilateral filtering (tuman/shovqinni tozalash) filtrlarini kuchaytirish (P1 - High)
- [ ] **TASK-204**: Two-Stage Detector (Mashina -> Raqam zonasi) modelini ulash va optimallashtirish (`detector.py`) (P0 - Must Have)
- [ ] **TASK-205**: Trapetsiya buzilishlarini to'g'rilash uchun Perspective Homography korreksiyasini yozish (`perspective.py`) (P1 - High)
- [ ] **TASK-206**: `UzbekistanPlateOCR` modulida harf va raqam chalkashliklarini (O/0, I/1, Z/2) avtomatik to'g'rilovchi mantiqiy filtrlarni kuchaytirish (P0 - Must Have)
- [ ] **TASK-207**: Multi-Frame Temporal Consensus yordamida kadrlararo ovoz berish orqali OCR aniqligini 95%+ ga yetkazish (`temporal_tracker.py`) (P1 - High)
- [ ] **TASK-208**: Mashinaning modeli va rangini (Vehicle Model/Color) aniqlash va seansga bog'lash (P2 - Medium)

---

## 📌 EPIC-2: Smart Parking Algoritmlari, Sessiyalar va To'lov Tizimi (Sprint 2 & 3)
*Maqsad: Spot Allocator, Tariff Calculator (Click, Payme, Uzum Pay & Staff free access), Cashless payment, 10-Min SLA Watchdog va Offline mode.*

- [ ] **TASK-301**: `spot_allocator.py` — Haydovchi uchun eng maqbul va yaqin bo'sh joyni avtomatik biriktirish algoritmini yozish (P0 - Must Have)
- [ ] **TASK-302**: `tariff_calculator.py` — Grace period (15 min bepul), kunduzgi/tungi stavkalar, EV charger va Staff (tekin) tariflarini hisoblash (P0 - Must Have)
- [ ] **TASK-303**: `gate_controller.py` — Kirish shlagbaumini avtomatik ochish yoki band qilish logikasini yozish (P0 - Must Have)
- [ ] **TASK-304**: Click, Payme va Uzum Pay webhook API'larini ulash va avtomatlashtirilgan naqd pulsiz (Cashless) to'lov mantiqini yaratish (P0 - Must Have)
- [ ] **TASK-305**: Qat'iy **10-daqiqalik SLA Watchdog** mexanizmini yozish (5 min warning, 7 min critical, 10 min Fail-Safe emergency open) (P0 - Critical)
- [ ] **TASK-306**: Barcha avtomatlashgan hisob-kitoblar va SLA tekshiruvlarini bajaruvchi fondagi Python demonini (`background_daemon.py`) yaratish (P1 - High)
- [ ] **TASK-307**: ESP32 mikrokontrolleri bilan MQTT/HTTP orqali shlagbaum relay va datchiklar aloqasini o'rnatish (P0 - Must Have)
- [ ] **TASK-308**: Offline Mode (Lokal SQLite/Redis kesh) arxitekturasini yozish va internet tiklanganda avtomatik sinxronizatsiya mexanizmini qo'shish (P1 - High)
- [ ] **TASK-309**: Tailgating (Ortma-ort kirish) va Qora ro'yxat (Blacklist) xavfsizlik filtrlarini yaratish (P1 - High)

---

## 📌 EPIC-3: Claymorphism Admin Panel, Isometric Xarita va API (Sprint 4)
*Maqsad: Zamonaviy Claymorphism dizayniga ega admin paneli, Isometric 3D xarita va Swagger API dokumentatsiyasini tayyorlash.*

- [ ] **TASK-401**: Next.js (React) loyihasini ochish va Claymorphism dizayn tizimini (Soft shadows, smooth rounded layers) sozlash (P1 - High)
- [ ] **TASK-402**: Parkovkaning Isometric (3D ko'rinishdagi) interaktiv xaritasini vizualizatsiya qilish komponentini yaratish (`ParkingMapWidget`) (P1 - High)
- [ ] **TASK-403**: WebSocket orqali slotlar holatini (Bo'sh / Band / Bron / Xatolik) real vaqtda xaritada yangilab turish (P0 - Must Have)
- [ ] **TASK-404**: Admin panelda kunlik tushumlar, tranzaksiyalar va faol seanslar monitoring sahifasini yasash (P1 - High)
- [ ] **TASK-405**: FastAPI avtomatik Swagger/OpenAPI dokumentatsiyasini (`/docs` va `/redoc`) talab qilingan barcha endpointlar uchun sozlash (P1 - High)
- [ ] **TASK-406**: Oferta shartlari va foydalanish qoidalarini (`TERMS.md`) tayyorlash va admin panelda ulash (P2 - Low)
