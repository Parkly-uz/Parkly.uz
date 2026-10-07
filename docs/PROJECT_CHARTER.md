# 📜 Parkly.uz — Loyiha Nizomi (Project Charter)

| Loyiha Nomi | **Parkly.uz — Smart Parking Management System** |
| :--- | :--- |
| **Loyiha Egasi (Project Owner):** | erjigitvv5 (Founder & Product Owner) |
| **Boshqaruv Usuli:** | Agile / Scrum (4 ta Sprint, 2 oy) |
| **Hujjat Versiyasi:** | 1.0 (Rasmiy tasdiqlangan) |
| **Sana:** | 2026-yil oktyabr |

---

## 1. Loyihaning Maqsadi va Biznes Asosi (Executive Summary & Business Case)

### Muammo:
O'zbekiston yirik shaharlarida (ayniqsa Toshkentda) savdo markazlari, biznes markazlar va jamoat joylarida avtoturargoh topish haydovchilarning kuniga o'rtacha 15–25 daqiqa vaqtini oladi. Mavjud parkovkalarda kirish-chiqishda navbatlar, qo'lda to'lov qilishdagi noqulayliklar, shaffof hisobotning yo'qligi hamda bo'sh joylar haqida ma'lumot yetishmasligi kuzatiladi.

### Yechim:
**Parkly.uz** — avtoturargoh jarayonlarini to'liq raqamlashtiruvchi intellektual ekotizim:
- Haydovchilar uchun bo'sh joylarni real vaqtda ko'rish va oldindan band qilish (Booking).
- Avtomatlashtirilgan to'lovlar (Payme, Click, Uzum) va 15 daqiqalik bepul oraliq (Grace period).
- Avtoturargoh operatorlari va rahbarlar uchun qulay **Desktop Admin Panel** (Super-admin, filial adminlari va smena operatorlari).
- Virtual va real datchiklar (sensorlar) orqali to'siqlar (shlagbaum) boshqaruvi.

---

## 2. Loyiha Doirasi (Project Scope)

### ✅ Loyiha Doirasiga Kiradi (In-Scope — MVP):
1. **Core Backend & DB:** Python (FastAPI), PostgreSQL, qat'iy ma'lumotlar sxemasi va migratsiyalar.
2. **Aqlli Algoritmlar:**
   - Optimal joy tanlash algoritmi (`SpotAllocator`).
   - Dinamik narx va grace-period kalkulyatori (`TariffCalculator`).
   - To'qnashuvsiz bron qilish tizimi (`ReservationMatcher`).
   - Shlagbaum kirish/chiqish holat mashinasi (`GateController`).
3. **C/C++ & Python Sensor Simulyatori:** Terminalda ishlovchi CLI avtomatik avtomobillar oqimi simulyatori.
4. **Desktop Admin Panel:** 1 ta Super-Admin, 2 ta Admin va 5 ta Smena Operatorlari uchun boshqaruv oynasi.
5. **To'lov Moduli:** Payme va Click Sandbox integratsiyasi va fiskal chek ma'lumotlar modeli.
6. **Loyiha Sifati:** Unit va integratsion testlar, avtomatlashtirilgan CI pipeline.

### ❌ Loyiha Doirasiga Kirmaydi (Out-of-Scope — Keyingi Fazalar):
- Jismoniy temir konstruksiyalar va shlagbaum mexanikasini o'rnatish (birinchi bosqichda virtual simulyatsiya qilinadi).
- Banklar bilan to'g'ridan-to'g'ri jismoniy POS-terminal apparatlarini payvandlash.

---

## 3. Asosiy Bosqichlar va Muddatlar (Milestones & Schedule)

| Bosqich / Milestone | Boshlanish | Tugash | Asosiy Natija (Deliverable) |
| :--- | :---: | :---: | :--- |
| **M1: Poydevor va Arxitektura** | 1-hafta | 2-hafta | Tizim arxitekturasi, DB, RBAC, Algoritmlar, Git repo tayyor |
| **M2: Parkovkalar va Admin Asosi**| 3-hafta | 4-hafta | Slotlar CRUD, Xarita integratsiyasi, Staging server deploy |
| **M3: MVP Funksionallik** | 5-hafta | 6-hafta | Sensor simulyatori, Real-time slotlar, Bron qilish, Tariflar |
| **M4: To'lov, Sifat va Taqdimot** | 7-hafta | 8-hafta | Payme/Click Sandbox, Desktop Admin release, Demo taqdimot |

---

## 4. Jamoa va Asosiy Manfaatchilar (Stakeholders & Team Roles)

| Ism / Rol | Mas'uliyat sohasi | Loyihadagi vazifasi |
| :--- | :--- | :--- |
| **Product Owner (Siz - erjigitvv5)** | Loyiha egasi / Strateg | Yakuniy talablarni qabul qilish, byudjet va relizlarni tasdiqlash |
| **Project Manager (PM)** | Jarayon boshqaruvi | Sprintlarni rejalashtirish, xatarlar nazorati, GitHub doskasi |
| **Lead / Senior Developer** | Texnik yetakchi | Arxitektura, kod sifati nazorati (Code Review), CI/CD |
| **Backend Developer (Python)** | API & Database | FastAPI, PostgreSQL, hisob-kitoblar, to'lovlar |
| **C/C++ & System Developer** | Simulyator & Hardware | Datchiklar simulyatori, aloqa protokollari, tezkor ishlov |
| **Desktop / UI Developer** | Desktop ilova | Super-admin, Admin va Operatorlar interfeysi |
| **QA Engineer (Tester)** | Sifat nazorati | Test-case'lar, avtomatik testlar va xavfsizlik auditi |

---

## 5. Muvaffaqiyat Mezonlari (Key Success Metrics & KPIs)

1. **Jadvalga rioya qilish (Schedule Variance):** Barcha 4 ta sprint o'z vaqtida (kechikish < 5%) topshirilishi.
2. **Texnik ishonchlilik (Reliability):** Algoritmlar testlar bilan 100% qamrab olingan bo'lishi.
3. **Tezkorlik (Performance):** Slot holati yangilanishi va shlagbaum ochilish javobi < 1 soniya bo'lishi.
4. **To'lov aniqligi:** Dinamik tariflar va hisob-kitoblarda 1 tiyin ham xatolikka yo'l qo'yilmasligi.

---

## 6. Loyiha Xatarlari (Risk Management Summary)

| Xatar (Risk) | Ehtimollik | Ta'sir | Yumshatish chorasi (Mitigation) |
| :--- | :---: | :---: | :--- |
| **Datchiklar yo'qligi** | Yuqori | O'rta | C++/Python CLI avtomatik sensor simulyatoridan foydalanish |
| **To'lov integratsiyasi kechikishi** | O'rta | Yuqori | Rasmiy Sandbox (Payme/Click) orqali oldindan testlash |
| **Talablar o'zgarishi** | O'rta | O'rta | 2 haftalik Scrum iteratsiyalari va moslashuvchan backlog |

---

## 7. Loyihani Tasdiqlash (Charter Sign-off)

- **Loyiha Rahbari (Product Owner):** _____________________ (Sana: 07.10.2026)
- **Bosh Texnik Mutaxassis (Tech Lead):** ________________ (Sana: 07.10.2026)
