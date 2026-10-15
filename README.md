<p align="center">
  <h1 align="center">🚗 Parkly.uz — Smart Parking Management System</h1>
  <p align="center">
    <strong>To'liq Avtomatlashgan, Naqd pulsiz (Cashless), Operatorsiz (Unattended) Smart Parkovka Ekotizimi</strong>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/FastAPI-2.0-green.svg" alt="FastAPI" />
  <img src="https://img.shields.io/badge/OpenCV-ANPR%20Weather-purple.svg" alt="OpenCV" />
  <img src="https://img.shields.io/badge/SLA-Max%2010%20Min-red.svg" alt="SLA 10 Min" />
  <img src="https://img.shields.io/badge/Tests-5%2F5%20Passing-brightgreen.svg" alt="Tests Passing" />
</p>

---

## 📌 Loyiha haqida (Overview)
**Parkly.uz** — Shaharlar, yirik savdo markazlari va biznes markazlar uchun inson omilisiz ishlovchi, ekstremal ob-havoda (yomg'ir, qor, tuman) avtomobil modeli va davlat raqamini aniqlovchi, bo'sh joylarni A* algoritmi bilan tavsiya qiluvchi hamda chiqishda haydovchini 10 daqiqadan oshiq ushlamasdan qarzga chiqaruvchi (**Fail-Safe 10-Min SLA**) zamonaviy aqlli platforma.

---

## 🏛️ Tizim Arxitekturasi

```
[ RTSP / ONVIF Kameralar ]       [ Ultratovush / Magnit Datchiklar ]
            │                                      │
            ▼                                      ▼
[ Adversarial Weather CV ]        [ Dual-Layer Slot Manager ]
 (CLAHE, Defogger, YOLOv8)              (A* Routing Engine)
            │                                      │
            └──────────────────┬───────────────────┘
                               ▼
               [ Parkly Core Engine (FastAPI) ]
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 [ 10-Min SLA Watchdog ]             [ Cashless Billing & QR ]
 (05m: Warn, 07m: Urg, 10m: Open)    (Payme, Click, Offline Debt)
```

---

## 💳 Rasmiy Tariflar Tizimi
- 🆓 **Grace Period:** Dastlabki 15 daqiqa — **0 so'm**
- 🚗 **Kunduzgi soatlik (08:00 - 20:00):** **5,000 so'm/soat**
- 🌙 **Tungi soatlik (20:00 - 08:00):** **3,000 so'm/soat**
- 🔥 **Tig'iz vaqt (Peak > 85% to'lalik):** **8,000 so'm/soat**
- 👑 **Kunlik fiksirlangan:** **40,000 so'm/kun**
- 🛡️ **No-Automation Qarz:** Internet uzilganda to'xtovsiz chiqish va ilovada to'lash

---

## 🛡️ Rollar va Ruxsatlar (RBAC)
- **Super-Admin (2 kishi):** `admin` (Erjigit), `superadmin2` (Sherzod) — To'liq nazorat va tariflarni o'zgartirish.
- **Adminlar (4 kishi):** `admin_yunusobod`, `admin_chilonzor`, `admin_mirobod`, `admin_sergeli` — Filial monitoringi va hisobotlar.
- **Smena Nazoratchisi (2 kishi):** `operator1`, `operator2` — Jonli oqim va SLA ogohlantirishlari.

---

## 🚀 O'rnatish va Ishga Tushirish

```bash
# 1. Repozitoriyani klonlash
git clone https://github.com/Parkly-uz/Parkly.uz.git
cd Parkly.uz

# 2. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 3. Testlarni tekshirish
python -m unittest tests/test_core_engine.py

# 4. API Serverni ishga tushirish
uvicorn main:app --reload --port 8000
```

---

## 📄 Hujjatlar
- 📑 [Master Project Specification](MASTER_PROJECT_SPECIFICATION.md)
- 📋 [Top 100 Backlog Tasks](BACKLOG_100_TASKS.md)
