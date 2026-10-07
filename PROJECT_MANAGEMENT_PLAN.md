# 📊 Parkly.uz — Loyihani Boshqarish Rejasi (Project Management Plan)

> **Loyiha:** Parkly.uz — Smart Parking Management System  
> **Loyiha kodi:** PRK-UZ-2026  
> **Metodologiya:** Agile / Scrum  
> **Hujjat maqsadi:** 8 haftalik (4 sprint, 6 kishi) ishlab chiqish jarayonini sifatli, xavfsiz va tizimli boshqarish bo'yicha to'liq qo'llanma.

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
1. **Sprint Planning:** Product Owner va PM rahbarligida navbatdagi sprint uchun vazifalar (User Stories & Tasks) tanlanadi va har bir jamoa a'zosiga biriktiriladi.
2. **Daily Standup:** Kunlik 15 daqiqalik yig'ilish. Har bir dasturchi 3 ta savolga javob beradi:
   - *Kecha nima ishni bajardim?*
   - *Bugun qaysi vazifani bajaraman?*
   - *Qanday to'siq yoki texnik qiyinchilik bor?*
3. **Sprint Review (Demo):** Ishlab chiquvchilar tayyor bo'lgan dasturiy qismlarni (API, simulyator, ANPR, Desktop oynasi) Product Ownerga real ishchi holatda ko'rsatadi.
4. **Sprint Retrospective:** Jamoa jarayonini tahlil qilish: nima yaxshi ishladi, qayerda kechikish bo'ldi, keyingi sprintda nimani yaxshilash kerak.

---

## 2. Jamoa RACI Mas'uliyat Matritsasi

- **R (Responsible):** Vazifani bevosita bajaruvchi dasturchi
- **A (Accountable):** Natija uchun yakuniy javobgar yagona shaxs
- **C (Consulted):** Maslahat beruvchi mutaxassis
- **I (Informed):** Jarayon haqida xabardor qilib boriladigan shaxs

| Loyiha Moduli / Jarayon | Product Owner (erjigitvv5) | Project Manager | Lead / Senior Dev | Backend Dev | C++ Dev | Desktop Dev | QA Tester |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Project Charter va Maqsadlar** | **A** | R | C | I | I | I | I |
| **Sprint Rejalari va Backlog** | **A** | R | C | C | C | C | C |
| **Arxitektura va 4 ta Algoritm** | I | I | **A / R** | R | R | C | C |
| **Computer Vision & ANPR Moduli** | I | I | **A** | C | R | C | R |
| **PostgreSQL & Core Backend API** | I | I | A | **R** | C | C | I |
| **C/C++ & CLI Sensor Simulyatori**| I | I | A | C | **R** | C | I |
| **Desktop Admin Boshqaruv Paneli**| C | I | A | C | I | **R** | I |
| **Payme & Click To'lov Tizimlari** | C | I | A | **R** | I | I | C |
| **Sifat Nazorati va Sinovlar** | I | I | A | C | C | C | **R** |
| **Yakuniy Reliz va Taqdimot** | **A** | R | R | R | R | R | R |

---

## 3. Kommunikatsiya va Aloqa Rejasi (Communication Plan)

| Kanal / Vosita | Vazifasi va Maqsadi | Ishtirokchilar | Qachon / Qancha vaqtda |
| :--- | :--- | :--- | :--- |
| **GitHub Projects** | Kanban doskasi (Tasklar holati) | Barcha jamoa | Real-vaqtda (har kuni yangilanadi) |
| **Telegram Tech Guruh** | Tezkor texnik savollar va xabarlar | Barcha jamoa | Doimiy (ish vaqti) |
| **GitHub Pull Requests** | Kod tekshiruvi (Code Review) | Lead Dev, Dasturchilar | Har bir yangi kod topshirilganda |
| **Google Meet** | Standup va Rejalashtirish majlislari | Barcha jamoa | Dushanba va Juma (jadval bo'yicha) |

---

## 4. Sifatni Boshqarish Rejasi (Quality Management Plan)

### A. Kod sifati standartlari:
- Python kodi **PEP8** qoidalariga (`ruff` / `black`) mos kelishi shart.
- C++ kodi Google C++ Style Guide talablariga mos yoziladi.
- Barcha algoritmlar va modullar uchun Unit Test qamrovi **kamida 80%** bo'lishi shart.

### B. Pull Request (PR) va Code Review qoidalari:
1. `main` tarmog'iga to'g'ridan-to'g'ri kod yuborish (push) qat'iyan taqiqlangan.
2. Har bir dasturchi o'z vazifasi uchun alohida tarmoq ochadi (`feature/issue-raqami`).
3. PR ochilganda avtomatik CI testlari muvaffaqiyatli (`PASS`) o'tishi kerak.
4. Kamida **1 nafar Senior / Lead dasturchi** kodni to'liq tekshirib tasdiqlashi (Approve) lozim.

### C. Definition of Done (DoD — Ish bitganlik mezoni):
Vazifa faqat quyidagi 5 ta shart to'liq bajarilgandagina **Done** ustuniga o'tkaziladi:
- [x] Acceptance Criteria (DoD) talablari 100% bajarilgan.
- [x] Barcha tegishli Unit va integratsion testlar yozilgan va muvaffaqiyatli o'tgan.
- [x] Kod review'dan o'tgan va tasdiqlangan.
- [x] Kod `develop` yoki `main` tarmog'iga merge qilingan.
- [x] Hujjatlar (Swagger, README) kerakli joyda yangilangan.

---

## 5. Xatarlar va Muammolarni Hal Qilish Tartibi (Escalation Matrix)

```
[ Muammo yuzaga keldi ]
         │
         ▼
[ Dasturchi 2 soat ichida yecha olmasa ] ──► [ Lead Developer texnik yordamga keladi ]
                                                      │
                                                      ▼ (Agar muddatga ta'sir qilsa)
                                            [ PM va Product Ownerga eskalatsiya qilinadi ]
```

1. **Texnik to'siqlar:** Agar dasturchi texnik muammo sababli 2 soatdan ortiq ushlanib qolsa, Standup'da yoki umumiy chatda buni ochiq bildiradi.
2. **Muddat xavfi:** Agar vazifa kechikishi kutilsa, PM boshqa vazifalarning ustuvorligini qayta ko'rib chiqadi (Scope re-prioritization).

---

## 6. O'zgarishlarni Boshqarish Jarayoni (Change Control)

Agarda mijoz yoki tashqi omillar sababli yangi talab paydo bo'lsa:
1. Yangi talab faqat **Product Owner (erjigitvv5)** tomonidan taklif qilinadi.
2. PM va Lead Dev uning murakkabligini (Story Points) baholaydi.
3. Jamoa zo'riqib ketmasligi uchun joriy sprintdan unga teng hajmdagi past ustuvorlikdagi (`Could Have`) vazifa keyingi sprintga suriladi (Trade-off qoidasi).
