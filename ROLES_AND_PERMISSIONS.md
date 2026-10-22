# 🛡️ Parkly.uz — Jamoa A'zolari, Rollar va Ruxsatlar Matritsasi (RBAC & GitHub)

Parkly.uz aqlli avtoturargoh tizimi barqaror, xavfsiz va uzluksiz ishlashi uchun barcha a'zolarning GitHub repozitoriyasidagi hamda C++/Qt Desktop Admin boshqaruv panelidagi rasmiy rollari va mas'uliyatlari aniq belgilangan.

---

## 👥 1. Rasmiy Jamoa A'zolari va Texnik Rollar (6 Ta Asosiy A'zo)

Loyiha tarkibi 6 nafar professional muhandis va yetakchilardan iborat. Barcha boshqaruv va texnik vazifalar faqat ushbu jamoa o'rtasida taqsimlangan:

| № | F.I.SH. | Tizim Logini | Loyihadagi Rasmiy Vazifasi | Tizim Roli (RBAC) | GitHub Huquqi |
|---|---|---|---|---|---|
| 1 | **Samaxov Dilshod** | `dilshod_pm` | **Product Manager (PM)** | `SUPER_ADMIN` | `Admin / Owner` |
| 2 | **Erjigitov Mirhamid** | `mirhamid_be` | **Backend & Algoritmlar (Bosh Rahbar)** | `SUPER_ADMIN` | `Admin / Maintain` |
| 3 | **Tohirjonov Hikmatilla** | `hikmatilla_fe` | **Frontend & Desktop Admin Panel** | `ADMIN` | `Write / Collaborator` |
| 4 | **Mamasarulov Jaloliddin**| `jaloliddin_iot` | **IoT & Mikrokontroller (ESP32)** | `ADMIN` | `Write / Collaborator` |
| 5 | **Saidov Abbosxon** | `abbosxon_qa` | **QA (Sifat Nazorati) & DevOps** | `ADMIN` | `Write / Collaborator` |
| 6 | **Omirboyev Said** | `omirboyev_cv` | **Computer Vision (ANPR & OCR)** | `ADMIN` | `Write / Collaborator` |

---

## 🏛️ 2. Dasturiy Tizim RBAC Huquqlar Matritsasi (Desktop Admin Panel)

Desktop Admin boshqaruv panelida ruxsatlar 2 ta qat'iy toifaga bo'linadi:

### 👑 A. Super-Admin Huquqlari (`SUPER_ADMIN`)
*Foydalanuvchilar:* `dilshod_pm` (Samaxov Dilshod) va `mirhamid_be` (Erjigitov Mirhamid).
- **Barcha 7 ta bo'limga to'liq kirish va tahrirlash:**
  1. Asosiy Dashboard (Jonli statistika va metrikalar).
  2. 3D İzometrik Xarita (Slotlarni qo'lda bo'shatish yoki band qilish).
  3. Kameralar & ANPR (RTSP oqimi va kadrlar monitoringi).
  4. Moliya va Kassa (Click, Payme, Uzum to'lovlari va hisobotlar).
  5. Sessiyalar va Mashinalar (Faol transportlar va Fastline nazorati).
  6. **Xodimlar va Huquqlar:** Barcha xodimlarni boshqarish, yangi xodim qo'shish, istalgan xodimning login va parolini o'zgartirish (✏️ Tahrirlash).
  7. **Tizim Sozlamalari:** Soatlik tariflar, grace period, kunduzgi/tungi stavkalarni belgilash.
- **Favqulodda Shlagbaum Boshqaruvi:** 10 daqiqalik kutish limiti (SLA Fail-Safe) buzilganda shlagbaumni majburiy ochish va sababini auditga yozish.

### 🛡️ B. Oddiy Admin Huquqlari (`ADMIN`)
*Foydalanuvchilar:* `hikmatilla_fe`, `jaloliddin_iot`, `abbosxon_qa`, `omirboyev_cv`.
- **Ruxsat berilgan amallar:**
  - Real-vaqt monitoringi va 3D İzometrik xaritaning joriy holatini kuzatish.
  - Kameralar oqimini ko'rish va avtoraqam tanish loglarini tekshirish.
  - O'z yo'nalishi bo'yicha ma'lumotlarni monitoring qilish.
  - **Faqat o'zining shaxsiy login va parolini o'zgartirish.**
- **Taqiqlangan amallar (Qulflangan 🔒):**
  - ❌ Boshqa xodimlarning ma'lumotlarini yoki parolini o'zgartirish taqiqlanadi.
  - ❌ Tizim tarif stavkalari va moliyaviy sozlamalarni o'zgartira olmaydi.

---

## ⏱️ 3. 10 Daqiqalik Maksimal Kutish va Fail-Safe Shlagbaum Qoidasi

Avtoturargohda hech qanday avtomobil kirish yoki chiqish shlagbaumida 10 daqiqadan ortiq ushlanib qolmasligi shart:
1. **0 – 5 daqiqa (Normal):** ANPR kamerasi orqali raqam o'qiladi, to'lov yoki obuna tekshirilib, shlagbaum avtomatik ochiladi.
2. **5 – 7 daqiqa (Ogohlantirish):** Admin panelida sariq xabarnoma chiqadi, kamera noaniq o'qigan bo'lsa raqamni tasdiqlash so'raladi.
3. **7 – 10 daqiqa (Kritik):** Super-Admin panelida qizil signal chalib, tirbandlik xavfi bildiriladi.
4. **10 daqiqa (Favqulodda Fail-Safe):** Shlagbaum avtomatik bir martalik ruxsat bilan ochilib, transport o'tkazib yuboriladi va voqea `barrier_audit` jadvaliga yoziladi.

---

## 💻 4. GitHub Repozitoriyasi Ish Tartibi va Branch Protection

- **Branch Strategiyasi:** Yangi funksiyalar `feature/*` tarmoqlarida yoziladi va `Mirhamid` (yoki `dev`) tarmog'iga Pull Request (PR) orqali birlashtiriladi.
- **Branch Protection:** `main` tarmog'iga to'g'ridan-to'g'ri push qilish cheklangan. Barcha o'zgarishlar Code Review va CI testlaridan o'tgandan so'ng merge qilinadi.
