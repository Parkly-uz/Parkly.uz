# 📋 Parkly.uz — Taskcafe & GitHub Projects Kanban Board Scope

> **Loyiha:** Parkly.uz — Smart Parking Management System  
> **Doska Turi:** Taskcafe / GitHub Projects Kanban Board (Sanoat standarti)  
> **Qat'iy SLA Cheklovi:** **Foydalanuvchi maksimal kutish vaqti ≤ 10 daqiqa (User Wait Max 10 Min)**  
> **Joriy Sprint:** Sprint 3 (MVP: Vision ANPR, 10-min SLA Watchdog, Spot Allocator, No-Automation Payments, Moliya & RBAC)  
> **GitHub Repozitoriyasi:** [github.com/erjigitvv5/Parkly.uz](https://github.com/erjigitvv5/Parkly.uz) / [github.com/Parkly-uz/Parkly.uz](https://github.com/Parkly-uz/Parkly.uz)

---

## 🌊 1. Taskcafe Swimlane'lar (Prioritet bo'yicha Qatorlar)

* **🔥 Swimlane 1: [P0-CRITICAL] SLA Blocker & Hardware Fail-Safe (Max 10-Min Wait)**  
  *Shlagbaum blokirovkasi, kamera uzilishi, 10 daqiqalik kutish chegarasi buzilishiga qarshi avtomatlashtirilgan choralar va xatarlarni yumshatish.*
* **📷 Swimlane 2: [P0/P1] Computer Vision, Camera ANPR & Spot Allocation**  
  *RTSP oqimi, Adaptive CLAHE, Two-Stage YOLO detektor, Homography to'g'irlash, Temporal Voting, OCR va bo'sh joylarni aqlli taqsimlash.*
* **💳 Swimlane 3: [P1/P2] Core Backend, Payments (Naqd/POS & Onlayn) & RBAC Finance**  
  *2 Super-Admin, 4 Oddiy Admin matritsasi, 4-Moliya moduli, naqd/POS avtomatlashtirilmagan to'lovlar, 7 kunlik grafik va Excel eksport.*

---

## 📌 2. Kanban Doskasi Ustunlari va Kartochkalar (Board Lanes & Cards)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    TASKCAFE KANBAN BOARD ARCHITECTURE                                                 │
├────────────────────┬────────────────────┬────────────────────┬────────────────────┬───────────────────────────────────┤
│ 📥 Product Backlog │ 🎯 Sprint Ready    │ 🚧 In Progress     │ 🧪 Review & QA     │ 🚀 Done / Shipped                 │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┴───────────────────────────────────┘
```

---

### 🚀 USTUN 1: [ 🚀 Done / Shipped ] (Muvaffaqiyatli Yakunlangan va Merge Qilingan)

#### 🎴 CARD-DONE-01: US-04 — RBAC Huquqlar Matritsasi va Xavfsizlik Enforcing
* **ID:** `PRK-CARD-001` | **Story:** `US-04` | **Prioritet:** `[P1-CORE]` | **SP:** `5`
* **Mas'ul:** `@erjigitvv5` | **Holati:** `DONE` | **Teglar:** `rbac`, `security`, `desktop-admin`
* **Tavsif:** Tizimda 2 ta Super-Admin, 4 ta Oddiy Admin va 2 ta Smena Operatori huquqlar matritsasi shakllantirildi. Oddiy adminlar uchun Xodimlar va Tizim sozlamalari qulflandi, tarif o'zgartirish taqiqlandi.
* **Acceptance Criteria Holati:**
  - [x] Super-Admin (2 kishi: `admin`, `superadmin2`) barcha 7 modulga to'liq kirdi.
  - [x] Oddiy Admin (4 kishi) Moliya bo'limini ko'radi, lekin Xodimlar va Sozlamalardan bloklandi (🔒).
  - [x] DB darajasida `update_tariff_rates` faqat Super-Admin ruxsatida ishlaydi.
* **Test Holati:** `tests/test_rbac_finance.py` — 100% muvaffaqiyatli o'tgan.

#### 🎴 CARD-DONE-02: MODUL-04 — Moliya va Tranzaksiyalar Bo'limi (Navigatsiyada 4-o'rin)
* **ID:** `PRK-CARD-002` | **Story:** `US-03` | **Prioritet:** `[P1-CORE]` | **SP:** `8`
* **Mas'ul:** `@erjigitvv5` | **Holati:** `DONE` | **Teglar:** `finance`, `chart`, `excel-export`
* **Tavsif:** Navigatsiya menyusida aynan 4-o'ringa joylashtirildi. 4 ta asosiy backend/UI funksiya (`get_financial_summary`, `get_transaction_history`, `export_financial_report`, `update_tariff_rates`) ishga tushirildi.
* **Acceptance Criteria Holati:**
  - [x] Kunlik, haftalik va oylik tushum kartochkalari (Deep Slate Gradient fonida).
  - [x] So'nggi 7 kunlik daromad dinamikasi bo'yicha native PyQt6 vektorli bar chart grafigi.
  - [x] Windows Excel bilan 100% mos UTF-8 BOM (`utf-8-sig`) va `;` formatidagi CSV eksport.
  - [x] Super-Admin uchun tariflarni boshqarish modali (`TariffRatesDialog`).

#### 🎴 CARD-DONE-03: SIM-01 — Virtual Sensor va Slot Simulyatori (Windows UTF-8 Himoyasi)
* **ID:** `PRK-CARD-003` | **Prioritet:** `[P1-CORE]` | **SP:** `5`
* **Mas'ul:** `@dev4_iot` | **Holati:** `DONE` | **Teglar:** `simulator`, `cli`, `windows-safe`
* **Tavsif:** Slotlar holatini real-vaqtda simulyatsiya qiluvchi CLI dvigateli. Windows konsollaridagi `UnicodeEncodeError` bartaraf etildi, UTF-8 xavfsiz rejimga o'tkazildi.
* **Acceptance Criteria Holati:**
  - [x] `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` himoyasi o'rnatildi.
  - [x] O'zbekiston davlat raqamlari generatori xatosiz ishlaydi.

#### 🎴 CARD-DONE-04: CORE-01 — Package Architecture va Imports Standartlashtirish
* **ID:** `PRK-CARD-004` | **Prioritet:** `[P0-CRITICAL]` | **SP:** `3`
* **Mas'ul:** `@lead_dev` | **Holati:** `DONE` | **Teglar:** `architecture`, `python`, `requirements`
* **Tavsif:** `ModuleNotFoundError: No module named 'app'` to'g'rilandi, barcha paketlar uchun `__init__.py` yaratildi, `requirements.txt` qo'shildi va testlar 20/20 yashil holatga keltirildi.

---

### 🧪 USTUN 2: [ 🧪 Review & QA ] (Kod Tekshiruvi va Avtotestlar Bosqichi)

#### 🎴 CARD-QA-01: CAM-08 — 10-Minute SLA Watchdog & Emergency Fail-Safe
* **ID:** `PRK-CARD-005` | **Story:** `US-01` | **Prioritet:** `[P0-CRITICAL]` | **SP:** `5`
* **Mas'ul:** `@dev_backend` | **Reviewer:** `@lead_dev` | **Teglar:** `sla:max-10min`, `fail-safe`, `security`
* **⏱️ Qat'iy SLA Sharti:** **User Wait Max 10 Minut**
* **Tavsif:** Kirish va chiqish postlarida har bir avtomobilning kutish vaqtini kuzatuvchi va 10 daqiqadan oshib ketishiga mutlaqo yo'l qo'ymaydigan monitoring dvigateli.
* **Acceptance Criteria:**
  - [x] `wait_minutes < 5.0` min: `level="NORMAL"`, `force_open=False` (Yashil holat).
  - [x] `5.0 <= wait_minutes < 7.0` min: `level="WARNING"` (Operator monitorida sariq xabarnoma).
  - [x] `7.0 <= wait_minutes < 10.0` min: `level="URGENT"` (Super-Adminga qizil eskalatsiya signali).
  - [x] `wait_minutes >= 10.0` min: `level="FAIL_SAFE_BREACH"`, `force_open=True`, `GateAction.OPEN_BARRIER` bilan shlagbaum darhol ochiladi va elektron talon beriladi.
* **DoD Tekshiruvi:** `tests/test_algorithms.py` da unit testlar yozildi va tasdiqlandi.

#### 🎴 CARD-QA-02: CAM-05 — Uzbekistan Plate Disambiguation OCR Engine
* **ID:** `PRK-CARD-006` | **Story:** `US-02` | **Prioritet:** `[P1-CORE]` | **SP:** `5`
* **Mas'ul:** `@dev_ai` | **Reviewer:** `@lead_dev` | **Teglar:** `anpr`, `ocr`, `regex-uz`
* **Tavsif:** O'zbekiston davlat raqamlari formatidagi harf va raqamlarni (`O` <-> `0`, `B` <-> `8`, `Z` <-> `2`, `S` <-> `5`) pozitsion regex qoidalari asosida avtomatik to'g'rilash.
* **Acceptance Criteria:**
  - [x] 1-2 o'rin faqat raqam bo'lishi shart (Viloyat kodi: `01`-`95`).
  - [x] `01 A 777 AA` va `01 777 AAA` formatlariga mos kelishi 100% tekshirildi.

---

### 🚧 USTUN 3: [ 🚧 In Progress ] (Hozirda Dasturchilar Bajarayotgan Vazifalar)

#### 🎴 CARD-WIP-01: SPOT-01 — Parkovkada Bo'sh Joyni Aqlli Aniqlash (Spot Allocator)
* **ID:** `PRK-CARD-007` | **Story:** `US-02` | **Prioritet:** `[P1-HIGH]` | **SP:** `5`
* **Mas'ul:** `@dev_backend` | **Tugash Muddati:** Sprint 3 | **Teglar:** `spot-allocation`, `smart-parking`, `ev`
* **Tavsif:** Kirgan transport vositasining turiga (`EV_CHARGING`, `REGULAR`, `VIP_STAFF`, `ACCESSIBLE`) mos ravishda kirish eshigiga eng yaqin va qulay bo'sh joyni evristik xarajat formulasi bo'yicha tanlash.
* **Acceptance Criteria:**
  - [ ] Elektromobil bo'lsa quvvatlash stansiyasi bor slot tanlanadi.
  - [ ] Qavat o'zgarishi uchun +200 jarima balli qo'shiladi.
  - [ ] Tanlangan slot darhol LED tabloga va Desktop 3D xaritaga chiqariladi.

#### 🎴 CARD-WIP-02: PAY-02 — Avtomatlashtirilmagan (Naqd / POS-terminal) To'lov Moduli
* **ID:** `PRK-CARD-008` | **Story:** `US-03` | **Prioritet:** `[P1-HIGH]` | **SP:** `5`
* **Mas'ul:** `@dev_backend` | **Tugash Muddati:** Sprint 3 | **Teglar:** `manual-payment`, `cash`, `pos-terminal`
* **Tavsif:** Onlayn to'lov bo'lmaganda yoki internet uzilganda haydovchining operatorga naqd pul yoki POS-karta orqali to'lashini ta'minlovchi qo'lda tasdiqlash oynasi va fiskal kvitansiya generatsiyasi.
* **Acceptance Criteria:**
  - [ ] Operator "Naqd to'lov qabul qilindi" tugmasini bosganda sessiya `PAID` holatiga o'tadi va shlagbaum ochiladi.
  - [ ] Internet yoki bank serveri ishlamasa, 10 daqiqa to'lganda "Post-Payment qarz taloni" chiqarilib, haydovchi qo'yib yuboriladi.

#### 🎴 CARD-WIP-03: SYNC-01 — Kirish va Chiqishda Real-Vaqt Ma'lumotlarni Yangilash
* **ID:** `PRK-CARD-009` | **Story:** `US-01 / US-03` | **Prioritet:** `[P0-CRITICAL]` | **SP:** `5`
* **Mas'ul:** `@dev_desktop` | **Tugash Muddati:** Sprint 3 | **Teglar:** `real-time`, `state-machine`, `3d-map`
* **Tavsif:** Mashina kirishi yoki chiqishi bilan butun tizim bo'ylab (DB, Desktop 3D xarita, Dashboard KPI, Kassa hisoboti) ma'lumotlarning soniyalar ichida yangilanishi.
* **Acceptance Criteria:**
  - [ ] Kirish: Slot holati `FREE` -> `OCCUPIED`, 3D xaritada mashina modeli va jonli taymer paydo bo'ladi.
  - [ ] Chiqish: Slot holati `OCCUPIED` -> `FREE`, 3D xaritadan mashina o'chiriladi, kassa tushumiga pul qo'shiladi.

#### 🎴 CARD-WIP-04: CAM-03 — Two-Stage Plate Region Detector (YOLO/Haar Cascade)
* **ID:** `PRK-CARD-010` | **Story:** `US-02` | **Prioritet:** `[P0-CRITICAL]` | **SP:** `8`
* **Mas'ul:** `@dev_ai` | **Tugash Muddati:** Sprint 3 | **Teglar:** `vision`, `yolo`, `ai`
* **Tavsif:** Umumiy kadr ichidan avval transport vositasini topish, so'ngra uning bamperidan 4.5:1 proporsiyadagi raqam maydonini yuqori aniqlikda kesib olish.

---

### 🎯 USTUN 4: [ 🎯 Sprint Backlog / Ready ] (Keyingi Qadamda Boshlanadigan Vazifalar)

#### 🎴 CARD-RDY-01: RSK-01 — Xatarlar Reestri va Eskalatsiya Mexanizmi
* **ID:** `PRK-CARD-011` | **Story:** `US-PM-01` | **Prioritet:** `[P0-CRITICAL]` | **SP:** `3`
* **Mas'ul:** `@lead_dev` | **Teglar:** `risk-management`, `sla`, `monitoring`
* **Tavsif:** 6 ta asosiy xatar (10-min SLA buzilishi, kamera uzilishi, bank agregatori xatosi, blackout) monitoringi va avtomatik zaxira tizimlari.

#### 🎴 CARD-RDY-02: UI-01 — Minimalist Dribbble Container Shadows & Badges
* **ID:** `PRK-CARD-012` | **Story:** `US-UI-01` | **Prioritet:** `[P2-MEDIUM]` | **SP:** `3`
* **Mas'ul:** `@dev_desktop` | **Teglar:** `ui-ux`, `dribbble`, `minimalism`
* **Tavsif:** Barcha oq bloklarga `16px border-radius`, mayin chegara chiziqlari, Deep Slate Gradient va monospace avto raqami stikeri vizualizatsiyasini to'liq joriy etish.

#### 🎴 CARD-RDY-03: CAM-04 — Homography Perspective Rectification
* **ID:** `PRK-CARD-013` | **Story:** `US-02` | **Prioritet:** `[P1-HIGH]` | **SP:** `5`
* **Mas'ul:** `@dev_ai` | **Teglar:** `homography`, `warp`, `opencv`
* **Tavsif:** 30°–45° burchak ostida turgan qiyshiq raqam rasmini tekis to'rtburchakka aylantirish.

---

### 📥 USTUN 5: [ 📥 Product Backlog ] (Kelgusi Sprintlar va Strategik Vazifalar)

* **`[P2-MEDIUM]` `PRK-CARD-014`:** Click va Payme Sandbox webhook integratsiyasini to'liq yoqish (8 SP).
* **`[P2-MEDIUM]` `PRK-CARD-015`:** Mobil ilova (Flutter) haydovchi kabineti uchun slot rezervatsiya API (8 SP).
* **`[P3-LOW]` `PRK-CARD-016`:** Telegram Bot orqali avtomobil joylashuvi va kvitansiyasini jo'natish (3 SP).
* **`[P3-LOW]` `PRK-CARD-017`:** Desktop Admin ilovasida qorong'i rejim (Dark Mode / Theme) qo'llab-quvvatlovi (3 SP).
* **`[P2-MEDIUM]` `PRK-CARD-018`:** Shlagbaum apparaturasi uchun Modbus/MQTT Relay drayverini C++ da integratsiya qilish (5 SP).

---

## 📋 3. Taskcafe / GitHub Loyihasini Sozlash Ko'rsatmasi

1. **GitHub Projects doskasi:**
   - [github.com/erjigitvv5/Parkly.uz/projects](https://github.com/erjigitvv5/Parkly.uz) bo'limiga kiring.
   - **New Project** -> **Board** shablonini tanlang.
   - Yuqoridagi 5 ta ustunni yarating: `Product Backlog`, `Sprint Backlog (Ready)`, `In Progress`, `Review & QA`, `Done / Shipped`.
2. **Custom Field'lar (Maxsus maydonlar):**
   - `SLA Limit`: Single select (`Normal`, `Max 10-Min SLA`, `Fail-Safe`).
   - `Story Points`: Number (`1, 2, 3, 5, 8, 13`).
   - `Priority`: Single select (`P0-Critical`, `P1-Core`, `P2-Medium`, `P3-Low`).
   - `Module`: Single select (`1.Dashboard`, `2.Map`, `3.Cameras`, `4.Finance`, `5.Sessions`, `6.Staff`, `7.Settings`).
   - `Payment Method`: Single select (`Online (Payme/Click)`, `No-Automation (Cash/POS)`).
3. **Avtomatlashtirish (Workflows):**
   - PR ochilganda kartochka avtomatik **Review & QA** ustuniga o'tadi.
   - PR `main` yoki `Mirhamid` branchga merge qilinganda kartochka avtomatik **Done / Shipped** ustuniga o'tadi.
