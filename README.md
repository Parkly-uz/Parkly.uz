<p align="center">
  <img src="assets/logo.png" width="420" alt="PARKY.uz Logo" />
</p>

# 🚗 Parkly.uz — Smart Parking Management System

> **Parkly.uz** — Shaharlar, savdo markazlari, biznes markazlar va xususiy avtoturargohlar uchun aqlli, to'liq avtomatlashtirilgan va xavfsiz Smart Parkovka ekotizimi.

---

## 📌 Loyiha haqida (Overview)

Parkly.uz haydovchilar uchun bo'sh joylarni real vaqt rejimida (real-time) topish, oldindan bron qilish (booking) hamda avtomatlashtirilgan to'lovlarni amalga oshirish imkonini beradi. Avtoturargoh egalari va boshqaruvchilari uchun esa aqlli hisob-kitob, ANPR (davlat raqamini aniqlash) kamerasi integratsiyasi, to'siqlar (barrier/shlagbaum) nazorati va analitika platformasini taqdim etadi.

---

## 🏗️ Tizim arxitekturasi va komponentlari

1. **📱 Mobil ilova (Haydovchilar uchun):**
   - Bo'sh joylar xaritasi (Google Maps / Yandex Maps integratsiyasi).
   - Joyni oldindan band qilish (Booking).
   - QR kod yoki avtomobil raqami orqali kirish/chiqish.
   - Tezkor to'lovlar (Payme, Click, Uzum Pay).

2. **🖥️ Web Dashboard (Admin & Operatorlar):**
   - Parkovka to'lalik darajasi (real-time occupancy).
   - Daromadlar, tariflar va hisobotlar tahlili.
   - Shlagbaum va kameralarni masofadan boshqarish.

3. **📷 IoT & Computer Vision (Hardware / Edge):**
   - ANPR (Automatic Number Plate Recognition) kameralari.
   - Ultratovush / magnit datchiklar (joy bo'shligini aniqlash).
   - Shlagbaum kontrollerlari (MQTT / WebSocket / Modbus).

4. **⚙️ Backend API:**
   - Mikroservis / Modul-monolit arxitektura.
   - Real-time aloqa: WebSockets / gRPC.
   - Tranzaksiyalar xavfsizligi va audit loglar.

---

## 👥 Jamoa tuzilmasi va Rollar

| Rol | GitHub Ruxsati (Permission) | Mas'uliyat |
| :--- | :--- | :--- |
| **Owner / Founder** | **Owner / Admin** | Loyiha egasi, yakuniy strategik qarorlar, to'liq boshqaruv |
| **Project Manager (PM)** | **Triage / Maintain** | Vazifalarni taqsimlash, sprintlar, Milestone va Issue nazorati |
| **Lead / Senior Dev** | **Maintain / Admin** | Arxitektura, kod sifatini nazorat qilish (Code Review), PR merge |
| **Backend / Frontend / Mobile Devs** | **Write** | Funksional kod yozish, yangi feature branchlar, PR yaratish |
| **QA / Tester** | **Triage / Read** | Bug reportlar ochish, release test qilish |

> Batafsil ruxsatlar bo'yicha ko'rsatma: [ROLES_AND_PERMISSIONS.md](ROLES_AND_PERMISSIONS.md)  
> Rasmiy loyiha boshqaruvi hujjatlari: [PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md) | [PROJECT_MANAGEMENT_PLAN.md](docs/PROJECT_MANAGEMENT_PLAN.md)

---

## 🌿 Git Branching Strategy (Ish jarayoni qoidasi)

- `main` — Faqat barqaror, ishlab turgan production versiya (faqat PR orqali merge qilinadi, to'g'ridan-to'g'ri push taqiqlangan).
- `develop` — Asosiy integratsiya tarmog'i (staging).
- `feature/<vazifa-nomi>` — Yangi imkoniyatlar uchun alohida tarmoqlar (masalan: `feature/anpr-plate-recognition`, `feature/payme-integration`).
- `bugfix/<muammo-nomi>` — Xatoliklarni to'g'rilash tarmog'i.
- `hotfix/<muammo-nomi>` — Production'dagi shoshilinch muammolar uchun.

---

## 🚀 Texnologik stek (Tavsiya etilgan)

- **Backend:** Node.js (NestJS / TypeScript) yoki Go (Golang) / Python (FastAPI)
- **Database:** PostgreSQL + Redis (keshlash va real-time holatlar uchun)
- **Frontend / Admin:** Next.js (React) / Tailwind CSS
- **Mobile:** Flutter (iOS & Android)
- **IoT & Computer Vision:** Python (OpenCV, YOLO v8/v11), MQTT broker (EMQX)
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD)

---

## 📄 Litsenziya

Loyiha xususiy mulk hisoblanadi. © 2026 Parkly.uz. Barcha huquqlar himoyalangan.
