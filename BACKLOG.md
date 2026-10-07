# 📋 Parkly.uz — Rasmiy Product Backlog va Sprint Rejasi

> **Repozitoriy:** [github.com/erjigitvv5/Parkly.uz](https://github.com/erjigitvv5/Parkly.uz.git)  
> **Jamoa:** 6 kishi  
> **Muddat:** 2 oy (4 ta Sprint, har biri 2 hafta)  
> **Jami yuklama:** ~105 Story Point (SP)  
> **Xususiyat:** Texnologiyalar va IoT uskunalari hali to'liq aniq bo'lmagani sababli vazifalar neytral shaklda yozildi. Jismoniy sensorlar o'rniga dasturiy simulyator nazarda tutilgan.

---

## 🏃 1. Sprint Rejasi (Release Roadmap)

| Sprint | Muddat | Maqsad | Story'lar | Yuklama (SP) |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 1 (S1)** | 1–2 hafta | **Poydevor:** Rejalashtirish, arxitektura, lokal muhit va User auth | 1.1, 1.2, 2.1, 2.2, 3.1 | **23 SP** |
| **Sprint 2 (S2)** | 3–4 hafta | **Parkovkalar va admin asosi:** Rollar, avtolar, xarita, deploy, joylar CRUD | 3.2, 3.3, 4.1, 2.3, 7.1 | **24 SP** |
| **Sprint 3 (S3)** | 5–6 hafta | **Asosiy funksiyalar (MVP):** Sensor simulyatori, real-time slotlar, bron qilish, tariflar | 4.2, 5.1, 5.2, 6.1, 7.2 | **29 SP** |
| **Sprint 4 (S4)** | 7–8 hafta | **To'lov, sifat va taqdimot:** Qidiruv, bildirishnomalar, to'lov, testlash, xavfsizlik, demo | 4.3, 5.3, 6.2, 8.1, 8.2, 8.3 | **29 SP** |

> 💡 *Eslatma: Sprint 1 yakunlanganidan so'ng jamoaning haqiqiy tezligiga (velocity) qarab SP baholari qayta ko'rib chiqiladi.*

---

## 🎯 2. Epiklar, Story'lar va Vazifalar (Epic → Story → Task)

> **Ustuvorlik darajalari:**
> - **M (Must have)** — Bo'lishi shart (MVP talabi)
> - **S (Should have)** — Juda muhim, keyingi bosqichda qo'shiladi
> - **C (Could have)** — Qo'shimcha qulaylik

---

### 🏛️ EPIC 1: Loyiha boshqaruvi (Project Management)

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1.1** | **Jamoa sifatida loyihani rejalashtirish** | • Rollarni taqsimlash (RACI jadvali)<br>• Project Charter (Nizom) yozish<br>• Risk register (Xatarlar reestri) tuzish<br>• GitHub Project doskasini sozlash | **M** | 5 | S1 |
| **1.2** | **Talablar va raqobatchilar tahlili** | • Foydalanuvchi talablarini yig'ish<br>• O'xshash tizimlarni (raqobatchilar) tahlil qilish<br>• Talablar hujjatini (SRS) yozish | **M** | 3 | S1 |

---

### 💻 EPIC 2: Arxitektura va infratuzilma (Computer Management)

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **2.1** | **Tizim arxitekturasi va ma'lumotlar bazasi dizayni** | • Texnologiya stekini tanlash<br>• Arxitektura diagrammasini chizish<br>• Ma'lumotlar bazasi ER diagrammasini ishlab chiqish | **M** | 5 | S1 |
| **2.2** | **Dasturlash muhiti va CI** | • Repo strukturasi va branch strategiyasini o'rnatish<br>• Lokal muhitni sozlash (`.env` / Docker)<br>• CI: lint va testlarni avtomatlashtirish | **M** | 5 | S1 |
| **2.3** | **Serverga joylashtirish (deploy)** | • Server / hosting provayderini tanlash<br>• Test muhitiga (staging) deploy qilish<br>• Zaxira nusxa (backup) va monitoring o'rnatish | **S** | 5 | S2 |

---

### 👥 EPIC 3: Foydalanuvchilar va autentifikatsiya

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **3.1** | **Haydovchi sifatida ro'yxatdan o'tish va kirish** | • Foydalanuvchi modeli (DB schema)<br>• Register / Login API yaratish<br>• Kirish va ro'yxatdan o'tish UI formasi | **M** | 5 | S1 |
| **3.2** | **Rollar bo'yicha kirish (haydovchi / operator / admin)** | • Rollar modeli (RBAC)<br>• Ruxsatlarni tekshirish (Middleware/Guards)<br>• Rolga qarab moslashuvchan UI interfeysi | **M** | 3 | S2 |
| **3.3** | **Profil va avtomobillarni qo'shish** | • Avtomobil modeli (DB)<br>• Profil API (mashina qo'shish, tahrirlash)<br>• Foydalanuvchi profili sahifasi | **S** | 3 | S2 |

---

### 🚗 EPIC 4: Parkovka va real vaqt monitoring

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **4.1** | **Parkovkalarni xaritada ko'rish** | • Parkovka modeli va CRUD API<br>• Xarita integratsiyasi (Map SDK)<br>• Parkovka kartochkasi UI | **M** | 8 | S2 |
| **4.2** | **Bo'sh va band joylarni real vaqtda ko'rish** | • Joy holati (slot status) API<br>• Sensor simulyatori (dasturiy virtual datchiklar)<br>• Real vaqt yangilanish (WebSocket / Polling)<br>• Joylar sxemasi UI (interaktiv xarita) | **M** | 8 | S3 |
| **4.3** | **Qidiruv va filtrlash** | • Manzil / narx bo'yicha qidiruv logikasi<br>• Filtr API endpointlari<br>• Qidiruv va filtr interfeysi (UI) | **C** | 3 | S4 |

---

### 📅 EPIC 5: Joy band qilish (Booking & Reservation)

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **5.1** | **Joyni oldindan band qilish** | • Band qilish modeli (DB Reservation)<br>• Vaqt to'qnashuvini (overlap conflict) tekshirish<br>• Band qilish API<br>• Band qilish foydalanuvchi interfeysi (UI) | **M** | 8 | S3 |
| **5.2** | **Bandni bekor qilish va muddati tugashi** | • Bekor qilish (Cancel) API<br>• Muddati o'tgan bandlarni avtomatik bo'shatish (Cron / Worker) | **S** | 3 | S3 |
| **5.3** | **Bildirishnomalar (Notifications)** | • Bildirishnoma xizmati (Push / SMS / Telegram)<br>• Band tasdig'i va muddat tugashi eslatma xabarlari | **C** | 5 | S4 |

---

### 💳 EPIC 6: To'lov va tarif

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **6.1** | **Tarif asosida narx hisoblash** | • Tarif modeli (soatlik, kunlik, bepul daqiqalar)<br>• Narx hisoblash biznes logikasi funksiyasi<br>• Unit testlar bilan to'liq qoplash | **M** | 5 | S3 |
| **6.2** | **Onlayn to'lov (test rejimida)** | • To'lov provayderini tanlash (Payme / Click Sandbox)<br>• Webhook va to'lov integratsiyasi<br>• To'lov holatini tekshirish va kvitansiya (chek) | **S** | 8 | S4 |

---

### 🛠️ EPIC 7: Admin panel

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **7.1** | **Admin parkovka va joylarni boshqarishi** | • Parkovka ma'lumotlarini tahrirlash CRUD<br>• Joylar (Slots) CRUD amallari<br>• Admin boshqaruv paneli interfeysi (UI) | **M** | 5 | S2 |
| **7.2** | **Statistika dashboardi** | • Band qilish va daromad statistikasi API<br>• Interaktiv analitika grafiklari | **S** | 5 | S3 |

---

### 🛡️ EPIC 8: Sifat, xavfsizlik va taqdimot

| ID | Story | Task'lar | Ustuvorlik | SP | Sprint |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **8.1** | **Tizimni testlash** | • Test-case'lar yozish<br>• Integratsion va API testlari<br>• Topilgan xatolarni (bugs) to'g'rilash | **M** | 5 | S4 |
| **8.2** | **Xavfsizlik tekshiruvi** | • Parollarni kuchli hash qilish (bcrypt/argon2) va validatsiya<br>• Rate limit (DDoS himoyasi)<br>• OWASP zaifliklarini audit qilish | **S** | 3 | S4 |
| **8.3** | **Hujjatlar va yakuniy taqdimot** | • README.md hujjatini yangilash<br>• Foydalanuvchi va admin qo'llanmasi<br>• Demo video va taqdimot slaydlari | **M** | 5 | S4 |

---

## 📋 3. GitHub'da Loyihani Sozlash Qoidalari

### A. Kanban doskasi (GitHub Projects) ustunlari:
```
[ Backlog ] ──► [ Sprint To Do ] ──► [ In Progress ] ──► [ Review ] ──► [ Done ]
```

### B. Label'lar tizimi:
- **Turi:** `epic`, `story`, `task`, `bug`
- **Ustuvorlik:** `priority:must`, `priority:should`, `priority:could`
- **Soha:** `backend`, `frontend`, `devops`, `docs`

### C. Milestone'lar:
- `Sprint 1`
- `Sprint 2`
- `Sprint 3`
- `Sprint 4`

### D. Tuzilma qoidasi:
- Har bir **Epic** va **Story** alohida **Issue** bo'ladi.
- **Task'lar** esa tegishli Story ichida nazorat ro'yxati (checklist `- [ ]`) ko'rinishida yoziladi.

### E. Definition of Done (DoD):
Vazifa quyidagi shartlar to'liq bajarilgandagina **Done** ustuniga o'tkaziladi:
- [x] Kod review'dan o'tgan (kamida 1 ta tasdiq)
- [x] Avtomatlashgan testlar muvaffaqiyatli o'tgan
- [x] Kod `main` yoki `develop` tarmog'iga merge qilingan
- [x] Barcha Acceptance Criteria'lar to'liq bajarilgan
