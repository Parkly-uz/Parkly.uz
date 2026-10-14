# 📊 Parkly.uz — Loyihani Boshqarish Rejasi (Project Management Plan)

> **Loyiha:** Parkly.uz — Smart Parking Management System  
> **Loyiha kodi:** PRK-UZ-2026  
> **Metodologiya:** Agile / Scrum (2 haftalik iteratsiyalar)  
> **Vazifalar Boshqaruvi:** Taskcafe va GitHub Projects Kanban Doskasi  
> **Qat'iy Cheklov:** Foydalanuvchining maksimal kutish vaqti ≤ 10 daqiqa (User Wait Max 10 Min)

---

## 1. Boshqaruv Metodologiyasi (Scrum Framework)

Loyiha qat'iy **2 haftalik iteratsiyalar (Sprintlar)** asosida amalga oshiriladi:

```
┌─────────────────────────┐
│ 1. Sprint Rejalashtirish │ (Har sprint boshida: Dushanba, 10:00 - 11:00)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 2. 14 Kunlik Ish Sikli  │ ──► Har kuni: 15 daqiqalik Daily Standup (10:00)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 3. Sprint Demo (Review) │ (Har sprint oxirida: Juma, 16:00 - 17:00)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 4. Retrospektiva        │ (Demo yakunida: Juma, 17:00 - 17:30)
└─────────────────────────┘
```

### Scrum Marosimlari (Ceremonies):
1. **Sprint Planning:** Product Owner va PM rahbarligida navbatdagi sprint uchun vazifalar (User Stories & Tasks) tanlanadi, Story Point baholanadi va har bir jamoa a'zosiga biriktiriladi.
2. **Daily Standup:** Kunlik 15 daqiqalik tezkor yig'ilish: kechagi natija, bugungi reja va to'siqlar muhokamasi.
3. **Sprint Review (Demo):** Ishlab chiquvchilar tayyor bo'lgan dasturiy qismlarni (API, simulyator, ANPR, Desktop oynasi) Product Ownerga real ishchi holatda ko'rsatadi.
4. **Sprint Retrospective:** Jamoa jarayonini tahlil qilish va takomillashtirish.

---

## 2. Jamoa RACI Mas'uliyat Matritsasi

- **R (Responsible):** Vazifani bevosita bajaruvchi dasturchi
- **A (Accountable):** Natija uchun yakuniy javobgar yagona shaxs
- **C (Consulted):** Maslahat beruvchi mutaxassis
- **I (Informed):** Jarayon haqida xabardor qilib boriladigan shaxs

| Loyiha Moduli / Jarayon | Product Owner (erjigitvv5) | Project Manager | Lead / Senior Dev | Backend Dev | C++ Dev | Desktop Dev | QA Tester |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Project Charter va Maqsadlar** | **A** | R | C | I | I | I | I |
| **Taskcafe & Backlog Boshqaruvi** | **A** | R | C | C | C | C | C |
| **Arxitektura va 4 ta Algoritm** | I | I | **A / R** | R | R | C | C |
| **Computer Vision & ANPR Moduli** | I | I | **A** | C | R | C | R |
| **10-Minutlik Kutish SLA Watchdog**| I | I | **A** | R | R | R | R |
| **PostgreSQL & Core Backend API** | I | I | A | **R** | C | C | I |
| **C/C++ & CLI Sensor Simulyatori**| I | I | A | C | **R** | C | I |
| **Desktop Admin Boshqaruv Paneli**| C | I | A | C | I | **R** | I |
| **4-Moliya va Tranzaksiyalar** | C | I | A | **R** | I | **R** | C |
| **Sifat Nazorati va Sinovlar** | I | I | A | C | C | C | **R** |
| **Yakuniy Reliz va Taqdimot** | **A** | R | R | R | R | R | R |

---

## 3. Kommunikatsiya va Vositalar Rejasi (Communication Plan)

| Kanal / Vosita | Vazifasi va Maqsadi | Ishtirokchilar | Qachon / Qancha vaqtda |
| :--- | :--- | :--- | :--- |
| **Taskcafe & GitHub Projects** | Kanban doskasi (Tasklar, SLA taymerlari, swimlanelar) | Barcha jamoa | Real-vaqtda (har kuni yangilanadi) |
| **Telegram Tech Guruh** | Tezkor texnik savollar, blokirlar va xabarlar | Barcha jamoa | Doimiy (ish vaqti) |
| **GitHub Pull Requests** | Kod tekshiruvi (Code Review) | Lead Dev, Dasturchilar | Har bir yangi kod topshirilganda |
| **Google Meet** | Standup va Rejalashtirish majlislari | Barcha jamoa | Dushanba va Juma (jadval bo'yicha) |

---

## 4. Sifatni Boshqarish Rejasi va Qat'iy SLA Qoidasi

### A. Kod sifati standartlari:
- Python kodi **PEP8** qoidalariga mos kelishi shart.
- C++ kodi Google C++ Style Guide talablariga mos yoziladi.
- Barcha algoritmlar va modullar uchun Unit Test qamrovi **100% yashil** bo'lishi shart (`pytest` va `unittest`).

### B. ⏱️ 10 Daqiqalik Maksimal Kutish (SLA Qoidasi):
- Hech qanday vaziyatda avtomobil kirish/chiqish to'sig'ida 10 daqiqadan ko'p ushlab turilishi mumkin emas.
- 5 daqiqada sariq ogohlantirish, 7 daqiqada qizil favqulodda signal, 10 daqiqada esa Fail-Safe avtomatik ochilish kafolatlangan.

### C. Definition of Done (DoD — Ish bitganlik mezoni):
Vazifa faqat quyidagi shartlar to'liq bajarilgandagina **Done** ustuniga o'tkaziladi:
- [x] Acceptance Criteria (DoD) talablari 100% bajarilgan.
- [x] 10 minutlik maksimal kutish chegarasi tekshirilgan va tasdiqlangan.
- [x] Barcha tegishli Unit va integratsion testlar yozilgan va muvaffaqiyatli o'tgan.
- [x] Kod review'dan o'tgan va tasdiqlangan.
- [x] Kod `main` yoki `Mirhamid` tarmog'iga merge qilingan.
- [x] Hujjatlar (`BACKLOG.md`, `TASKCAFE_BOARD.md`, `README.md`) yangilangan.
