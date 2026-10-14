# 📋 Parkly.uz — Rasmiy Product Backlog, Epiklar va Texnik Talablar

> **Loyiha:** Parkly.uz — Smart Parking Management System  
> **Repozitoriy:** [github.com/erjigitvv5/Parkly.uz](https://github.com/erjigitvv5/Parkly.uz) / [github.com/Parkly-uz/Parkly.uz](https://github.com/Parkly-uz/Parkly.uz)  
> **Metodologiya:** Agile / Scrum (2 haftalik Sprintlar)  
> **Qat'iy SLA Cheklovi:** **Foydalanuvchi/Haydovchi maksimal kutish vaqti ≤ 10 daqiqa (User Wait Max 10 Min)**  
> **Asosiy Qoidalar:** Minimalist Dribbble/Figma UI/UX, Kamera Mantiqi (ANPR), Avtomatlashtirilmagan (Naqd/POS) to'lov, Bo'sh joylarni aqlli aniqlash, Real-vaqt Kirish/Chiqish sinxronizatsiyasi va Xatarlar Reestri (Risk Scope).

---

## 🎯 1. Loyiha Ko'lami (Project Scope Management)

### A. In-Scope (Loyiha doirasiga kiruvchi to'liq funksional):
1. **Kirish va Chiqish ANPR:** RTSP/IP kameralar orqali kadrni qayta ishlash, davlat raqamini aniqlash, ishonchlilik (Confidence score) nazorati va shlagbaum boshqaruvi.
2. **⏱️ 10 Daqiqalik Maksimal Kutish Kafolati (SLA):** Kirish/chiqishda haydovchining kutish vaqtini kuzatuvchi avtomatik taymer (3m normal, 5m sariq ogohlantirish, 7m qizil shoshilinch signal, 10m fail-safe favqulodda shlagbaumni ochish).
3. **Parkovkada Bo'sh Joyni Aqlli Aniqlash (Spot Allocation):** Avtomobil turi (Standart, Elektromobil, VIP, Maxsus ehtiyojli) va masofa evristikasi (Cost Function) asosida eng qulay bo'sh slotni tanlash va LED tabloga uzatish.
4. **To'lov Usullari (Avtomatlashtirilgan va Avtomatlashtirilmagan):**
   - *Avtomatlashtirilgan:* Payme va Click Sandbox onlayn to'lovlari.
   - *Avtomatlashtirilmagan (No-Automation / Manual):* Naqd pul (Cash) va Bank kartasi (POS-terminal) orqali operator kassasiga to'lash, fiskal chek chop etish va tizimda qo'lda tasdiqlash (`Mark as Paid Manually`). Tarmoq uzilganda offline qarz taloni berish.
5. **Real-Vaqtda Ma'lumotlarni Yangilash (Enter/Exit Real-Time Info Updating):**
   - Mashina kirishi bilan: DB sessiya ochiladi -> Slot `FREE` dan `OCCUPIED` ga o'tadi -> 3D xaritada mashina modeli va jonli taymer paydo bo'ladi -> Dashboard KPI ko'rsatkichlari yangilanadi.
   - Mashina chiqishi bilan: To'lov tasdiqlanadi -> Shlagbaum ochiladi -> Slot `FREE` bo'ladi -> 3D xaritadan mashina o'chiriladi -> Kassa tushumi va hisoboti soniyalarda oshadi.
6. **Desktop Admin Paneli (Minimalist UI/UX):**
   - 7 ta navigatsiya moduli: 1.Dashboard, 2.3D Izometrik Xarita, 3.Kameralar (ANPR), **4.Moliya va Tranzaksiyalar (aynan 4-o'rinda!)**, 5.Sessiyalar, 6.Xodimlar (RBAC), 7.Tizim Sozlamalari.
   - RBAC huquqlar matritsasi: 2 ta Super-Admin (to'liq kirish), 4 ta Oddiy Admin (monitoring va moliya ko'rish, lekin sozlamalar/xodimlar qulflangan 🔒), 2 ta Smena Operatori.
   - Vektorli 7 kunlik daromad grafigi va Excel uchun mos UTF-8 BOM (`utf-8-sig`) CSV eksport.

### B. Out-of-Scope (Ushbu reliz doirasiga kirmaydigan elementlar):
- Shaxsiy garajlarni ijaraga berish P2P platformasi.
- Avtomobillarni yuvish va servis xizmatlarini bron qilish.
- Yoqilg'i quyish shoxobchalari bilan to'g'ridan-to'g'ri integratsiya.

---

## 🧭 2. Backlog Prioritet Standarti (Prioritization Framework)

Barcha vazifalar **MoSCoW** va **P0–P3** tizimi asosida taqsimlangan:

| Prioritet | MoSCoW | Ahamiyati va Ta'rifi | Reaksiya / SLA |
| :---: | :---: | :--- | :---: |
| **P0** | **Must Have (Blocker)** | **Kritik / Blocker:** 10 daqiqalik kutish SLA'si buzilishi, shlagbaum bloklanishi, kamera to'liq uzilishi, kassa ma'lumotlari yo'qolishi. | **Zudlik bilan (< 15 daqiqa)** |
| **P1** | **Must Have (Core)** | **Asosiy Oqim (Core MVP):** ANPR raqamni aniqlash, bo'sh joy ajratish, naqd/POS to'lov tasdig'i, 4-Moliya hisoboti, RBAC matritsasi. | **Joriy Sprint (Sprint 1–2)** |
| **P2** | **Should Have** | **Yuqori Qulaylik:** Payme/Click onlayn to'lov, Excel hisobot eksport, vaqt to'qnashuvisiz oldindan bron qilish (Booking). | **Navbatdagi Sprint (Sprint 3)** |
| **P3** | **Could Have** | **Qo'shimcha Qulaylik:** SMS xabarnomalar, qorong'i UI mavzusi, kengaytirilgan qidiruv filtrlari. | **Keyingi relizlar (Sprint 4)** |

---

## 🎨 3. Minimalist UI/UX Dizayn Standarti (Design Specification)

Desktop Admin paneli eng nufuzli Dribbble va Figma minimalist dizayn qoidalariga asoslanadi:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MINIMALISTIC UI/UX COMPONENT STANDARDS                   │
├──────────────────────┬──────────────────────────────────────────────────────┤
│ Card Style           │ Oq fon (#ffffff), border-radius: 16px, border: 1px   │
│                      │ solid rgba(226, 232, 240, 0.8), soft shadow:         │
│                      │ box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03)          │
├──────────────────────┼──────────────────────────────────────────────────────┤
│ Deep Slate Gradient  │ linear-gradient(135deg, #0F172A 0%, #0066FF 100%)    │
│ (Asosiy Kassa KPI)   │ Matn rangi: #ffffff, oqish piktogrammalar            │
├──────────────────────┼──────────────────────────────────────────────────────┤
│ Monospace Avto Raqam │ font-family: 'Consolas', 'Courier New', monospace;   │
│ (Plate Sticker)      │ background: #f1f5f9; border: 1px solid #cbd5e1;      │
│                      │ border-radius: 6px; padding: 3px 8px; font-weight:700│
├──────────────────────┼──────────────────────────────────────────────────────┤
│ Status Badges        │ • BO'SH: bg #DCFCE7, text #166534, radius: 20px      │
│                      │ • BAND:  bg #FEE2E2, text #991B1B, radius: 20px      │
│                      │ • BRON:  bg #FEF3C7, text #92400E, radius: 20px      │
│                      │ • TA'MIR: bg #F1F5F9, text #475569, radius: 20px     │
├──────────────────────┼──────────────────────────────────────────────────────┤
│ 3D Izometrik Xarita  │ 4 qavat, 3D avto modellari, jonli taymerlar, quvvat-  │
│                      │ lash stansiyasi, ta'mirlash animatsiyalari, zoom     │
└──────────────────────┴──────────────────────────────────────────────────────┘
```

---

## ⚠️ 4. Xatarlar Reestri va Boshqaruvi (Risk Register & Scope)

Loyihaning muvaffaqiyatiga ta'sir qiluvchi xatarlar, ularning bahosi va yumshatish choralari:

| Risk ID | Xatar Nomi va Tavsifi | Ehtimollik (1-5) | Ta'sir (1-5) | Daraja (L x I) | Yumshatish Chorasi (Mitigation Strategy) | Favqulodda Reja (Contingency Plan) | Mas'ul |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| **RSK-01** | **Kirish/chiqishda tirbandlik va kutish vaqti 10 daqiqadan oshishi** | 3 | 5 | **15 (YUQORI)** | Kadr tezligini <150ms ushlash; 5m da sariq, 7m da qizil signal berish. | 10 minutda avtomatik bir martalik offline-talon berib shlagbaumni ochish (Fail-safe). | Lead Dev / Ops |
| **RSK-02** | **Kamera uzilishi (RTSP oqimi to'xtashi)** | 2 | 5 | **10 (O'RTA)** | Reconnect Watchdog daemon; 5 soniyada javob bo'lmasa avtomatik qayta ulanish. | Zaxira kameraga ulanish yoki operator qo'lda kiritish rejimiga o'tishi. | Vision Lead |
| **RSK-03** | **Noaniq raqamlar (loyqa, qorongi, qiyshiq burchak)** | 4 | 3 | **12 (YUQORI)** | Adaptive CLAHE + Homography Warp; 3 kadrli Temporal Voting o'rnatish. | Ishonchlilik <85% bo'lsa operator monitoriga 15 soniyada qo'lda tasdiqlash uchun yuborish. | AI Dev |
| **RSK-04** | **Onlayn to'lov agregatorlari (Click/Payme) uzilishi** | 3 | 4 | **12 (YUQORI)** | Timeout 3 soniya; no-automation (Naqd/POS) to'lov muqobilini doim tayyor tutish. | Chiqishda 10 min qolib ketmaslik uchun avto raqamiga biriktirilgan Post-Pay elektron qarz taloni berish. | Backend Dev |
| **RSK-05** | **Elektr ta'minoti uzilishi (Blackout)** | 1 | 5 | **5 (PAST)** | Shlagbaum va serverga UPS (Uzluksiz quvvat manbai) o'rnatish talabi. | Mexanik kalit orqali shlagbaumni doimiy ochiq holatga keltirish. | Hardware Dev |
| **RSK-06** | **Ruxsatsiz tarif yoki sozlamalar o'zgartirilishi** | 2 | 4 | **8 (O'RTA)** | RBAC qat'iy cheklovi: faqat 2 ta Super-Admin o'zgartirishi mumkin, DB darajasida guard. | Xodimlar va sozlamalarni oddiy adminlar uchun qulflash (🔒). | Security Lead |

---

## 🏛️ 5. Qayta Yozilgan Rasmiy Epiklar (Epic Rewrite)

---

### 🏛️ EPIC 1: Loyiha Boshqaruvi, Xatarlar va Sifat Standartlari
* **Maqsad:** Loyihani 10 minutlik SLA, risklar reestri va sifat mezonlari asosida Scrum qoidalarida boshqarish.
* **Stories:** US-PM-01 (Loyiha xartiyasi va xatarlar), US-PM-02 (Taskcafe Kanban va SLA monitoringi).

---

### 💻 EPIC 2: Tizim Arxitekturasi va C/C++ Hardware Integratsiyasi
* **Maqsad:** Yuqori unumdorlikka ega mikro-monolit arxitektura, C/C++ simulyatori va PostgreSQL/SQLite bazasini yaratish.
* **Stories:** US-ARC-01 (C4 arxitektura va ERD), US-ARC-02 (C/C++ Simulyatori va datchiklar oqimi).

---

### 🛡️ EPIC 3: RBAC Huquqlar Matritsasi va Xavfsizlik (2 Super, 4 Oddiy Admin)
* **Maqsad:** Tizimda xavfsizlik va mas'uliyatni ajratish: 2 Super-Admin, 4 Oddiy Admin va 2 Operator rollari.
* **Stories:** US-SEC-01 (Huquqlar matritsasi va menyular qulfi), US-SEC-02 (Xodimlarni boshqarish va audit jurnali).

---

### 📷 EPIC 4: Computer Vision, ANPR va Kameralar Mantiqi
* **Maqsad:** RTSP kameralaridan real-vaqtda kadr qabul qilish, shovqinlarni tozalash, O'zbekiston davlat raqamlarini o'qish va ko'p kadrli konsensus orqali `>= 85%` aniqlikka erishish.
* **Stories:** US-CAM-01 (Kamera oqimi va CLAHE yorug'lik filtri), US-CAM-02 (Two-Stage detektor, Homography warp va OCR chalkashliklarini tuzatish).

---

### ⏱️ EPIC 5: 10 Daqiqa Maksimal Kutish SLA'si va Shlagbaum Nazorati
* **Maqsad:** Haydovchi kirish yoki chiqish darvozasida hech qachon 10 daqiqadan ortiq kutmasligini ta'minlash (Watchdog va Fail-Safe).
* **Stories:** US-SLA-01 (10 minutlik kutish SLA taymeri va eskalatsiyasi), US-SLA-02 (Favqulodda shlagbaumni avtomatik ochish).

---

### 🚗 EPIC 6: Bo'sh Joylarni Aqlli Aniqlash va 3D Izometrik Xarita
* **Maqsad:** Kirgan transport turiga mos ravishda (Standart, Elektromobil, VIP) eng kam masofadagi bo'sh slotni tanlash va 3D xaritada ko'rsatish.
* **Stories:** US-MAP-01 (Spot Allocator joy tanlash algoritmi), US-MAP-02 (4 qavatli 3D Izometrik xarita va avto modellari).

---

### 📅 EPIC 7: Joy Band Qilish (Booking) va To'qnashuvlarni Oldini Olish
* **Maqsad:** Haydovchilar tomonidan joyni oldindan bron qilish va vaqt kesishuvlarini (Overlap Conflict) 100% bartaraf etish.
* **Stories:** US-RES-01 (Reservation Matcher vaqtlarni solishtirish), US-RES-02 (Muddati o'tgan bronlarni avto-bo'shatish).

---

### 💳 EPIC 8: To'lov Tizimlari (Click/Payme va Naqd/POS Qo'lda To'lov)
* **Maqsad:** Avtomatlashtirilgan onlayn to'lovlarni (Payme/Click) hamda avtomatlashtirilmagan naqd pul va POS-terminal orqali qo'lda to'lovlarni to'liq qamrab olish.
* **Stories:** US-PAY-01 (15 min bepul muddat va Click/Payme integratsiyasi), US-PAY-02 (Naqd/POS to'lovlarini operator tomonidan qo'lda tasdiqlash va offline qarz taloni).

---

### 🖥️ EPIC 9: Desktop Admin Paneli va 4-Moliya Moduli
* **Maqsad:** Minimalist dizayndagi zamonaviy boshqaruv paneli, aynan 4-o'rindagi Moliya moduli, 7 kunlik bar chart va Excel UTF-8 BOM eksporti.
* **Stories:** US-UI-01 (Figma/Dribbble minimalist interfeysi va 7 ta modul), US-UI-02 (4-Moliya tushumlar hisoboti, haftalik chart va tariflar modali).

---

### 🛡️ EPIC 10: Sifat Nazorati (QA), E2E Testlar va Yakuniy Reliz
* **Maqsad:** Barcha modullarni 100% avtotestlar bilan qoplash (pytest/unittest - 20/20 yashil) va xatosiz ishlab chiqarishga chiqarish.
* **Stories:** US-QA-01 (Algoritmlar, Vision va SLA testlari), US-QA-02 (DoD tekshiruvi va reliz packaging).

---

## 📝 6. To'liq Agile User Story'lar va Qabul Qilish Mezonlari (Acceptance Criteria)

---

### 🚗 US-01: Kirish Shlagbaumida Avtomatik ANPR va 10 Daqiqa Max Kutish Kafolati
* **Kod:** `US-01` | **Prioritet:** `P0 (Critical Blocker)` | **SP:** `8` | **Mas'ul:** AI Lead & Backend Dev

#### User Story:
> **Haydovchi sifatida,**  
> men avtoturargoh kirish postiga kelganimda davlat raqamim kamera orqali soniyalar ichida aniqlanishini, optimal bo'sh slot ko'rsatilib shlagbaum ochilishini xohlayman,  
> **toki** men va orqamdagi transportlar tirbandlikda va navbatda **maksimal 10 daqiqadan ko'p kutib qolmasin**.

#### 📋 Acceptance Criteria (GIVEN / WHEN / THEN):
- [ ] **AC-01.1 (Tezlik va Aniqlash):**
  - **Given:** Avtomobil kirish shlagbaumining ko'rish maydoniga kirdi.
  - **When:** Kamera kadrlarni ANPR quvuriga yuboradi.
  - **Then:** Tizim 150 ms dan kam vaqtda davlat raqamini aniqlaydi va bazada sessiyani ochadi.
- [ ] **AC-01.2 (⏱️ Qat'iy 10 Daqiqalik Kutish SLA Qoidasi):**
  - `0 – 15 soniya:` Raqam `>= 85%` ishonchlilik bilan o'qiladi, shlagbaum ochiladi.
  - `15 soniya – 3 daqiqa:` Raqam loyqa bo'lsa, navbat operator monitoriga "Qo'lda tekshirish"ga tushadi.
  - `5 daqiqa (Sariq Ogohlantirish):` Postda kutish 5 daqiqadan oshsa, operator panelida sariq taymer miltillaydi.
  - `7 daqiqa (Qizil Xavf):` Super-Admin panelida shoshilinch signal chalinadi va eskalatsiya qilinadi.
  - `10 daqiqa (Kafolatlangan Fail-Safe):` Tizim avtomobilni postda **10 daqiqadan ortiq ushlab turishga mutlaqo yo'l qo'ymaydi**. 10 daqiqa to'lganda shlagbaum avtomatik ravishda bir martalik vaqtinchalik offline-talon bilan ochiladi va hodisa `CRITICAL_SLA_BREACH` audit jurnaliga yoziladi.
- [ ] **AC-01.3 (Real-Vaqtda Ma'lumot Yangilanishi):**
  - Shlagbaum ochilishi bilan 3D xaritada avto modeli paydo bo'ladi, sloti `OCCUPIED` bo'ladi va dashboarddagi bo'sh joylar soni darhol -1 ga kamayadi.

---

### 🅿️ US-02: Parkovkada Bo'sh Joyni Aqlli Aniqlash (Spot Allocation)
* **Kod:** `US-02` | **Prioritet:** `P1 (Must Have)` | **SP:** `5` | **Mas'ul:** Algoritm Muhandisi

#### User Story:
> **Haydovchi sifatida,**  
> men avtoturargohga kirganimda tizim menga avtomobilim turiga mos (elektromobil bo'lsa quvvatlash stansiyasi bor, oddiy bo'lsa standart) va kirish darvozasiga eng yaqin bo'sh joyni avtomatik ajratib berishini xohlayman,  
> **toki** men qavatlar oralab bo'sh joy qidirib 10 daqiqadan ortiq vaqt yo'qotmay.

#### 📋 Acceptance Criteria:
- [ ] **AC-02.1 (Transport Turiga Moslik):**
  - Elektromobil kelganda: birinchi navbatda `EV_CHARGING` slot ajratiladi.
  - Standart yengil avto kelganda: `REGULAR` slot ajratiladi (`EV` yoki `VIP` berilmaydi).
  - VIP/Xodim kelganda: `VIP_STAFF` sloti ajratiladi.
- [ ] **AC-02.2 (Evristik Masofa va Qavat Xarajati):**
  - `Cost = sqrt((slot.x - gate.x)^2 + (slot.y - gate.y)^2) + 200.0 * abs(target_floor - current_floor)`.
  - Eng kam xarajatga ega bo'lgan joy birinchi bo'lib tanlanadi.
- [ ] **AC-02.3 (Tabloda Ko'rsatish):**
  - Tanlangan slot raqami (`Slot: A-101`) darhol kirish tablosida va haydovchi kvitansiyasida aks etadi.

---

### 💵 US-03: Avtomatlashtirilmagan (Naqd / POS-terminal) To'lovlar va 10 Minutlik Chiqish Himoyasi
* **Kod:** `US-03` | **Prioritet:** `P1 (Must Have)` | **SP:** `5` | **Mas'ul:** Backend & Finance Dev

#### User Story:
> **Haydovchi va kassa operatori sifatida,**  
> men onlayn to'lov ilovasi bo'lmaganda yoki bank serveri ishlamay qolganda naqd pul yoki bank kartasi (POS) orqali to'lovni operatorga topshirishni va darhol chiqib ketishni xohlayman,  
> **toki** to'lov muammolari sababli chiqish darvozasida 10 daqiqadan ortiq ushlanib qolmay.

#### 📋 Acceptance Criteria:
- [ ] **AC-03.1 (15 Daqiqalik Bepul Muddat va Chiqish Imtiyozi):**
  - Dastlabki 15 daqiqada kirib-chiqqan transport to'lovsiz chiqariladi (`amount_due = 0`).
  - To'lov amalga oshirilgach, chiqib ketish uchun 15 daqiqalik bepul chiqish darchasi beriladi.
- [ ] **AC-03.2 (Avtomatlashtirilmagan / Qo'lda To'lov):**
  - Operator monitorida "Naqd pul qabul qilindi" yoki "POS-terminal orqali to'landi" tugmasi bosilganda sessiya `PAID` holatiga o'tadi, fiskal kvitansiya raqami generatsiya qilinadi va shlagbaum ochiladi.
- [ ] **AC-03.3 (To'lov Tizimi Uzilgandagi 10 Daqiqa Fallback):**
  - Agar bank tizimi yoki internet uzilsa va haydovchi chiqishda **7 daqiqadan ko'p kutsa**, operator ekranida "Keyinchalik to'lash kafolati" paydo bo'ladi.
  - **10 daqiqa to'lganda:** Shlagbaum avtomatik ravishda ochiladi, avto raqamiga elektron qarz taloni yoziladi; haydovchi hech qachon 10 daqiqadan ko'p ushlab turilmaydi.
- [ ] **AC-03.4 (Chiqishda Real-Vaqt Yangilanishi):**
  - Shlagbaum ochilib mashina chiqishi bilan slot holati darhol `FREE` bo'ladi, 3D xaritadan avto modeli o'chiriladi, kassa tushumiga to'lov summasi qo'shiladi.

---

### 🛡️ US-04: RBAC Huquqlar Matritsasi va Xavfsizlik Nazorati
* **Kod:** `US-04` | **Prioritet:** `P1 (Must Have)` | **SP:** `5` | **Mas'ul:** Security & Desktop Dev

#### User Story:
> **Bosh rahbar (Super-Admin) sifatida,**  
> men operatsion xodimlar faqat o'zlariga tegishli monitoring sahifalarini ko'rishini, tariflar va tizim sozlamalariga teginolmasligini xohlayman,  
> **toki** inson omili sababli moliyaviy va texnik konfiguratsiyalar buzilmasin.

#### 📋 Acceptance Criteria:
- [ ] **AC-04.1 (Super-Admin - 2 kishi):**
  - Barcha 7 ta modulga to'liq kirish, tariflarni yangilash, adminlarni boshqarish va shlagbaumni favqulodda ochish huquqi.
- [ ] **AC-04.2 (Oddiy Admin - 4 kishi):**
  - Monitoring, 3D xarita, ANPR va 4-Moliya bo'limini ko'rish va Excel yuklab olish huquqi.
  - ❌ **Taqiqlangan:** Tariflarni tahrirlash, 6-Xodimlar va 7-Sozlamalar bo'limlariga kirish (qulflangan 🔒 belgi va ogohlantirish oynasi).
- [ ] **AC-04.3 (Smena Operatori - 2 kishi):**
  - Faqat joriy smena monitoringi, shlagbaumni qo'lda tekshirib ochish (sababini ko'rsatgan holda audit jurnaliga yozish sharti bilan).

---

## 📷 7. Kameralar Mantiqi Texnik Vazifalari (Camera Logic Technical Tasks)

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

| Task ID | Texnik Vazifa Nomi | Qatlam | Tavsifi va Qabul Talabi | SP |
| :---: | :--- | :---: | :--- | :---: |
| **CAM-01** | **Multi-Source Zero-Latency Streamer** | OpenCV / Threading | RTSP va IP kameralardan oqimni bufer to'lib ketishisiz fonda qabul qilish, avtomatik qayta ulanish (Watchdog) | 5 |
| **CAM-02** | **Adaptive CLAHE & Glare Suppression** | OpenCV | Tungi qorong'ilik va avtomobil faralari nurini bartaraf etuvchi dinamik yorug'lik va kontrast filtri | 5 |
| **CAM-03** | **Two-Stage Plate Region Detector** | PyTorch / OpenCV | Avval avtomobil korpusini, so'ngra 4.5:1 proporsiyadagi raqam to'rtburchagini ajratib oluvchi detektor | 8 |
| **CAM-04** | **Homography Perspective Rectification** | OpenCV (Warp) | 30°–45° qiyshiq burchakdagi raqamni to'g'ri to'rtburchak shaklga aylantirish (Homography transform) | 5 |
| **CAM-05** | **Uzbekistan Plate Disambiguation OCR** | Regex / Tesseract | O'zbekiston formati (`01 A 777 AA` va `01 123 AAA`) bo'yicha harf-raqam chalkashliklarini tuzatish (`O`<->`0`, `B`<->`8`, `Z`<->`2`) | 5 |
| **CAM-06** | **Sliding Window Temporal Voting Tracker** | Python DS | 1.5–2.0 soniya ichidagi ketma-ket 3–5 kadr konsensusi asosida ko'pchilik ovozi bilan raqamni tasdiqlash | 5 |
| **CAM-07** | **Confidence Score Decision Engine** | Backend | `>= 85%` bo'lsa shlagbaum avto ochiladi, `< 85%` bo'lsa operator monitoriga snapshot bilan tushadi | 3 |
| **CAM-08** | **10-Minute SLA Watchdog Daemon** | Background Worker | Har bir avtomobilning kamera maydonida turish vaqtini nazorat qiluvchi taymer (5m sariq, 7m qizil, 10m fail-safe) | 5 |
| **CAM-09** | **Desktop ANPR Live Stream & Override** | PyQt6 / C++ Qt | Operator uchun real-vaqt video oynasi, confidence ko'rsatkichi va 1-tugmali qo'lda tasdiqlash dialogi | 5 |
| **CAM-10** | **Offline Camera Fallback & Audit Logger** | SQLite / Postgres | Kamera uzilganda test simulyatsiyasi rejimiga o'tish, shlagbaum harakatlarini audit bazasida qayd etish | 3 |

---

## 📊 8. Taskcafe & GitHub Projects Kanban Preview Scope

Loyihaning Taskcafe doskasi ko'rinishi:

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
│ [P1-HIGH] [5 SP]         │ [P1-HIGH] [5 SP]         │ [P1-CORE] [5 SP]                 │
│ US-03: Naqd / POS Qo'lda │ CAM-09: PyQt6 Desktop    │ SIM-01: Virtual Sensor va Slot   │
│ To'lov & Post-Pay Tiket  │ Live Stream & Override UI│ CLI Simulyatori (UTF-8 Xavfsiz)  │
│ 🏷️ `billing` `sla:10min` │ 🏷️ `desktop-admin` `ui`  │ 🏷️ `simulator` `no-emojis`       │
│ 👤 @dev_backend          │ 👤 @dev_desktop          │ 👤 @erjigitvv5  ✅ Windows OK    │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

## 🏁 9. Definition of Ready (DoR) va Definition of Done (DoD)

### Definition of Ready (DoR):
1. User Story rasmiy formatda yozilgan (`As a... I want... So that...`).
2. Kamida 3 ta aniq va tekshiriluvchi Acceptance Criteria (shu jumladan 10 minutlik kutish SLA'si) ko'rsatilgan.
3. Story Point (SP) bahosi jamoa tomonidan kelishilgan.
4. Bog'liq vazifalar (Dependencies) aniqlangan va to'siqlar yo'q.

### Definition of Done (DoD):
1. Barcha Acceptance Criteria'lar sinovdan o'tgan va tasdiqlangan.
2. Hech bir holatda foydalanuvchining kutish vaqti 10 daqiqadan oshmasligi avtotest bilan tekshirilgan.
3. Unit va integratsion testlar yozilgan (`pytest` va `unittest` 100% yashil).
4. Kod standartlarga mos (PEP8, linter, no-warnings), Git branch `main` ga PR orqali merge qilingan.
5. Hujjatlar (`BACKLOG.md`, `TASKCAFE_BOARD.md`, `README.md`) to'liq yangilangan.
