# 🏗️ Parkly.uz — Backend Architecture, Algorithms & Session Management

> **Tizim:** Parkly.uz Aqlli Avtoturargoh Boshqaruv Tizimi  
> **Versiya:** 2.12.0  
> **Arxitektura Turi:** Microservices-Ready Modular Monolith (FastAPI + PostgreSQL + Redis + C++/Qt Desktop Admin)

---

## 🏛️ 1. Backend Arxitektura Umumiy Tuzilishi (High-Level Architecture)

Parkly.uz backend tizimi asinxron Python (`FastAPI`), ma'lumotlar bazasi (`PostgreSQL`), tezkor kesh va xabar navbati (`Redis`) hamda C++/Qt asosidagi native Desktop Admin Paneldan iborat. Docker to'liq chiqarib yuborilib, to'g'ridan-to'g'ri native muhitda ishga tushirishga moslashtirilgan.

```
┌────────────────────────────────────────────────────────┐
│            C++/Qt Desktop Admin Panel                  │
│  (Hybrid DB: PostgreSQL + Local SQLite Fallback)       │
└────────┬───────────────────────────────┬───────────────┘
         │                               │
         │ REST API / WebSockets         │ Admin Actions & Stats
         ▼                               ▼
┌────────────────────────────────────────────────────────┐
│                     FastAPI Backend                    │
│  ┌──────────────────┐  ┌────────────────────────────┐  │
│  | Gate / ANPR Hook |  | Payment Gateway (Click/Pay)|  │
│  └────────┬─────────┘  └─────────────┬──────────────┘  │
│           │                          │                 │
│           ▼                          ▼                 │
│  ┌──────────────────────────────────────────────┐      │
│  │        Slot Allocator & Tariff Engine        │      │
│  └──────────────────────┬───────────────────────┘      │
└─────────────────────────┼──────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│  PostgreSQL DB   │            │    Redis Cache   │
│ (Persistent Data)│            │ (Real-time Slots)│
└──────────────────┘            └──────────────────┘
```

---

## 🔄 2. Parking Sessiyasi Hayotiy Sikli va Holatlar Mashinasi (Session Lifecycle & State Machine)

Avtomobil kirish va chiqish postidan o'tish jarayonidagi barcha holatlar (`States`) va ularning o'tish qoidalari quyidagi diagrammada keltirilgan:

```
[ IDLE ] ──(ANPR Detected)──► [ ARRIVED ] ──(Slot Assigned)──► [ ACTIVE ]
                                                                   │
                                                   ┌───────────────┴───────────────┐
                                                   ▼                               ▼
                                            [ UNPAID_EXIT ]                [ SUBSCRIPTION_PASS ]
                                                   │                               │
                                                   ▼                               ▼
                                           (Cashless Payment)              (Auto-Validated)
                                                   │                               │
                                                   └───────────────┬───────────────┘
                                                                   ▼
                                                          [ BARRIER_OPENED ]
                                                                   │
                                                                   ▼
                                                            [ COMPLETED ]
```

### Holatlar Tavsifi:
1. **ARRIVED**: Kamera avtomobil davlat raqamini o'qidi (`/api/v1/gate/entry`).
2. **ACTIVE**: Mashinaga eng optimal to'xtash joyi (`slot_number`) biriktirildi va shlagbaum ochildi. Seans boshlandi (`SES-XXXX`).
3. **UNPAID_EXIT**: Mashina chiqish postiga keldi. Vaqt va tarif hisoblandi. Naqd pulsiz to'lov kutilmoqda.
4. **SUBSCRIPTION_PASS**: 1, 3 yoki 6 oylik obunasi bor avtomobillar uchun to'lov talab etilmaydi, darhol shlagbaum ochiladi.
5. **BARRIER_OPENED**: To'lov muvaffaqiyatli tasdiqlandi (yoki obuna mavjud) va shlagbaum ochilish signali yuborildi.
6. **COMPLETED**: Mashina hududni tark etdi, slot holati `FREE` ga o'zgartirildi.

---

## 🧮 3. Slot Taqsimlash Algoritmi (Slot Allocator Algorithm)

Slot taqsimlash moduli (`slot_allocator.py`) haydovchining ehtiyojiga qarab eng yaqin va qulay joyni tanlaydi:
* **VIP xodimlar**: Kirish gate'iga eng yaqin bo'lgan VIP-zona slotlari.
* **Elektromobillar (EV)**: Zaryadlash stansiyasi mavjud maxsus slotlar (`EV-01`, `EV-02`).
* **Oddiy haydovchilar**: Qavatlar bo'yicha eng kam yurish masofasiga ega bo'lgan bo'sh (`FREE`) slotlar.

```python
# Algoritmik mantiq qisqacha:
def allocate_optimal_slot(vehicle_type: str, floor_preference: int = 1):
    available_slots = get_free_slots_from_redis_or_db()
    
    if vehicle_type == "EV":
        ev_slots = [s for s in available_slots if s["slot_type"] == "EV_CHARGER"]
        if ev_slots: return ev_slots[0]
        
    if vehicle_type == "VIP":
        vip_slots = [s for s in available_slots if s["slot_type"] == "VIP"]
        if vip_slots: return vip_slots[0]
        
    # Standard greedy proximity allocation
    regular_slots = [s for s in available_slots if s["floor"] == floor_preference]
    if regular_slots:
        return regular_slots[0] # Birinchi bo'sh slot
    return available_slots[0] if available_slots else None
```

---

## 💳 4. Tarif va Obuna Hisob-Kitob Dvigateli (Tariff & Subscription Engine)

* **Soatlik Tarif**: Kunduzgi (`08:00 - 20:00`) va Tungi (`20:00 - 08:00`) stavkalar.
* **Grace Period**: Kirishdan keyingi dastlabki 15 daqiqa mutlaqo bepul.
* **Daily Cap**: Bir kunlik turish uchun maksimal chegara (masalan, 50,000 UZS).
* **Oylik Tariflar (Subscriptions)**:
  * **1 oylik pass**: 130,000 UZS
  * **3 oylik pass (Quarterly)**: 350,000 UZS (Chegirma bilan)
  * **6 oylik pass (Semiannual)**: 650,000 UZS

---

## ⏱️ 5. 10-Minute SLA Watchdog & Fail-Safe Emergency Protocol

* **SLA Monitoring**: Har bir kirish seansi uchun maksimal 10 daqiqa ichida joylashish va chiqishda 3 daqiqa ichida to'lov amalga oshirilishi kuzatiladi.
* **Fail-Safe Emergency**: Tarmoq uzilishi yoki to'lov tizimi (Click, Payme) javob bermagan favqulodda holatlarda, shlagbaum avtomatik ravishda ochiladi (`Emergency Open Mode`) va hodisa logga yoziladi.

---

## 🌐 6. Cashless Payment Webhook Integratsiyasi

To'lovlar faqat naqd pulsiz (`Click`, `Payme`, `Uzum Pay`) amalga oshiriladi:
1. Mashina chiqish postiga keladi.
2. QR-kod yoki avtomatik raqam tanib olinishi orqali summa chiqariladi.
3. Mijoz mobil ilova orqali to'laydi.
4. Webhook (`/api/v1/payments/webhook`) orqali tasdiq kelgach, shlagbaum ochiladi.
