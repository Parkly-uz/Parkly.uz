# 📚 Parkly.uz — REST API Documentation

> **Versiya:** 2.12.0  
> **Asosiy URL (Base URL):** `http://localhost:8000/api/v1`  
> **Format:** JSON (`Content-Type: application/json`)  
> **Avtorizatsiya:** Bearer Token (JWT) yoki API Key (`X-API-Key`)

---

## 📌 1. System Health & Status

### `GET /`
Tizim holati va versiyasini tekshirish.
* **Javob (200 OK):**
```json
{
  "system": "Parkly.uz Smart Parking API",
  "status": "online",
  "version": "2.12.0",
  "sla_max_wait_minutes": 10.0
}
```

### `GET /health`
Server va ma'lumotlar bazasi sog'lomligini tekshirish.
* **Javob (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-10-21T14:30:00.123456"
}
```

---

## 🚙 2. Gate & ANPR Control (Kirish va Chiqish)

### `POST /api/v1/gate/entry`
Mashina kirish postiga kelganda ANPR orqali o'qilgan raqamni qabul qilish va shlagbaum / slot taqsimlash qarorini qaytarish.
* **Request Body:**
```json
{
  "plate_number": "01A777AA",
  "vehicle_type": "REGULAR",
  "is_staff": false,
  "available_slots": [
    {"slot_number": "A-101", "floor": 1, "zone": "A", "status": "FREE"}
  ]
}
```
* **Javob (200 OK):**
```json
{
  "action": "OPEN_BARRIER",
  "message": "Xush kelibsiz! Slot biriktirildi: A-101",
  "assigned_slot": "A-101",
  "session_id": "SES-1050"
}
```

### `POST /api/v1/gate/exit`
Mashina chiqish postiga kelganda naqd pulsiz (Cashless) to'lov va shlagbaum ochish tekshiruvi. Operator talab etilmaydi.
* **Request Body:**
```json
{
  "plate_number": "01A777AA",
  "session_data": {
    "entry_time": "2026-10-21T13:00:00",
    "duration_minutes": 90,
    "tariff_amount": 15000
  },
  "payment_status": "SUCCESS"
}
```
* **Javob (200 OK):**
```json
{
  "action": "OPEN_BARRIER",
  "message": "To'lov tasdiqlandi. Yo'l bo'sh, xavfsiz qayting!",
  "fiskal_check": "FISC-88215"
}
```

---

## 💳 3. Payment Webhooks (Click, Payme, Uzum Pay)

### `POST /api/v1/payments/webhook`
To'lov tizimlaridan keladigan webhook so'rovlarini qabul qilish va seansni yopish.
* **Request Body:**
```json
{
  "provider": "PAYME",
  "transaction_id": "TX-992145",
  "amount": 15000.0,
  "session_id": "SES-1050",
  "status": "SUCCESS"
}
```
* **Javob (200 OK):**
```json
{
  "status": "OK",
  "message": "To'lov qabul qilindi (PAYME). Seans yopildi.",
  "session_id": "SES-1050"
}
```

---

## 🗺️ 4. Parking Slots & Real-time Monitoring

### `GET /api/v1/slots/status`
Admin Panel va Isometric Xarita uchun barcha slotlarning real vaqtda holatini qaytarish.
* **Javob (200 OK):**
```json
{
  "parking_lot": "Parkly Central — Tashkent City",
  "total_slots": 12,
  "free_slots": 5,
  "occupied_slots": 4,
  "reserved_slots": 2,
  "maintenance_slots": 1,
  "slots": [
    {
      "slot_number": "A-101",
      "floor": 1,
      "zone": "A",
      "status": "FREE",
      "slot_type": "REGULAR",
      "pos_x": 50,
      "pos_y": 50
    }
  ]
}
```

---

## 📅 5. Obunalar va Oylik Tariflar (Subscriptions)

### `POST /api/v1/subscriptions/create`
Haydovchi uchun 1, 3 yoki 6 oylik obuna sotib olish yoki uzaytirish.
* **Request Body:**
```json
{
  "plate_number": "01A777AA",
  "plan_type": "QUARTERLY_PASS",
  "duration_months": 3,
  "amount": 350000.0,
  "provider": "CLICK"
}
```
* **Javob (200 OK):**
```json
{
  "status": "SUCCESS",
  "subscription_id": "SUB-8812",
  "expires_at": "2027-01-21T00:00:00",
  "message": "3 oylik obuna faollashtirildi!"
}
```
