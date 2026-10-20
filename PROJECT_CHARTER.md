# 🚗 Parkly.uz — Project Charter (Loyiha Nizomi)

> **Loyiha nomi:** Parkly.uz — Smart Parking Management System  
> **Loyiha kodi:** PRK-UZ-2026-SINGLE  
> **Sana:** 2026-yil 20-oktabr  
> **Status:** Tasdiqlangan va Amalga oshirilmoqda

---

## 1. 🎯 Loyihaning Maqsadi va Dolzarbligi (Executive Summary)
Yirik obyektlar (savdo markazlari, biznes markazlar va yirik majmualar) uchun avtoturargohlarni tartibga solish, bo'sh joy topishdagi vaqt yo'qotishlarini bartaraf etish, kirish/chiqishdagi 10 daqiqadan ortiq navbatlarni oldini olish hamda to'liq avtomatlashtirilgan, naqd pulsiz (Cashless), operator talab etmaydigan **Parkly.uz** aqlli avtoturargoh ekotizimini yaratish.

---

## 2. 📐 Loyiha Doirasi va Chegaralari (Project Scope & Scale)

### 🟢 Qamrab olingan imkoniyatlar (In-Scope):
1. **Obyekt Turi:** Yirik bitta obyekt uchun mo'ljallangan markazlashgan tizim (Multi-location talab etilmaydi).
2. **Universal Kamera & ANPR:** Istalgan RTSP IP-kamera, USB veb-kamera yoki sinov video faylini `.env` orqali ulash; CLAHE va Bilateral filtrlar orqali qorong'i, tuman va xira ob-havoda raqamlarni aniq o'qish.
3. **Cashless To'lov Tizimi:** O'zbekistonning yetakchi to'lov tizimlari — **Click, Payme va Uzum Pay** integratsiyasi. To'lov oldindan (mobil ilova orqali) yoki chiqish postida avtomatlashtirilgan tarzda amalga oshiriladi.
4. **Xodimlar uchun Imtiyoz (Staff / Personnel):** Ro'yxatdan o'tgan personal uchun to'lov olinmaydi (tekin / oqim ruxsati).
5. **IoT & Hardware (ESP32):** Shlagbaum va datchiklarni boshqarish uchun **ESP32** mikrokontrolleridan foydalanish.
6. **Offline Mode & Sync:** Internet aloqasi uzilib qolganda ham lokal baza orqali uzluksiz ishlash va aloqa tiklanganda ma'lumotlarni serverga avtomatik sinxron qilish.
7. **Strict 10-Min SLA Watchdog:** Postda kutish vaqti 10 daqiqadan oshsa, Fail-Safe rejimida shlagbaumni avtomatik ochish.
8. **Admin Panel & Isometric Map:** Claymorphism dizayniga ega zamonaviy boshqaruv paneli va parkovkaning 3D/Isometric ko'rinishdagi xaritasi.

### 🔴 Qamrab olinmaganlar (Out-of-Scope):
- Ko'p filialli (Multi-location / Chain) tarmoq arxitekturasi (hozircha yirik bitta obyektga qaratilgan).
- Naqd pul qabul qiluvchi fizika apparatlari (Bill acceptor / Coin machine).

---

## 3. 👥 Jamoa Rollari va Mas'uliyat Matritsasi (6 ta Rol)

1. **Product Owner (PO):** Biznes talablari, oferta qoidalari va moliyaviy strategiya.
2. **Project Manager (PM):** Sprintlar, GitHub Kanban doskasi (`Parkly Project`), deadline va resurs taqsimoti.
3. **Lead / AI & CV Architect:** ANPR quvur liniyasi, kamera oqimi, tuman/qorong'i filtrlari va model aniqligi.
4. **Backend & Algorithms Engineer:** PostgreSQL/Redis, FastAPI, Spot Allocator, Tariff Calculator, Gate Controller, Payment gateways va Offline sync.
5. **Frontend & UI/UX Engineer:** Next.js yordamida Claymorphism Admin Paneli va Isometric Parking Map xaritasi.
6. **IoT & Hardware Integration Engineer:** ESP32 mikrokontrolleri va shlagbaum/datchiklar protokollari.

---

## 4. 🛡️ Xatarlar va Ularni Hal Etish Rejasi (Risk Management)

| Xatar (Risk) | Ehtimolligi | Ta'siri | Oldini olish chorasi (Mitigation Strategy) |
| :--- | :--- | :--- | :--- |
| **Internet tarmog'ining uzilishi** | O'rta | Yuqori | **Offline Mode:** Lokal kesh va SQLite orqali ishlash, internet kelganda sinxronlash. |
| **Tuman va qorong'ida raqam o'qilmasligi** | Yuqori | Yuqori | CLAHE, Bilateral smoothing va adaptiv yorug'lik korreksiyasi. |
| **SLA 10 daqiqalik cheklovning buzilishi** | Past | Kritik | Fail-Safe Watchdog orqali 10 daqiqada shlagbaum avtomatik ochiladi. |

---

## 5. 🏆 Muvaffaqiyat Mezonlari (Definition of Success)
- ANPR aniqligi: **≥ 95%**.
- Tizimning javob berish vaqti (Latency): **< 200 ms**.
- Foydalanuvchining maksimal kutish vaqti: **Qat'iy ≤ 10 daqiqa**.
- Internet bo'lmaganda ham uzluksiz ishlash va avtomatik sinxronizatsiya.
