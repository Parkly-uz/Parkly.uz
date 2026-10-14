# 📋 Parkly.uz — Rasmiy Product Backlog, User Stories va Sifat Mezonlari

> **Loyiha:** Parkly.uz — Smart Parking Management System  
> **Repozitoriy:** [github.com/erjigitvv5/Parkly.uz](https://github.com/erjigitvv5/Parkly.uz) / [github.com/Parkly-uz/Parkly.uz](https://github.com/Parkly-uz/Parkly.uz)  
> **Boshqaruv Usuli:** Agile / Scrum (2 haftalik Sprintlar)  
> **Qat'iy SLA Cheklovi:** **Foydalanuvchi/Haydovchi maksimal kutish vaqti ≤ 10 daqiqa (User Wait Max 10 Min)**  
> **Uskuna va Mantiq:** Real-time RTSP/IP Kameralar ANPR, Sensor Simulyatori, Desktop Admin (PyQt6 / C++ Qt), PostgreSQL / SQLite

---

## 🧭 1. Backlog Prioritetlari va Baholash Standarti (Prioritization Framework)

Barcha vazifalar **MoSCoW** va **P0–P3** tizimi bo'yicha qat'iy ustuvorliklarga ajratilgan:

| Prioritet | MoSCoW | Ahamiyati va Ta'rifi | SLA / Reaksiya Vaqti |
| :---: | :---: | :--- | :---: |
| **P0** | **Must Have (Blocker)** | **Kritik / Blocker:** 10 daqiqalik kutish SLA'si buzilishi, shlagbaum bloklanishi, kamera to'liq uzilishi, xavfsizlik va ma'lumotlar yo'qolishi xavfi. | **Zudlik bilan (< 15 daqiqa)** |
| **P1** | **Must Have (Core)** | **Asosiy Oqim (Core MVP):** ANPR raqamni aniqlash, bo'sh joy ajratish (Spot Allocator), tarif hisoblash, RBAC ruxsatlar matritsasi. | **Joriy Sprint (Sprint 1–2)** |
| **P2** | **Should Have** | **Yuqori Qiymatli Qulaylik:** Onlayn to'lov (Payme/Click sandbox), Excel/CSV moliyaviy hisobotlar, vaqt to'qnashuvisiz oldindan bron qilish. | **Navbatdagi Sprint (Sprint 3)** |
| **P3** | **Could Have** | **Qo'shimcha Takomillashtirish:** SMS/Telegram bildirishnomalar, qorong'i UI mavzusi, qidiruv filtrlarining kengaytirilgan variantlari. | **Keyingi relizlar (Sprint 4+)** |

* **Story Point (SP):** Fibonachchi shkalasi (1, 2, 3, 5, 8, 13) asosida baholanadi (1 SP ≈ 4 soatlik sof muhandislik mehnati).

---

## 🎯 2. To'liq Agile User Story'lar va Qabul Qilish Mezonlari (Acceptance Criteria)

---

### 🚗 US-01: Kirish Shlagbaumida Avtomatik ANPR va 10 Daqiqa Maksimal Kutish Kafolati
* **Kod:** `US-01` | **Prioritet:** `P0 (Must Have)` | **Yuklama:** `8 SP` | **Mas'ul:** AI Lead & Backend Dev

#### User Story:
> **Haydovchi sifatida,**  
> men avtoturargoh kirish postiga kelganimda davlat raqamim kamera orqali soniyalar ichida aniqlanishini, optimal bo'sh slot ko'rsatilib shlagbaum ochilishini xohlayman,  
> **toki** men va orqamdagi transportlar tirbandlikda va navbatda **maksimal 10 daqiqadan ko'p kutib qolmasin**.

#### 📋 Acceptance Criteria (Qabul Qilish Mezonlari - Given / When / Then):
- [ ] **AC-01.1 (Tezlik va Kadrni Qayta Ishlash):**
  - **Given:** Avtomobil kirish shlagbaumining induktiv datchigi yoki kamerasi ko'rish maydoniga kirdi.
  - **When:** Kamera kadrlarni ANPR quvuriga yuboradi.
  - **Then:** Tizim 150 ms dan kam vaqtda avto raqamini aniqlaydi va bazadagi sessiyani ochadi.
- [ ] **AC-01.2 (⏱️ Qat'iy 10 Daqiqalik Kutish SLA Qoidasi):**
  - **Normal Holat (0 – 15 soniya):** ANPR raqamni `>= 85%` ishonchlilik bilan o'qiydi, shlagbaum ochiladi.
  - **Kechikish / Noaniqlik (15 soniya – 3 daqiqa):** Raqam iflos yoki qorongi bo'lsa, navbat operator monitoriga "Diqqat: Qo'lda tekshirish" (Manual Verification) ga tushadi.
  - **Sariq Ogohlantirish (5 daqiqa):** Agar bitta avtomobil postda 5 daqiqa qolib ketsa, operator panelida vizual taymer sariq rangda miltillaydi va operatorga SMS/Push xabar ketadi.
  - **Qizil Ogohlantirish (7 daqiqa):** Navbat 7 daqiqaga yetganda Super-Admin panelida favqulodda signal chalinadi va shlagbaumni majburiy ochish taklifi chiqadi.
  - **Kafolatlangan Fail-Safe (10 daqiqa):** Tizim avtomobilni postda **10 daqiqadan ortiq ushlab turishga mutlaqo yo'l qo'ymaydi**. 10 daqiqa to'lganda shlagbaum avtomatik ravishda bir martalik vaqtinchalik offline-talon (Emergency Pass Ticket) chop etib ochiladi, voqea `CRITICAL_SLA_BREACH` audit jurnaliga yoziladi.
- [ ] **AC-01.3 (Aqlli Joy Ajratish):**
  - Kirgan avtomobil turiga qarab (Standart, Elektromobil, VIP) eng maqbul joy (masofa va qavat bo'yicha) belgilanadi va LED axborot tablosida `Slot: A-101 (1-qavat)` ko'rsatiladi.

---

### 📷 US-02: Kameralar Mantiqi, Multi-Kadr Konsensusi va Noaniq Raqamlarni Hal Qilish
* **Kod:** `US-02` | **Prioritet:** `P0 (Must Have)` | **Yuklama:** `8 SP` | **Mas'ul:** AI / Vision Muhandisi

#### User Story:
> **Navbatchi operator sifatida,**  
> men kirish va chiqishdagi barcha kameralarning jonli oqimini (FPS, kechikish, ishonchlilik indeksi) real-vaqtda kuzatishni va noto'g'ri o'qilgan raqamlarni 15 soniyada qo'lda to'g'rilashni xohlayman,  
> **toki** kamera xatosi sababli haydovchi tirbandlikda qolib ketmasin va kutish vaqti 10 daqiqaga yetmasin.

#### 📋 Acceptance Criteria:
- [ ] **AC-02.1 (Multi-Source RTSP / IP Streaming):**
  - Tizim RTSP, IP-kamera, USB web-kamera va sinov video manbalarini uzluksiz 10+ FPS tezlikda qabul qilishi shart.
- [ ] **AC-02.2 (Ruxsat etilgan Ishonchlilik Chegaralari):**
  - `Confidence Score >= 85%`: Shlagbaum avtomatik ochiladi (Zero-Human-Touch).
  - `50% <= Confidence Score < 85%`: Operator monitorida tezkor kadr kattalashtirilib, raqamni 1-click orqali tasdiqlash yoki tahrirlash taklif etiladi.
  - `Confidence Score < 50%`: Kadr avtomatik ravishda ikki tomonlama filtrga (Bilateral + CLAHE) yuborilib, qayta skanerlanadi.
- [ ] **AC-02.3 (Multi-Frame Temporal Voting):**
  - Raqam bitta kadr bilan emas, ketma-ket kamida 3 ta kadr konsensusi asosida tasdiqlanadi (masalan, 5 kadr ichida 4 ta `01 A 777 AA` bo'lsa, shovqinli 1 ta kadr inkor qilinadi).
- [ ] **AC-02.4 (Kamera Nosozligi - Watchdog):**
  - Agar biror kamera bilan aloqa 5 soniyadan ortiq uzilsa, tizim darhol zaxira kameraga ulanadi va operator panelida ogohlantirish beradi.

---

### 💳 US-03: Chiqishdagi To'lov Nazorati va To'lov Tizimi Uzilgandagi Post-Pay Himoyasi
* **Kod:** `US-03` | **Prioritet:** `P1 (Must Have)` | **Yuklama:** `5 SP` | **Mas'ul:** Backend Dev & Integrator

#### User Story:
> **Haydovchi sifatida,**  
> men avtoturargohdan chiqish shlagbaumiga borganimda to'lov holatim avtomatik tekshirilib, to'langan bo'lsa darhol shlagbaum ochilishini, agar to'lanmagan bo'lsa qulay QR-kod berilishini xohlayman,  
> **toki** chiqish darvozasida to'lov muammolari sabab 10 daqiqadan ortiq ushlanib qolmay.

#### 📋 Acceptance Criteria:
- [ ] **AC-03.1 (15 Daqiqalik Bepul Muddat va Chiqish Imtiyozi):**
  - Dastlabki 15 daqiqa ichida kirib-chiqqan transportlar uchun to'lov summasi 0 so'm deb hisoblanadi va darhol chiqishga ruxsat etiladi.
  - To'lov amalga oshirilgandan so'ng chiqib ketish uchun qo'shimcha 15 daqiqalik bepul chiqish darchasi (Exit Grace Period) beriladi.
- [ ] **AC-03.2 (To'lov Tizimi Uzilishi va 10 Daqiqa Fallback):**
  - **Given:** Chiqish shlagbaumida Payme/Click billing provayderi javob bermayapti yoki bank serveri ishlamayapti.
  - **When:** Haydovchining navbatda turish vaqti **7 daqiqaga** yetdi.
  - **Then:** Operator ekranida "Keyinchalik To'lash Kafolati" (Post-Payment Guarantee Ticket) opsiyasi paydo bo'ladi.
  - **And:** 10 daqiqa to'lganda avtomobil raqamiga elektron qarz vaucheri (SMS havola) biriktirilib, haydovchi chiqarib yuboriladi; haydovchi 10 daqiqadan ko'p ushlab turilmaydi.

---

### 🛡️ US-04: RBAC Huquqlar Matritsasi va Xavfsizlik Boshqaruvi
* **Kod:** `US-04` | **Prioritet:** `P1 (Must Have)` | **Yuklama:** `5 SP` | **Mas'ul:** Security & Desktop Dev

#### User Story:
> **Bosh rahbar (Super-Admin) sifatida,**  
> men operatsion xodimlar va operatorlar faqat o'zlariga tegishli monitoring sahifalarini ko'rishini, tariflar va tizim sozlamalariga teginolmasligini xohlayman,  
> **toki** inson omili sababli moliyaviy va texnik konfiguratsiyalar buzilmasin.

#### 📋 Acceptance Criteria:
- [ ] **AC-04.1 (Super-Admin Huquqlari - 2 kishi):**
  - Barcha 7 ta modulga (Dashboard, 3D Xarita, Kameralar, Moliya, Sessiyalar, Xodimlar, Sozlamalar) to'liq kirish va tahrirlash huquqi.
  - Tariflarni o'zgartirish, admin akkauntlarini yaratish/o'chirish va shlagbaumni favqulodda (Emergency Override) ochish huquqi.
- [ ] **AC-04.2 (Oddiy Admin Huquqlari - 4 kishi):**
  - Real-vaqt monitoringi, 3D xarita, ANPR kameralari va 4-Moliya bo'limini ko'rish va hisobotlarni Excel/CSV formatida yuklab olish ruxsati.
  - ❌ **Taqiqlangan:** Tariflarni tahrirlash (modal qulflangan), Xodimlar (5) va Tizim Sozlamalari (6) bo'limlariga kirish (qulflangan 🔒 belgi va ogohlantirish oynasi).
- [ ] **AC-04.3 (Smena Operatori Huquqlari - 2 kishi):**
  - Faqat joriy smena monitoringi, shlagbaumni qo'lda tekshirib ochish (sababini ko'rsatgan holda audit jurnaliga yozish sharti bilan).

---

## 📷 3. Kameralar Mantiqi Bo'yicha Chuqur Texnik Vazifalar (Camera Logic Technical Tasks)

Kamera tizimini ishlab chiqish va sinovdan o'tkazish uchun 10 ta aniq texnik vazifa:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PARKLY.UZ CAMERA LOGIC PIPELINE                        │
└─────────────────────────────────────────────────────────────────────────────┘
  [RTSP/IP Cam] ──► [Zero-Latency Buffer] ──► [Adaptive CLAHE & Denoise]
                           │
                           ▼
  [Two-Stage Detector] ──► [Homography Warp] ──► [Uzbekistan OCR Engine]
                           │
                           ▼
  [Temporal Voting (3 Frames)] ──► [Confidence Gate (85% Auto / <85% Manual)]
                           │
                           ▼
  [⏱️ 10-Minute SLA Watchdog (Alert at 5m/7m -> Emergency Fail-Safe at 10m)]
```

| Task ID | Texnik Vazifa Nomi | Texnologik Qatlam | Tavsifi va Qabul Talabi | SP |
| :---: | :--- | :---: | :--- | :---: |
| **CAM-01** | **Multi-Source Zero-Latency RTSP Streamer** | OpenCV / Threading | RTSP va IP kameralardan oqimni bufer to'lib ketishisiz (lag yo'q) fondagi oqimda qabul qilish, avtomatik qayta ulanish (Reconnect Watchdog) | 5 |
| **CAM-02** | **Adaptive CLAHE & Glare Suppression** | OpenCV (CV_8UC1) | Tungi qorong'ilik va avtomobil faralari nurini bartaraf etuvchi dinamik yorug'lik filtri, kadr gistogrammasini avtomatik tekislash | 5 |
| **CAM-03** | **Two-Stage Plate Region Detector** | PyTorch / OpenCV | Kadr ichidan avval transport vositasini, so'ngra 4.5:1 proporsiyadagi davlat raqami to'rtburchagini ajratib oluvchi ikki bosqichli detektor | 8 |
| **CAM-04** | **Homography Perspective Rectification** | OpenCV (WarpPerspective)| 30°–45° burchak ostida turgan qiyshiq raqam rasmini 4 ta nuqta koordinatasi bo'yicha to'g'ri to'rtburchak shaklga aylantirib beruvchi transformatsiya | 5 |
| **CAM-05** | **Uzbekistan Plate Disambiguation OCR** | Regex / Tesseract / EasyOCR | O'zbekiston standartlari (`01 A 777 AA` va `01 123 AAA`) bo'yicha harf-raqam chalkashliklarini avtomatik tuzatish (`O` <-> `0`, `B` <-> `8`, `Z` <-> `2`) | 5 |
| **CAM-06** | **Sliding Window Temporal Voting Tracker** | Python Data Structures | 1.5–2.0 soniya ichidagi ketma-ket 3–5 ta kadr natijalarini to'plab, ko'pchilik ovozi bilan eng to'g'ri yakuniy raqamni aniqlash mexanizmi | 5 |
| **CAM-07** | **Confidence Score Decision Engine** | Backend Logic | `>= 85%` bo'lganda avtomatik shlagbaum ochish signali berish, `< 85%` bo'lganda operator paneliga snapshot va ovozli bildirishnoma yuborish | 3 |
| **CAM-08** | **10-Minute SLA Watchdog Daemon** | Background Worker / Asyncio | Har bir avtomobilning kamera maydonida turish vaqtini nazorat qiluvchi taymer; 5-daqiqada sariq, 7-daqiqada qizil, 10-daqiqada avtomatik favqulodda ochish | 5 |
| **CAM-09** | **Desktop ANPR Live Stream & Override Widget**| PyQt6 / C++ Qt | Operator uchun real-vaqt video oynasi, aniqlangan raqamlar ro'yxati, confidence ko'rsatkichi va 1-tugmali qo'lda tasdiqlash dialogi | 5 |
| **CAM-10** | **Offline Camera Fallback & Audit Logger** | SQLite / PostgreSQL | Kamera uzilganda test simulyatsiyasi rejimiga o'tish, shlagbaumning har bir ochilish/yopilish sabablarini vaqt belgilari bilan bazada saqlash | 3 |

---

## 📊 4. GitHub va Taskcafe Loyiha Doskasi Ko'rinishi (Taskcafe / GitHub Projects Scope)

Loyiha boshqaruvi uchun **Taskcafe** va **GitHub Projects** kanban doskasining to'liq arxitekturasi:

### A. Ustunlar (Board Lanes):
1. **`📥 [Product Backlog]`** — Barcha rejalashtirilgan va ustuvorligi aniqlangan User Story'lar bazasi.
2. **`🎯 [Sprint Backlog / Ready]`** — Joriy 2 haftalik sprint uchun ajratilgan va texnik talablari tayyor vazifalar.
3. **`🚧 [In Progress]`** — Hozirda dasturchi tomonidan kod yozilayotgan vazifalar (WIP Limit: 1 kishiga max 2 ta).
4. **`🧪 [Review & QA]`** — Pull Request ochilgan, testlar (pytest/unittest) o'tayotgan va kod tekshiruvidagi vazifalar.
5. **`🚀 [Done / Shipped]`** — `main` branchga merge qilingan, barcha Acceptance Criteria'lar va 10 minutlik SLA sinovlaridan o'tgan vazifalar.

---

### B. Taskcafe Swimlane'lar (Qatorlar bo'yicha chegaralanish):
* **🔥 Swimlane 1: Expedite / SLA Critical (P0)** — 10 daqiqalik maksimal kutish SLA'si, shlagbaum blokirovkasi, kamera uzilish xatarlari.
* **📷 Swimlane 2: Computer Vision & ANPR Logic** — Kameralar oqimi, detektor, OCR va temporal voting vazifalari.
* **💳 Swimlane 3: Core Backend, RBAC & Finance** — 4-Moliya moduli, rollar matritsasi, tariflar va hisobotlar.

---

### C. Taskcafe / GitHub Loyiha Kartochkalari Namoyishi (Live Preview Mockup):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  TASKCAFE / GITHUB PROJECTS KANBAN BOARD PREVIEW                                       │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ 🎯 SPRINT BACKLOG (READY)│ 🚧 IN PROGRESS           │ 🚀 DONE / SHIPPED                │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ [P0-CRITICAL] [8 SP]     │ [P0-CRITICAL] [5 SP]     │ [P1-CORE] [5 SP]                 │
│ US-01: Kirishda ANPR va  │ CAM-08: 10-Min SLA       │ US-04: RBAC Huquqlar Matritsasi  │
│ 10-Minut Max Kutish SLA  │ Watchdog & Emergency     │ (2 Super, 4 Oddiy Admin)         │
│                          │ Fail-Safe Daemon         │                                  │
│ 🏷️ `sla:max-10min` `anpr`│ 🏷️ `sla:max-10min` `core`│ 🏷️ `rbac` `security` `desktop`   │
│ 👤 @dev_ai  ⏱️ Max 10 min│ 👤 @dev_backend ⏱️ 10m  │ 👤 @erjigitvv5  ✅ 20 Tests OK   │
│ Checklist: 0/3 AC met    │ Checklist: 2/3 AC met    │ Checklist: 3/3 AC met            │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ [P0-CRITICAL] [8 SP]     │ [P0-CRITICAL] [5 SP]     │ [P1-CORE] [8 SP]                 │
│ CAM-03: Two-Stage Plate  │ CAM-06: Multi-Frame      │ MODUL-04: Moliya va Tranzaksiya  │
│ Region Detector (YOLO)   │ Temporal Voting (Consen) │ Hisobotlari & Haftalik Chart     │
│ 🏷️ `vision` `ai`         │ 🏷️ `vision` `python`     │ 🏷️ `finance` `excel-export`      │
│ 👤 @dev_ai               │ 👤 @dev_ai               │ 👤 @erjigitvv5  ✅ Excel BOM     │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ [P2-MEDIUM] [5 SP]       │ [P1-HIGH] [5 SP]         │ [P1-CORE] [5 SP]                 │
│ US-03: Chiqishda To'lov  │ CAM-09: PyQt6 Desktop    │ SIM-01: Virtual Sensor va Slot   │
│ Nazorati & Post-Pay Tiket│ Live Stream & Override UI│ CLI Simulyatori (UTF-8 Xavfsiz)  │
│ 🏷️ `billing` `sla:10min` │ 🏷️ `desktop-admin` `ui`  │ 🏷️ `simulator` `no-emojis`       │
│ 👤 @dev_backend          │ 👤 @dev_desktop          │ 👤 @erjigitvv5  ✅ Windows OK    │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

## 🏁 5. Definition of Ready (DoR) va Definition of Done (DoD)

### Definition of Ready (DoR) — Vazifa Sprintga olinishi uchun:
1. User story rasmiy formatda yozilgan bo'lishi shart (`As a... I want... So that...`).
2. Kamida 3 ta aniq va tekshiriluvchi Acceptance Criteria (shu jumladan 10 minutlik kutish SLA'si) ko'rsatilgan.
3. Story Point (SP) bahosi jamoa a'zolari tomonidan kelishilgan.
4. Bog'liq vazifalar (Dependencies) aniqlangan va to'siqlar yo'q.

### Definition of Done (DoD) — Vazifa "Done" deb tan olinishi uchun:
1. Barcha Acceptance Criteria'lar sinovdan o'tgan va tasdiqlangan.
2. Hech bir holatda foydalanuvchining kutish vaqti 10 daqiqadan oshmasligi avtotest bilan tekshirilgan.
3. Unit va integratsion testlar yozilgan (`pytest` va `unittest` 100% yashil).
4. Kod standartlarga mos (PEP8, linter, no-warnings), Git branch `main` ga PR orqali merge qilingan.
5. README yoki texnik hujjatlarga zarur o'zgartirishlar kiritilgan.
