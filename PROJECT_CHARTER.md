# 📜 Parkly.uz — Rasmiy Loyiha Nizomi (Project Charter)

> **Loyiha nomi:** Parkly.uz — Smart Parking Management System  
> **Loyiha kodi:** PRK-UZ-2026  
> **Loyiha egasi (Product Owner):** erjigitvv5  
> **Metodologiya:** Agile / Scrum (4 ta Sprint, 2 oy)  
> **Repozitoriy:** [github.com/erjigitvv5/Parkly.uz](https://github.com/erjigitvv5/Parkly.uz.git)  
> **Holati:** Rasmiy tasdiqlangan (Approved)  

---

## 1. Loyiha Pasporti (Project Profile)

| Ko'rsatkich | Tavsif |
| :--- | :--- |
| **Loyiha nomi** | Parkly.uz — Aqlli Avtoturargoh Boshqaruv Tizimi |
| **Boshlanish sanasi** | 2026-yil 7-oktyabr |
| **Rejalashtirilgan yakun** | 2026-yil dekabr (8 hafta / 4 sprint) |
| **Jamoa tarkibi** | 6 nafar mutaxassis (PO, PM, Tech Lead, Backend, C++/IoT, Desktop UI, QA) |
| **Asosiy texnologiyalar** | Python (FastAPI), PostgreSQL, C/C++, OpenCV (ANPR), Desktop GUI (PyQt) |
| **To'lov integratsiyasi** | Payme va Click Sandbox + O'zbekiston Davlat Soliq Qo'mitasi fiskal modeli |

---

## 2. Biznes Asosi va Muammo Tahlili (Business Case)

### Mavjud muammolar:
1. **Vaqt yo'qotilishi:** Shahar markazlarida haydovchilar bo'sh joy qidirish uchun har kuni o'rtacha 15–25 daqiqa behuda vaqt va yoqilg'i sarflaydi.
2. **Kirish/Chiqish tirbandligi:** Shlagbaum oldida qog'oz chipta olish va naqd to'lov qilish oqibatida katta tirbandliklar yuzaga keladi.
3. **Shaffoflikning yo'qligi:** Avtoturargoh egalari uchun tushumlarni 100% nazorat qilish va noqonuniy naqd pul aylanmasini to'xtatish imkoniyati cheklangan.

### Taklif etilayotgan yechim:
**Parkly.uz** — to'liq avtomatlashtirilgan aqlli ekotizim:
- **Intellektual ANPR:** 7 millisekundda O'zbekiston davlat raqamlarini taniydi, yoritilishi past bo'lganda adaptiv CLAHE va Gamma korreksiyasi orqali kontrastni oshiradi, qiyshiq rakurslarni Homography orqali tekislaydi.
- **Aqlli Algoritmlar:**
  - Kirgan mashinaga eng yaqin va mos bo'sh joyni ajratish (`SpotAllocator`).
  - Dastlabki 15 daqiqa bepul va soatlik moslashuvchan tariflar (`TariffCalculator`).
  - Vaqt to'qnashuvlarisiz joyni oldindan band qilish (`ReservationMatcher`).
  - To'siq va shlagbaumni avtomatik ochuvchi holat mashinasi (`GateController`).
- **Markaziy Desktop Boshqaruv:** Super-Admin, 2 ta filial Admini va 5 ta Smena Operatorlari uchun jonli monitoring paneli.

---

## 3. Loyiha Doirasi (Project Scope)

### ✅ Loyiha Doirasiga Kiradi (In-Scope — MVP):
1. **Universal Kamera & ANPR Moduli:** RTSP, IP-kamera va Web-kameralardan 5–10 FPS oqim olish, Two-Stage (Mashina ➡️ Raqam) aniqlash, Homography va ko'pchilik ovozi (Temporal Voting).
2. **Core Backend & PostgreSQL DB:** Qat'iy tiplashtirilgan jadvallar, slotlar, seanslar, tariflar va Alembic migratsiyalari.
3. **C/C++ & Python Sensor Simulyatori:** Terminalda ishlovchi CLI avtomatik avtomobillar oqimi simulyatori.
4. **Desktop Admin Panel:** Xodimlar, jonli transport, slotlar 2D xaritasi va favqulodda shlagbaumni ochish (Manual Override).
5. **To'lov Moduli:** Payme va Click Sandbox integratsiyasi, to'lovdan so'ng chiqish uchun 15 daqiqalik bepul oraliq.
6. **Sifat va Xavfsizlik:** 100 ta aniq texnik vazifa, avtomatlashtirilgan testlar va CI pipeline.

### ❌ Loyiha Doirasiga Kirmaydi (Out-of-Scope — 2-Bosqich):
- Jismoniy shlagbaum temir konstruksiyalarini montaj qilish.
- Banklarning jismoniy POS-terminallari apparatini ulash.

---

## 4. Asosiy Bosqichlar va Jadval (Milestones)

| Milestone | Muddat | Yuklama | Kutilayotgan Natija |
| :--- | :---: | :---: | :--- |
| **M1: Poydevor va Arxitektura** | 1–2 hafta | 23 SP | DB sxemasi, 4 ta algoritm, ANPR asosi, Git repository tayyor |
| **M2: Parkovkalar va Admin Asosi**| 3–4 hafta | 24 SP | Slotlar CRUD, Xarita integratsiyasi, Staging deploy |
| **M3: MVP Asosiy Funksiyalar** | 5–6 hafta | 29 SP | CLI simulyator, Real-time slotlar, Bron qilish, Tariflar |
| **M4: To'lov, Sifat va Taqdimot** | 7–8 hafta | 29 SP | Payme/Click Sandbox, Desktop Admin release, Demo taqdimot |

---

## 5. Jamoa Tuzilmasi va Manfaatchilar (Stakeholders)

| Ism / Rol | Boshqaruvdagi O'rni | Mas'uliyati |
| :--- | :--- | :--- |
| **erjigitvv5 (Product Owner)** | Loyiha egasi | Yakuniy talablar, byudjet, qabul qilish va relizlar |
| **Project Manager (PM)** | Jarayon boshqaruvchisi | Sprintlar rejasi, risklar nazorati, GitHub Projects doskasi |
| **Lead / Senior Developer** | Texnik rahbar | Arxitektura, kod sifatini nazorat qilish (Code Review), CI/CD |
| **Backend Developer** | Dasturchi | Python (FastAPI), PostgreSQL, API integratsiyalari |
| **C/C++ & System Developer** | Dasturchi | Hardware simulyatori, past darajadagi protokollar |
| **Desktop / UI Developer** | Dasturchi | PyQt Desktop Admin paneli va interaktiv xarita |
| **QA Engineer** | Sifat mutaxassisi | Test-case'lar, yuklama testlari, avtomatik testlar |

---

## 6. Muvaffaqiyat Mezonlari (Key Success Metrics & KPIs)

1. **Vaqtga rioya (On-time Delivery):** Barcha 4 ta sprint o'z vaqtida (kechikish < 5%) topshirilishi.
2. **Aniqlik va Sifat:**
   - ANPR davlat raqamlarini aniqlash aniqligi $\ge 95\%$.
   - Algoritmlar testlar bilan 100% qamrab olingan bo'lishi.
3. **Tezkorlik (Performance):**
   - ANPR kadrini qayta ishlash tezligi $\le 10$ ms.
   - Shlagbaum ochilishiga buyruq berish $\le 500$ ms.
4. **Moliyaviy hisob-kitob:** To'lovlar va daqiqalar bo'yicha xatolik $0\%$.

---

## 7. Loyiha Xatarlari (Risk Management Summary)

| Xatar | Ehtimollik | Ta'sir | Yumshatish Chorasi |
| :--- | :---: | :---: | :--- |
| **Jismoniy datchiklar kechikishi** | Yuqori | O'rta | C++/Python CLI simulyatoridan to'liq foydalanish |
| **Qorong'ida raqam o'qilmasligi** | O'rta | Yuqori | Adaptive CLAHE + Gamma korreksiyasi va zaxira QR chipta |
| **To'lov integratsiyasi cheklovlari** | O'rta | O'rta | Rasmiy Payme va Click Sandbox test hisoblaridan foydalanish |

---

## 8. Rasmiy Tasdiq (Charter Approval & Sign-off)

- **Loyiha Egasi (Product Owner):** ___________________________ (Sana: 07.10.2026)  
- **Texnik Rahbar (Tech Lead):** _____________________________ (Sana: 07.10.2026)  
- **Loyiha Menejeri (Project Manager):** ______________________ (Sana: 07.10.2026)  
