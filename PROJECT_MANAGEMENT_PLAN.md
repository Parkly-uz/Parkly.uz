# 📊 Parkly.uz — Loyihani Boshqarish Rejasi (Project Management Plan)

> **Loyiha:** Parkly.uz — Smart Parking Management System (Single Large Facility)  
> **Loyiha kodi:** PRK-UZ-2026  
> **Metodologiya:** Agile / Scrum (2 haftalik iteratsiyalar)  
> **Vazifalar Boshqaruvi:** GitHub Projects Kanban Doskasi (`Parkly Project`)  
> **Qat'iy SLA Cheklovi:** Foydalanuvchining maksimal kutish vaqti `≤ 10 daqiqa`  

---

## 1. Boshqaruv Metodologiyasi & Sprint Rejasi (Scrum Framework)

Loyiha qat'iy **2 haftalik iteratsiyalar (Sprintlar)** asosida amalga oshiriladi:

```
┌─────────────────────────┐
│ 1. Sprint Rejalashtirish │ (Har sprint boshida: Dushanba, 10:00)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 2. 14 Kunlik Ish Sikli  │ ──► Har kuni: 15 daqiqalik Daily Standup (10:00)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 3. Sprint Demo (Review) │ (Har sprint oxirida: Juma, 16:00)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 4. Retrospektiva        │ (Demo yakunida: Juma, 17:00)
└────────────┬────────────┘
```

### 4 ta Asosiy Sprint Roadmap:
- **Sprint 1 (1-2 hafta):** Infratuzilma, PostgreSQL/Redis DB (`schema.sql`), Universal Kamera Drayveri (`camera_stream.py`) va Robust ANPR Vizual Filtri (`frame_enhancer.py`, `ocr_engine.py`).
- **Sprint 2 (3-4 hafta):** Spot Allocator, Tariff Calculator (Click, Payme, Uzum Pay & Staff free access), va Gate Controller mantiqi.
- **Sprint 3 (5-6 hafta):** 10-Minut SLA Watchdog, Offline Mode (Lokal kesh va avtomatik sinxronizatsiya) hamda ESP32 IoT / Shlagbaum integratsiyasi.
- **Sprint 4 (7-8 hafta):** Claymorphism Admin Panel, Isometric Parking Map, Profit Analytics va API dokumentatsiya.

---

## 2. Jamoa Rollari va Mas'uliyat Matritsasi (6 ta Rol)

- **R (Responsible):** Vazifani bevosita bajaruvchi mutaxassis
- **A (Accountable):** Natija uchun yakuniy javobgar yagona shaxs
- **C (Consulted):** Maslahat beruvchi ekspert
- **I (Informed):** Jarayon haqida xabardor qilib boriladigan shaxs

| Loyiha Moduli / Jarayon | Product Owner (PO) | Project Manager (PM) | Lead / AI Architect | Backend & Algo | Frontend UI/UX | IoT / Hardware |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Project Charter va Reja** | **A** | R | C | I | I | I |
| **GitHub Backlog & Kanban** | **A** | R | C | C | C | C |
| **Universal Kamera & ANPR** | I | I | **A / R** | C | I | R |
| **Spot Allocator & Tariff** | I | I | A | **R** | I | I |
| **10-Min SLA & Offline Mode**| I | I | A | **R** | C | R |
| **Click, Payme, Uzum Integratsiyasi**| C | I | A | **R** | C | I |
| **ESP32 Shlagbaum & Datchiklar** | I | I | A | C | I | **R** |
| **Claymorphism Admin Panel**| C | I | A | C | **R** | I |
| **Sifat Nazorati va Testlar** | I | I | A | R | R | R |

---

## 3. Sifatni Boshqarish Rejasi va Qat'iy SLA Qoidasi

### A. Kod Sifati Standartlari:
- Python kodi **PEP8** qoidalariga mos va toza bo'lishi shart.
- Frontend (Next.js) kodi TypeScript va Tailwind CSS standartlariga mos yoziladi.
- Asosiy algoritmlar uchun unit testlar (`pytest`) yozilishi shart.

### B. ⏱️ 10 Daqiqalik Maksimal Kutish (SLA Qoidasi - CRITICAL):
- Avtomobil kirish yoki chiqish postida hech qachon **10 daqiqadan ko'p** ushlab turilishi mumkin emas.
- **Bosqichlar:**
  - `0 - 5 min`: Normal rejim (Yashil)
  - `5 - 7 min`: Sariq ogohlantirish (Tizim / Operator xabari)
  - `7 - 10 min`: Qizil favqulodda ogohlantirish (Super-Admin eskalatsiyasi)
  - `>= 10 min`: **FAIL-SAFE EMERGENCY OPEN** (Tizim nosozligida ESP32 orqali shlagbaum avtomatik ochiladi).

### C. Definition of Done (DoD — Ish bitganlik mezoni):
Vazifa faqat quyidagi shartlar bajarilgandagina Kanban doskada **Done** ustuniga o'tkaziladi:
- [ ] Acceptance Criteria talablari 100% bajarilgan.
- [ ] 10 minutlik SLA kutish cheklovi inobatga olingan va tekshirilgan.
- [ ] Barcha testlar xatosiz o'tgan.
- [ ] Kod GitHub'da Pull Request orqali `main` yoki `develop` ga qo'shilgan.
- [ ] Hujjatlar va Backlog yangilangan.
