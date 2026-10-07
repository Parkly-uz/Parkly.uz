# 📊 Parkly.uz — Loyihani Boshqarish Rejasi (Project Management Plan)

> **Loyiha:** Parkly.uz (Smart Parking Management System)  
> **Metodologiya:** Agile / Scrum  
> **Hujjat Maqsadi:** Loyihaning 2 oylik (8 hafta, 4 sprint) jarayonini tartibli, sifatli va o'z vaqtida amalga oshirish qoidalari.

---

## 1. Boshqaruv Metodologiyasi (Scrum Framework)

Loyiha **2 haftalik Sprintlar** asosida boshqariladi:

```
[ Sprint Rejalashtirish ] ──► [ 14 Kunlik Ish Jarayoni ] ──► [ Sprint Review (Demo) ] ──► [ Retrospektiva ]
       (Dushanba)              (Har kuni 15 min Standup)              (Juma)                   (Juma)
```

### Scrum Marosimlari (Ceremonies):
1. **Sprint Planning (Sprintni rejalashtirish):**
   - Har bir yangi sprintning birinchi dushanba kuni (1 soat).
   - Backlog'dan navbatdagi vazifalar tanlanadi va har bir jamoa a'zosiga biriktiriladi.
2. **Daily Standup (Kunlik tezkor yig'ilish):**
   - Har kuni soat 10:00 da (15 daqiqa, Telegram / Google Meet).
   - 3 ta savol:
     * *Kecha nima qildim?*
     * *Bugun nima qilaman?*
     * *Qanday to'siq yoki muammolar bor?*
3. **Sprint Review & Demo (Sprint natijalari namoyishi):**
   - Sprintning oxirgi juma kuni (45 daqiqa).
   - Ishlab chiquvchilar tayyor bo'lgan dasturiy qismlarni (ishlab turgan kodni) Product Ownerga ko'rsatadi.
4. **Sprint Retrospective (Retrospektiva):**
   - Demo tugagach (30 daqiqa).
   - Nima yaxshi bo'ldi? Nimani yaxshilash kerak? Keyingi sprintda nimani o'zgartiramiz?

---

## 2. Jamoa RACI Matritsasi

Loyiha jarayonida har bir vazifa bo'yicha mas'uliyat quyidagi xalqaro matritsa asosida taqsimlanadi:
- **R (Responsible):** To'g'ridan-to'g'ri bajaruvchi dasturchi
- **A (Accountable):** Natija uchun yakuniy javobgar shaxs (faqat 1 kishi)
- **C (Consulted):** Maslahat beruvchi mutaxassis
- **I (Informed):** Xabardor qilib boriladigan shaxs

| Bosqich / Vazifa | Product Owner (Siz) | Project Manager | Lead / Senior Dev | Backend Dev | C++ Dev | Desktop Dev | QA Tester |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Loyiha maqsadi va Charter** | **A** | R | C | I | I | I | I |
| **Sprint Backlog tasdiqlash** | **A** | R | C | C | C | C | C |
| **Arxitektura va Algoritmlar** | I | I | **A / R** | R | R | C | C |
| **Backend & DB yaratish** | I | I | A | **R** | C | C | I |
| **Sensor Simulyatori (CLI)** | I | I | A | C | **R** | C | I |
| **Desktop Admin Panel** | C | I | A | C | I | **R** | I |
| **Payme & Click to'lovlari** | C | I | A | **R** | I | I | C |
| **Sifat nazorati va Testlash** | I | I | A | C | C | C | **R** |
| **Yakuniy Release va Demo** | **A** | R | R | R | R | R | R |

---

## 3. Kommunikatsiya Rejasi (Communication Plan)

| Kanal / Vosita | Maqsadi | Kimlar qatnashadi | Qachon / Qancha vaqtda |
| :--- | :--- | :--- | :--- |
| **GitHub Projects** | Vazifalar holati (Kanban doska) | Barcha jamoa | Real-vaqtda (har kuni yangilanadi) |
| **Telegram Tech Guruhi** | Tezkor texnik savollar va muhokamalar | Barcha jamoa | Ish vaqti davomida doimiy |
| **GitHub Pull Requests** | Kod tekshiruvi (Code Review) | Lead Dev, Dasturchilar | Har bir feature topshirilganda |
| **Google Meet** | Standup va Rejalashtirish yig'ilishlari | Barcha jamoa | Belgilangan jadval asosida |

---

## 4. Sifatni Boshqarish Rejasi (Quality Management Plan)

### A. Kod sifati standartlari:
- Python kodi **PEP8** qoidalariga (`ruff` / `black`) mos kelishi shart.
- C++ kodi Google C++ Style Guide asosida formatlanishi kerak.
- Algoritmlar va biznes mantiqning Unit Test qamrovi **kamida 80%** bo'lishi shart.

### B. Pull Request (PR) va Code Review qoidalari:
1. Hech kim o'z kodini to'g'ridan-to'g'ri `main` tarmog'iga merge qila olmaydi.
2. Har bir PR ochilganda avtomatlashtirilgan CI testlari yashil (`PASS`) bo'lishi shart.
3. Kamida **1 nafar Senior / Lead dasturchi** kodni ko'rib chiqib tasdiqlashi (Approve) lozim.

### C. Definition of Done (DoD — Ish bitganlik mezoni):
Biror User Story quyidagi shartlar bajarilgandagina **Done** deb qabul qilinadi:
- [x] Acceptance Criteria talablari to'liq bajarilgan.
- [x] Unit/Integration testlar yozilgan va muvaffaqiyatli o'tgan.
- [x] Kod review'dan o'tgan va tasdiqlangan.
- [x] Funksiya `develop` yoki `main` tarmog'iga qo'shilgan.
- [x] Foydalanish hujjatlari (kerak bo'lsa) yangilangan.

---

## 5. Xatarlar va Muammolarni Boshqarish (Risk & Issue Management)

```
[ Muammo yuzaga keldi ] ──► [ Dasturchi 2 soat ichida yecha olmadi ] ──► [ Lead Dev yordamga keladi ] ──► [ PM / Owner xabardor qilinadi ]
```

- Agar dasturchi texnik muammo sababli 2 soatdan ortiq ushlanib qolsa, buni yashirmasdan Standup yoki umumiy chatda bildiradi.
- Lead Developer texnik yordam ko'rsatadi.
- Agar muammo muddatga ta'sir qilsa, PM vazifaning ustuvorligini qayta ko'rib chiqadi (Scope Management).

---

## 6. O'zgarishlarni Boshqarish Tartibi (Change Control)

Agarda loyihaga yangi talab (masalan, yangi to'lov turi yoki qo'shimcha interfeys) qo'shilishi kerak bo'lsa:
1. Yangi talab faqat **Product Owner (Siz)** tomonidan taklif qilinadi.
2. PM va Lead Dev uning qancha Story Point (SP) va vaqt olishini baholaydi.
3. Agar yangi vazifa kiritilsa, jamoaning yuklamasi oshib ketmasligi uchun joriy sprintdan unga teng hajmdagi past ustuvorlikdagi (`Could Have`) vazifa keyingi sprintga suriladi.
