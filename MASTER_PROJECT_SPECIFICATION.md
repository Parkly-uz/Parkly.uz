# 🚗 Parkly.uz — Master Project Specification & Architecture Baseline

> **Hujjat maqomi:** Rasmiy Master Spetsifikatsiya (Production Baseline)  
> **Loyiha nomi:** Parkly.uz — Next-Gen Unattended Smart Parking System  
> **Versiya:** 2.0 (Operatorsiz, Naqd pulsiz, 10 daqiqalik Fail-Safe SLA)

---

## 📑 MUNDARIJA
1. [Muammoning Qayta Tahlili (Problem Statement & Core Value)](#1-muammoning-qayta-tahlili)
2. [Backlog Prioritetlari Matritsasi (P0, P1, P2 Prioritization)](#2-backlog-prioritetlari-matritsasi)
3. [Tariflar Modeli va Hisob-kitob Qoidalari (Pricing & Tariffs)](#3-tariflar-modeli-va-hisob-kitob-qoidalari)
4. [To'liq Project Scope va Tizim Chegaralari](#4-toliq-project-scope-va-tizim-chegaralari)
5. [Kirish/Chiqish va Holat Yangilanishi (Enter/Exit Updating Info State Machine)](#5-kirishchiqish-va-holat-yangilanishi)
6. [Foydalanuvchi Akkauntlari va Rollar Matritsasi (RBAC & Accounts)](#6-foydalanuvchi-akkauntlari-va-rollar-matritsasi)
7. [Risk Scope va Xatarlar Xaritasi](#7-risk-scope-va-xatarlar-xaritasi)
8. [OpenAPI 3.1 Dokumentatsiyasi (Enter / Exit / Telemetry Updates)](#8-openapi-31-dokumentatsiyasi)
9. [Katta Epiklar (Epics Definition)](#9-katta-epiklar-epics-definition)

---

## 1. Muammoning Qayta Tahlili

### 1.1 An'anaviy Parkovkalardagi 5 Ta Kritik Muammo:
1. **Inson omili va Sekinlik:** Qorovul/kassir tomonidan talon berish yoki to'lov olish har bir mashina uchun 45–90 soniya vaqt oladi. Bu esa tirbandlikka sabab bo'ladi.
2. **Ob-havo va Xiralik:** Yomg'ir, tuman yoki qorong'ida arzon kameralar davlat raqamini o'qiy olmaydi, natijada post to'xtab qoladi.
3. **Naqd puldagi noaniqlik va O'g'rilik:** Naqd pulli tizimlarda tushumning 15–20% qismi hisobotlarga kirmay qoladi (qog'oz talonlar yo'qolishi yoki operator firibgarligi).
4. **Ichkarida Sarson Bo'lish:** Haydovchi kirgach, qayerda bo'sh joy borligini bilmaydi va 10–15 daqiqa joy qidirib behuda yoqilg'i sarflaydi.
5. **Texnik To'xtalish (Deadlock):** Bank tizimi yoki internet uzilganda shlagbaum yopilib qolib, o'nlab avtomobillar 30–40 daqiqa tiqilib qoladi.

### 1.2 Parkly.uz Yechimi:
To'liq **operatorsiz (Unattended)**, **naqd pulsiz (Cashless)**, har qanday ob-havoda kadrni sun'iy tiniqlashtiruvchi (**Adversarial Weather CV**), optimal bo'sh joyni ko'rsatuvchi (**A* Routing**) va internet o'chsa ham haydovchini 10 daqiqadan ortiq ushlamay avtomatik qarzga chiqarib yuboruvchi (**Fail-Safe 10-Min SLA**) yagona aqlli ekotizim.

---

## 2. Backlog Prioritetlari Matritsasi

| Prioritet | Qatlam | Ma'nosi va SLA | Bajariladigan Vazifalar |
| :---: | :---: | :--- | :--- |
| 🔴 **P0** | **Blocker / Core** | Tizim ishlashi uchun hayotiy zarur. Birinchi sprintda yakunlanishi shart. | • Ob-havo filtrlari (CLAHE/Defogger)<br>• O'zbekiston ANPR + Avto modeli (YOLOv8/11)<br>• 10 daqiqalik shlagbaum SLA taymeri<br>• Enter/Exit tranzaksiya holatlari mashinasi<br>• Dinamik QR-to'lov (Payme/Click) |
| 🟡 **P1** | **High / Feature** | Tizimning to'laqonli samaradorligi va avtonomligi uchun zarur. | • A* Bo'sh joy tavsiya qilish algoritmi<br>• Datchik va Kamera ziddiyatini tekshirish (Conflict)<br>• Offline Qarz Reestri va Internet Sync<br>• 3D Izometrik monitoring xaritasi (PyQt6) |
| 🟢 **P2** | **Medium / Polish** | Xavfsizlik, shaffoflik va audit loglari. | • Qora quti audit jurnali (Suratli saqlash)<br>• Kunlik/oylik moliya hisoboti (Excel/CSV)<br>• LED Informatsion tablo integratsiyasi |

---

## 3. Tariflar Modeli va Hisob-kitob Qoidalari

Parkly.uz tizimida adolatli va shaffof 4 xil tarif rejimi joriy etilgan:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PARKLY.UZ TARIFLAR TIZIMI                       │
├─────────────────────┬──────────────────┬───────────────────────────────┤
│ Tarif Nomi          │ Stavka (so'm)    │ Qo'llanish Qoidasi            │
├─────────────────────┼──────────────────┼───────────────────────────────┤
│ 🆓 Bepul Interval   │ 0 so'm           │ Dastlabki 15 daqiqa (Grace)   │
│ 🚗 Standart Soatlik │ 5,000 so'm/soat  │ Kunduzgi (08:00 - 20:00)      │
│ 🌙 Tungi Soatlik    │ 3,000 so'm/soat  │ Tungi (20:00 - 08:00)         │
│ 🔥 Tig'iz Vaqt (Peak)│ 8,000 so'm/soat │ To'lalik darajasi > 85% bo'lsa│
│ 👑 Kunlik Fiksirlangan│ 40,000 so'm/kun│ 24 soatlik to'xtash           │
│ 🛡️ No-Automation Qarz│ Asl summa + SMS │ Internet o'chganda qarzga     │
└─────────────────────┴──────────────────┴───────────────────────────────┘
```

### Hisoblash Formulasi:
$$TotalFee = \begin{cases} 
0, & \text{agar } t \le 15 \text{ min} \\
\lceil \frac{t}{60} \rceil \times Rate, & \text{agar } t > 15 \text{ min}
\end{cases}$$

---

## 4. To'liq Project Scope va Tizim Chegaralari

### 4.1 Scope In (Loyiha ichidagi vazifalar):
- **Universal Edge Vision:** RTSP, IP, ONVIF va USB kameralardan kadr olib, yomg'ir, tuman, qor va qorong'ilikda kontrastni 40% ga oshirish va raqamni $\ge 95\%$ aniqlikda o'qish.
- **Smart Slot Routing:** Kirgan mashina o'lchamiga mos eng yaqin bo'sh joyni 1 soniyada xaritada topish va kirish tablosida ko'rsatish.
- **Cashless Kiosk & Deferred Debt:** Chiqishda dinamik QR kod orqali to'lov; internet o'chganda avtomatik qarz reestriga yozib, shlagbaumni ochish.
- **10-Minute SLA Engine:** Har qanday postda 10:00 daqiqa to'xtab qolish holatida shlagbaumni favqulodda majburiy ochish (Fail-Safe Open).
- **Desktop & Web Admin UI:** 3D Izometrik xarita, real-vaqt telemetriyasi, kassa/moliya analitikasi.

### 4.2 Scope Out (Loyiha tarkibiga kirmaydiganlar):
- Shlagbaum mikrosxemalarini jismoniy lehimlash/ishlab chiqarish (faqat mavjud standart RS-485 kontrollerlariga buyruq beriladi).
- Yoqilg'i quyish yoki elektromobillarni quvvatlash stansiyalarini to'g'ridan-to'g'ri boshqarish.

---

## 5. Kirish/Chiqish va Holat Yangilanishi (Enter/Exit Updating Info)

Avtomobilning parkovkadagi har bir qadami aniq **Holatlar Mashinasi (State Machine)** orqali boshqariladi:

```
[APPROACHING_GATE] ──> Kamera aniqladi ──> [PLATE_RECOGNIZED]
                                                    │
                                                    ▼
[BARRIER_OPENED_ENTRY] <── Joy tayinlandi <── [SLOT_ALLOCATED]
         │
         ▼
[PARKED_OCCUPIED] <── Datchik tasdiqladi (Vaqt hisobi ketmoqda)
         │
         ▼
[APPROACHING_EXIT] ──> Chiqish kamerasi ──> [FEE_CALCULATED]
                                                    │
                   ┌────────────────────────────────┴──────────────────┐
                   ▼                                                   ▼
       [PAYMENT_SUCCESS_ONLINE]                            [NO_AUTOMATION_DEFERRED_DEBT]
         (Payme / Click QR)                                 (Internet o'chgan / SLA 10 min)
                   │                                                   │
                   └────────────────┬──────────────────────────────────┘
                                    ▼
                         [BARRIER_OPENED_EXIT]
                                    │
                                    ▼
                          [SESSION_COMPLETED]
```

### Real-Time Updating Info Parametrlari:
Har bir holat o'zgarganda WebSocket orqali operator ekrani va markaziy serverga quyidagi JSON paket yuboriladi:
- `session_id`: Unikal sessiya raqami
- `vehicle_plate`: Davlat raqami
- `current_status`: Joriy status
- `allocated_slot`: Tayinlangan katak (masalan: `B-14`)
- `elapsed_time_sec`: Parkovkada turgan vaqti (soniyalarda)
- `current_fee`: Joriy hisoblangan to'lov
- `sla_wait_seconds`: Postda turib qolgan vaqti (SLA taymeri)

---

## 6. Foydalanuvchi Akkauntlari va Rollar Matritsasi (RBAC & Accounts)

Tizimda xavfsizlik va mas'uliyatni ajratish maqsadida 8 ta aniq akkaunt va 3 xil rol biriktirilgan:

| Akkaunt Logini | To'liq Ismi | Biriktirilgan Rol | Ruxsatlar va Cheklovlar |
| :--- | :--- | :---: | :--- |
| **`admin`** | Erjigit (Bosh Rahbar) | **Super-Admin** | Barcha 7 ta bo'limga to'liq kirish, tariflarni o'zgartirish, favqulodda shlagbaumni ochish, audit loglarini ko'rish. |
| **`superadmin2`** | Sherzod Aliyev (Arxitektor) | **Super-Admin** | Tizim konfiguratsiyasi, kamera drayverlari, API kalitlar va to'liq boshqaruv. |
| **`admin_yunusobod`** | Jahongir Qodirov | **Admin** | Yunusobod filiali telemetriyasi, 3D xarita, moliya hisobotlarini ko'rish va yuklab olish. (Sozlamalar qulflangan 🔒). |
| **`admin_chilonzor`** | Aziz Rustamov | **Admin** | Chilonzor filiali monitoringi, tushumlar tahlili. |
| **`admin_mirobod`** | Bobur Mirzayev | **Admin** | Mirobod filiali monitoringi, datchiklar holati. |
| **`admin_sergeli`** | Dilshod Karimov | **Admin** | Sergeli filiali monitoringi, sessiyalar nazorati. |
| **`operator1`** | Farrux Yusupov | **Smena Nazoratchisi** | Real-vaqt kameralar oqimi, SLA ogohlantirishlarini kuzatish. Tarif va sozlamalarga kirish taqiqlangan ❌. |
| **`operator2`** | G'ayrat Xoliqov | **Smena Nazoratchisi** | Tungi smena nazorati, favqulodda hodisalar qaydnomasi. |

---

## 7. Risk Scope va Xatarlar Xaritasi

| Risk ID | Xatar Tavsifi | Ehtimollik | Ta'sir | Bartaraf etish rejasi (Mitigation & Fallback) |
| :--- | :--- | :---: | :---: | :--- |
| **RSK-01** | **Kuchli qor/tuman tufayli kamera raqamni o'qiy olmasligi** | Yuqori | Yuqori | CLAHE & Defog filtrlari ishga tushadi. Agar Confidence < 75% bo'lsa, terminal 2 soniyada avtomatik offline QR-talon chop etadi. |
| **RSK-02** | **Chiqish postida tirbandlik va kutish vaqti > 10 daqiqa** | O'rta | Yuqori | 5-minutda sariq ogohlantirish, 7-minutda qizil signal, 10-minutda shlagbaum avtomatik majburiy ochilib, qarzga chiqariladi. |
| **RSK-03** | **To'liq Internet va Markaziy Server uzilishi** | O'rta | O'ta Yuqori | Post avtomatik lokal SQLite rejimiga o'tadi. Barcha chiqishlar offline qarzga yozilib, internet kelgach sinxronlanadi. |
| **RSK-04** | **Datchik va Kamera ma'lumoti ziddiyati (Sensor Conflict)** | Yuqori | O'rta | Datchik "bo'sh", kamera "band" desa, katak "CONFLICT" statusini oladi va yangi mashinalarga tavsiya etilmaydi. |
| **RSK-05** | **Elektr ta'minoti uzilishi (Blackout)** | Past | Kritik | 24V UPS zaxira akkumulyatorlari; tok to'liq o'chganda shlagbaum avtomatik ravishda ochiq holatga keladi (Fail-Safe Open). |

---

## 8. OpenAPI 3.1 Dokumentatsiyasi

```yaml
openapi: 3.1.0
info:
  title: Parkly.uz Enter/Exit & Telemetry Engine API
  version: 2.0.0
  description: Real-time ANPR, Slot Allocation, Cashless Payments and State Updating API.
paths:
  /api/v1/gate/enter:
    post:
      summary: Avtomobil kirishini qayd etish va bo'sh joy tayinlash
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [gate_id, plate_number]
              properties:
                gate_id:
                  type: string
                  example: "GATE_IN_01"
                plate_number:
                  type: string
                  example: "01A777AA"
                vehicle_model:
                  type: string
                  example: "Chevrolet Cobalt"
                confidence:
                  type: number
                  example: 0.985
      responses:
        '200':
          description: Kirish tasdiqlandi, shlagbaum ochildi
          content:
            application/json:
              schema:
                type: object
                properties:
                  session_id:
                    type: string
                    example: "SES-20261015-001"
                  barrier_command:
                    type: string
                    example: "OPEN"
                  allocated_slot:
                    type: string
                    example: "B-14"
                  enter_time:
                    type: string
                    format: date-time

  /api/v1/gate/exit:
    post:
      summary: Chiqishda to'lov hisoblash va holatni yangilash
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [gate_id, plate_number]
              properties:
                gate_id:
                  type: string
                  example: "GATE_OUT_01"
                plate_number:
                  type: string
                  example: "01A777AA"
      responses:
        '200':
          description: Chiqish hisob-kitobi
          content:
            application/json:
              schema:
                type: object
                properties:
                  session_id:
                    type: string
                    example: "SES-20261015-001"
                  duration_minutes:
                    type: integer
                    example: 65
                  total_fee:
                    type: number
                    example: 10000.0
                  qr_payment_url:
                    type: string
                    example: "https://pay.parkly.uz/payme/SES-001"
                  sla_timer_started:
                    type: boolean
                    example: true

  /api/v1/telemetry/slots-update:
    get:
      summary: Real-time bo'sh joylar va ziddiyatlar holati
      responses:
        '200':
          description: Xarita telemetriyasi
          content:
            application/json:
              schema:
                type: object
                properties:
                  total_capacity:
                    type: integer
                    example: 150
                  free_slots:
                    type: integer
                    example: 42
                  occupied_slots:
                    type: integer
                    example: 106
                  conflicted_slots:
                    type: integer
                    example: 2
```

---

## 9. Katta Epiklar (Epics Definition)

- **EPIC-01: Universal Vision & Ob-havo Filtrlash Tizimi** — RTSP/ONVIF oqimlarida CLAHE/Defogger va YOLOv8/11 ANPR.
- **EPIC-02: Aqlli Marshrutlash va Bo'sh Joylarni Boshqarish** — A* algoritmi, datchik-kamera ziddiyatlarini bartaraf etish.
- **EPIC-03: 100% Naqd pulsiz Dinamik QR To'lov Kioski** — Payme/Click integratsiyasi, ekranda QR generatsiya qilish.
- **EPIC-04: No-Automation Offline Qarz Reestri va Fail-Safe** — Internet o'chganda avtomobilni to'xtovsiz qarzga chiqarish.
- **EPIC-05: 10 Daqiqalik Qat'iy SLA Watchdog Servisi** — 5 min (sariq), 7 min (qizil), 10 min (majburiy ochilish).
- **EPIC-06: 3D Izometrik Admin Dashboard va RBAC Xavfsizlik** — Rollar bo'yicha cheklangan yuqori unumdor interfeys.
