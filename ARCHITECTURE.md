# 🏛️ Parkly.uz — Smart Parkovka Tizimi Arxitekturasi

Ushbu hujjat **Parkly.uz** aqlli avtoturargoh tizimining texnik arxitekturasi, ma'lumotlar oqimi va asosiy modullarini tushuntiradi.

---

## 1. Tizimning Yuqori Darajadagi Arxitekturasi (High-Level Architecture)

```
       [ 🚗 Avtomobil Kirishi ]
                 │
                 ▼
        [ 📷 ANPR Kamera ] ──────> [ AI Plate Recognition Service ]
                 │                                │
                 ▼                                ▼
       [ 🚪 Shlagbaum / Barrier ] <─── [ Core Parking Engine (API) ]
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 │                                │                                │
                 ▼                                ▼                                ▼
       [ 📱 Mobile App ]               [ 🖥️ Admin Dashboard ]            [ 💳 Payment Gateway ]
     (Bron, Navigatsiya, QR)           (Monitoring, Analitika)             (Payme, Click, Uzum)
```

---

## 2. Asosiy Modullar (Core Modules)

### A. Hardware & Edge Layer (IoT & Kompyuter Ko'rishi)
- **ANPR (Automatic Number Plate Recognition):** Kirish va chiqish yo'laklariga o'rnatilgan IP kameralar RTSP video oqimini uzatadi.
- **Plate Detection Engine:** Python (YOLOv8/v11 + OCR) yordamida O'zbekiston davlat raqamlarini (01 A 777 AA, 10 123 AAA va boshqalar) millisekundlarda taniydi.
- **Barrier Controller:** Mikrokontroller (ESP32 / Raspberry Pi / Modbus relay) orqali shlagbaumga avtomatik signal yuboriladi (Open / Close).
- **Slot Sensors:** Ultratovushli yoki magnetik datchiklar har bir bo'sh/band joy holatini MQTT orqali markaziy serverga yuboradi.

### B. Core Backend API
- **Session Manager:** Mashina kirgan vaqtdan to chiqib ketguncha bo'lgan seansni yuritadi (Kirish vaqti, slot raqami, mashina raqami, surat).
- **Tariff & Billing Engine:** Dinamik tariflar (birinchi 15 daqiqa bepul, soatlik to'lov, tunlik stavka, VIP zonalar).
- **Reservation (Booking) Service:** Foydalanuvchiga ma'lum vaqt oralig'ida bo'sh joyni oldindan band qilish imkoniyati.
- **Notification Service:** Telegram Bot / SMS / Push xabarnomalar (Masalan: "Sizning parkovka vaqtingiz tugashiga 10 daqiqa qoldi").

### C. To'lov tizimlari integratsiyasi
- **Payme, Click, Uzum Pay API:**
  - Avtomatlashtirilgan to'lov tekshiruvi (Fiscal chek bilan).
  - Chiqish shlagbaumi oldida QR-kod skaner qilib to'lash yoki ilova ichida avto-to'lov.

### D. Foydalanuvchi va Boshqaruv Interfeyslari
- **Mobile Client (Flutter):** Haydovchilar uchun iOS & Android ilovasi.
- **Web Admin Panel (Next.js):** Operatorlar, moliya bo'limi va boshqaruvchilar uchun qulay boshqaruv paneli.

---

## 3. Ma'lumotlar Bazasi Modeli (ERD Asosiy Jadvalari)

1. `users` — Foydalanuvchilar (id, phone, name, role)
2. `vehicles` — Avtomobillar (id, user_id, plate_number, model, color)
3. `parking_lots` — Avtoturargohlar (id, name, address, latitude, longitude, total_spots)
4. `parking_spots` — Alohida parkovka joylari (id, parking_lot_id, spot_number, status: free/occupied/reserved, sensor_id)
5. `parking_sessions` — Kirish-chiqish seanslari (id, vehicle_id, parking_lot_id, entry_time, exit_time, status, total_amount)
6. `transactions` — To'lovlar (id, session_id, payment_provider, amount, status, transaction_id)
