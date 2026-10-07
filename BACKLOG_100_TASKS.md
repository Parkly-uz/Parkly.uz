# 📋 Parkly.uz — Top 100 Mukammal Backlog Tasklar Ro'yxati

> **Loyiha:** Parkly.uz — Smart Parking Management System  
> **Texnologik stek:** Python (FastAPI/Core API), PostgreSQL, C/C++ (Hardware/Simulyator datchiklar boshqaruvi)  
> **Sensor simulyatori:** CLI (konsol) orqali ishlovchi avtomatik skript (tasodifiy mashinalar oqimi)  
> **Admin panel:** Desktop ilova (Super-admin, 2 ta adminlar, 5 ta smena operatorlari)  
> **To'lovlar:** Payme va Click (Sandbox test rejimi) + Fiskal chek ma'lumotlari modeli  
> **Tuzilma:** 10 ta Modul x 10 ta Task = **Jami 100 ta aniq texnik vazifa**

---

## 🏛️ MODUL 1: Loyiha Boshqaruvi va Tizim Tahlili (Tasks 1–10)

1. **TASK-001: Jamoa RACI matritsasini ishlab chiqish**
   - *Tavsif:* 6 kishilik jamoa a'zolari o'rtasida mas'uliyatni belgilash (Responsible, Accountable, Consulted, Informed).
   - *Qatlam:* PM / Docs | *SP:* 2

2. **TASK-002: Project Charter (Loyiha Nizomi) hujjatini yozish**
   - *Tavsif:* Loyiha maqsadi, chegaralari, byudjeti, muddatlari va yakuniy kutilmalarni rasmiylashtirish.
   - *Qatlam:* PM / Docs | *SP:* 3

3. **TASK-003: Risk Register (Xatarlar reestri) tuzish**
   - *Tavsif:* Texnik (C/C++ portlar, simulyator kechikishi) va tashkiliy xatarlarni baholash va yumshatish choralari.
   - *Qatlam:* PM / Docs | *SP:* 2

4. **TASK-004: GitHub Projects Kanban doskasini sozlash**
   - *Tavsif:* `Backlog` -> `Sprint To Do` -> `In Progress` -> `Review` -> `Done` ustunlari, avtomatik workflowlar.
   - *Qatlam:* PM / GitHub | *SP:* 2

5. **TASK-005: GitHub Label'lar va Milestone'lar tizimini yaratish**
   - *Tavsif:* `Sprint 1-4` milestonelari, `epic`, `story`, `task`, `bug`, `priority:must/should/could` yorliqlari.
   - *Qatlam:* PM / GitHub | *SP:* 1

6. **TASK-006: Foydalanuvchi talablarini yig'ish (Stakeholder Interviews)**
   - *Tavsif:* Haydovchi, Super-admin, Parkovka admini va Smena operatori talablarini tahlil qilish.
   - *Qatlam:* Tahlil / Docs | *SP:* 3

7. **TASK-007: Raqobatchilar va mavjud yechimlarni tahlil qilish**
   - *Tavsif:* Mahalliy va xorijiy smart parking tizimlari kuchli/zaif tomonlarini solishtirish.
   - *Qatlam:* Tahlil / Docs | *SP:* 2

8. **TASK-008: SRS (Software Requirements Specification) yozish**
   - *Tavsif:* Funksional va nofunksional talablarni IEEE standarti asosida rasmiylashtirish.
   - *Qatlam:* Tahlil / Docs | *SP:* 5

9. **TASK-009: Foydalanuvchi yo'li xaritasi (User Journey Map)**
   - *Tavsif:* Haydovchining kirishdan to'lov qilib chiqib ketishigacha bo'lgan qadamlari xaritasi.
   - *Qatlam:* UI/UX / Tahlil | *SP:* 2

10. **TASK-010: Sprint 1 backlogini tasdiqlash va vazifalarni taqsimlash**
    - *Tavsif:* Birinchi 2 haftalik sprint maqsadini belgilash va dasturchilarga biriktirish.
    - *Qatlam:* PM / Sprint | *SP:* 2

---

## 💻 MODUL 2: Arxitektura, DB Dizayni va C/C++ Hardware Asosi (Tasks 11–20)

11. **TASK-011: Tizimning umumiy C4 arxitektura diagrammasini chizish**
    - *Tavsif:* Python Backend API, Desktop Admin, C/C++ Simulyator va PostgreSQL o'zaro aloqa chizmasi.
    - *Qatlam:* Arxitektura | *SP:* 3

12. **TASK-012: PostgreSQL ERD (Entity Relationship Diagram) ishlab chiqish**
    - *Tavsif:* Barcha modellar (`users`, `roles`, `parking_lots`, `slots`, `sessions`, `reservations`, `payments`).
    - *Qatlam:* PostgreSQL / DB | *SP:* 5

13. **TASK-013: DB Indekslash va Cheklovlar (Constraints) strategiyasi**
    - *Tavsif:* Mashina raqamlari, slot holati va vaqt oraliqlari bo'yicha tezkor qidiruv indekslari.
    - *Qatlam:* PostgreSQL / DB | *SP:* 3

14. **TASK-014: C/C++ va Python o'rtasidagi aloqa protokolini loyihalash**
    - *Tavsif:* TCP Socket, IPC yoki REST orqali tezkor binar/JSON xabarlar almashish spetsifikatsiyasi.
    - *Qatlam:* C/C++ / Python | *SP:* 4

15. **TASK-015: Ma'lumotlar bazasi migratsiya mexanizmini sozlash (Alembic)**
    - *Tavsif:* Python backendda Alembic orqali versiyalangan DB migratsiyalarini yo'lga qo'yish.
    - *Qatlam:* Python / DB | *SP:* 3

16. **TASK-016: API shartnomasi va ma'lumotlar sxemalarini (Pydantic) yaratish**
    - *Tavsif:* Barcha request/response DTO obyektlarini qat'iy tiplashtirish.
    - *Qatlam:* Python / API | *SP:* 3

17. **TASK-017: Tizim audit loglari arxitekturasi**
    - *Tavsif:* Operatorlar va adminlarning har bir xatti-harakatini bazaga yozib boruvchi log arxitekturasi.
    - *Qatlam:* DB / Security | *SP:* 2

18. **TASK-018: Xatoliklarni markazlashgan qayta ishlash moduli (Error Handling)**
    - *Tavsif:* Global exception handler, xato kodlari (RFC 7807 standarti).
    - *Qatlam:* Python / Core | *SP:* 2

19. **TASK-019: C/C++ hardware drayver interfeysi abstraksiyasi (HAL)**
    - *Tavsif:* Haqiqiy barrier/sensorlar kelganda kodni o'zgartirmaslik uchun Hardware Abstraction Layer.
    - *Qatlam:* C/C++ | *SP:* 5

20. **TASK-020: Arxitektura hujjatini (ARCHITECTURE.md) yangilash**
    - *Tavsif:* Qabul qilingan arxitektura qarorlarini (ADR) repo ichida hujjatlashtirish.
    - *Qatlam:* Docs | *SP:* 2

---

## ⚙️ MODUL 3: Dasturlash Muhiti, Docker va CI/CD (Tasks 21–30)

21. **TASK-021: Repozitoriya papkalar strukturasini standartlashtirish**
    - *Tavsif:* `/backend`, `/desktop-admin`, `/simulator-cpp`, `/docs` monorepo yoki modulli strukturasi.
    - *Qatlam:* DevOps / Git | *SP:* 2

22. **TASK-022: `.env.example` va konfiguratsiya boshqaruv tizimi**
    - *Tavsif:* Muhit o'zgaruvchilari (Development, Test, Production) xavfsiz boshqaruvi.
    - *Qatlam:* DevOps / Python | *SP:* 2

23. **TASK-023: PostgreSQL va Redis uchun `docker-compose.yml` sozlash**
    - *Tavsif:* Barcha ishlab chiquvchilar uchun 1 ta buyruq bilan ma'lumotlar bazasini ko'tarish.
    - *Qatlam:* Docker | *SP:* 3

24. **TASK-024: Python Backend uchun Dockerfile yaratish**
    - *Tavsif:* Multi-stage build, minimal xavfsiz alpine/slim imij.
    - *Qatlam:* Docker | *SP:* 3

25. **TASK-025: C/C++ Simulyatori uchun CMake va build skriptlarini sozlash**
    - *Tavsif:* CMakeLists.txt, avtomatik kompilyatsiya va binar fayllarni chiqarish.
    - *Qatlam:* C/C++ / Build | *SP:* 3

26. **TASK-026: Kod sifatini tekshiruvchi Linterni sozlash (Ruff / Black / Clang-Format)**
    - *Tavsif:* PEP8 va C++ Google kod uslubini majburiy tekshirish qoidalari.
    - *Qatlam:* CI / Quality | *SP:* 2

27. **TASK-027: Pre-commit hooklarni sozlash**
    - *Tavsif:* Commit qilishdan oldin formatlash va maxfiy ma'lumotlar (.env leak) yo'qligini tekshirish.
    - *Qatlam:* Git / Hooks | *SP:* 2

28. **TASK-028: GitHub Actions CI workflow (Python & C++ testlari)**
    - *Tavsif:* Har bir Pull Request ochilganda testlar va lint avtomatik yugurishi.
    - *Qatlam:* CI / GitHub | *SP:* 4

29. **TASK-029: Test ma'lumotlari generatori (DB Seeder)**
    - *Tavsif:* 100 ta sinov foydalanuvchisi, 3 ta parkovka va 150 ta slotni bazaga avtomatik kiritish.
    - *Qatlam:* Python / Seed | *SP:* 3

30. **TASK-030: Lokal dasturchi yo'riqnomasi (CONTRIBUTING & Setup Guide)**
    - *Tavsif:* Yangi dasturchi kelganda loyihani 15 daqiqada ishga tushirish qo'llanmasi.
    - *Qatlam:* Docs | *SP:* 2

---

## 👥 MODUL 4: Foydalanuvchilar, RBAC Rollar va Auth (Tasks 31–40)

31. **TASK-031: Foydalanuvchilar va Rollar DB jadvallarini yaratish**
    - *Tavsif:* `users`, `roles`, `user_roles`, `permissions` jadvallari va migratsiyalari.
    - *Qatlam:* DB / Models | *SP:* 3

32. **TASK-032: Rollar matritsasini realizatsiya qilish (RBAC)**
    - *Tavsif:* 1 ta Super-Admin, 2 ta Admin (filial), 5 ta Operator (smena) va Haydovchi ruxsatlari.
    - *Qatlam:* Python / Auth | *SP:* 4

33. **TASK-033: Parollarni xavfsiz hash qilish (Argon2 / BCrypt)**
    - *Tavsif:* Tuz (salt) bilan parollarni xavfsiz saqlash va tekshirish servisi.
    - *Qatlam:* Security / Core | *SP:* 2

34. **TASK-034: JWT token autentifikatsiyasi (Access & Refresh Token)**
    - *Tavsif:* Qisqa muddatli Access token (15 min) va xavfsiz Refresh token (7 kun) mexanizmi.
    - *Qatlam:* Python / Auth | *SP:* 4

35. **TASK-035: Role-based Permission Middleware / Dependency Injection**
    - *Tavsif:* `@requires_role(Role.SUPER_ADMIN)` dekoratori yoki FastAPI dependency nazorati.
    - *Qatlam:* Python / API | *SP:* 3

36. **TASK-036: Haydovchi ro'yxatdan o'tish (SMS / Telefon tasdiqlash mock)**
    - *Tavsif:* Telefon raqam orqali tezkor SMS OTP tasdiqlash logikasi.
    - *Qatlam:* Python / API | *SP:* 3

37. **TASK-037: Foydalanuvchi profili va avtomobillarni saqlash API**
    - *Tavsif:* Davlat raqami, mashina modeli va rangini profilga biriktirish CRUD.
    - *Qatlam:* Python / API | *SP:* 3

38. **TASK-038: Admin tomonidan operatorlarni yaratish va smenaga biriktirish API**
    - *Tavsif:* Super-admin va Admin yangi 5 ta operator akkauntlarini ochishi va parolini boshqarishi.
    - *Qatlam:* Python / API | *SP:* 3

39. **TASK-039: Akkauntni bloklash va sessiyalarni bekor qilish API**
    - *Tavsif:* Xavfsizlik buzilganda yoki operator ishdan bo'shatilganda darhol tokenlarni blacklistga kiritish.
    - *Qatlam:* Python / Redis | *SP:* 3

40. **TASK-040: Auth moduli uchun to'liq Unit va Integratsion testlar**
    - *Tavsif:* Noto'g'ri parol, muddati o'tgan token, huquqi yetmagan rol holatlarini testlash.
    - *Qatlam:* Testing / QA | *SP:* 4

---

## 📟 MODUL 5: C/C++ va Python Sensor Simulyatori (CLI Oqimi) (Tasks 41–50)

41. **TASK-041: C/C++ Simulyatori asosiy arxitekturasini qurish**
    - *Tavsif:* Multi-threaded yoki asinxron arxitektura: virtual datchiklar holatini boshqarish.
    - *Qatlam:* C/C++ / Core | *SP:* 5

42. **TASK-042: O'zbekiston avtomobil raqamlari tasodifiy generatori**
    - *Tavsif:* `01 A 777 AA`, `10 123 BBA` formatidagi haqiqiy davlat raqamlarini generatsiya qilish.
    - *Qatlam:* C/C++ / Python | *SP:* 2

43. **TASK-043: CLI konsol foydalanuvchi interfeysi (Interactive Terminal Dashboard)**
    - *Tavsif:* Terminalda chiroyli ASCII/ANSI formatida joriy mashinalar, tezlik va holatlarni ko'rsatish.
    - *Qatlam:* CLI / C++ | *SP:* 3

44. **TASK-044: Tasodifiy mashinalar kirish/chiqish oqimi generatori (Poisson Distribution)**
    - *Tavsif:* Real hayotga o'xshash: ertalab va kechqurun gavjum, tushda o'rtacha trafik oqimi.
    - *Qatlam:* C/C++ / Algoritm | *SP:* 4

45. **TASK-045: Virtual slot datchiklari holatini boshqarish (Free / Occupied)**
    - *Tavsif:* Har bir joy uchun virtual ultratovush datchigi: avto joylashganda `OCCUPIED`, chiqsa `FREE`.
    - *Qatlam:* C/C++ | *SP:* 3

46. **TASK-046: Backend API bilan TCP Socket / HTTP Client aloqasi**
    - *Tavsif:* C/C++ simulyatoridan Python Backendga tezkor kirish/chiqish hodisalarini (events) yuborish.
    - *Qatlam:* C/C++ / Network | *SP:* 4

47. **TASK-047: CLI orqali simulyator tezligi va parametrlarini boshqarish**
    - *Tavsif:* Konsoldan buyruqlar: `--rate=10` (daqiqa tezligi), `--cars=50`, `--chaos-mode` (nosozliklar).
    - *Qatlam:* CLI / Args | *SP:* 3

48. **TASK-048: Virtual Shlagbaum holati simulyatsiyasi (Barrier State)**
    - *Tavsif:* Signal kelganda ochilish (OPENING -> OPEN -> CLOSING -> CLOSED) vaqt sikllari.
    - *Qatlam:* C/C++ | *SP:* 3

49. **TASK-049: Simulyator nosozliklari va zaxira holatlarini testlash (Edge Cases)**
    - *Tavsif:* Raqam o'qilmay qolishi (no-plate event) va zaxira QR kod generatsiyasiga signal berish.
    - *Qatlam:* C/C++ / Test | *SP:* 3

50. **TASK-050: Simulyatorni ishga tushirish bo'yicha CLI qo'llanma (SIMULATOR_README.md)**
    - *Tavsif:* Dasturchi va testerlar simulyatorni qanday ishga tushirishi bo'yicha to'liq qo'llanma.
    - *Qatlam:* Docs | *SP:* 2

---

## 🚗 MODUL 6: Parkovka Boshqaruvi va Real-Vaqt Slotlar (Tasks 51–60)

51. **TASK-051: `ParkingLot` va `ParkingSpot` DB modellarini to'liq yaratish**
    - *Tavsif:* Qavatlar, zonalar (A, B, C), slot raqamlari, koordinatalari va tarif bog'lanmalari.
    - *Qatlam:* DB / Models | *SP:* 3

52. **TASK-052: Parkovkalar va zonalar CRUD API**
    - *Tavsif:* Yangi parkovka qo'shish, slotlar sonini belgilash, koordinatalarni saqlash API.
    - *Qatlam:* Python / API | *SP:* 3

53. **TASK-053: Parkovka faol sessiyalari moduli (`ParkingSession`)**
    - *Tavsif:* Kirgan avtomobil uchun sessiya ochish (`ACTIVE`), kirish vaqti va eshigini yozish.
    - *Qatlam:* Python / Core | *SP:* 4

54. **TASK-054: Simulyatordan kelgan kirish xabarini qayta ishlash Webhook/Ingress**
    - *Tavsif:* C++ simulyatordan raqam kelganda bo'sh slotni avtomatik biriktirish va sessiyani boshlash.
    - *Qatlam:* Python / Engine | *SP:* 4

55. **TASK-055: Chiqish hodisasi va sessiyani yopish logikasi**
    - *Tavsif:* Mashina chiqish to'sig'iga kelganda sessiyani tekshirish, pulni hisoblash va slotni bo'shatish.
    - *Qatlam:* Python / Engine | *SP:* 4

56. **TASK-056: Real-vaqt WebSocket serverini sozlash (FastAPI WebSockets)**
    - *Tavsif:* Har bir slot holati o'zgarganda ulangan Desktop ilovalarga 500ms ichida signal tarqatish.
    - *Qatlam:* Python / WebSocket | *SP:* 5

57. **TASK-057: Zaxira Polling API (Long-Polling Fallback)**
    - *Tavsif:* Agar WebSocket uzilib qolsa, desktop ilova uchun tezkor keshdan oxirgi holatni olish.
    - *Qatlam:* Python / Redis | *SP:* 3

58. **TASK-058: Parkovka xaritasi va slotlar joylashuv sxemasi ma'lumotlar modeli**
    - *Tavsif:* Desktop panelda chizish uchun har bir slotning (X, Y) koordinatalari va burchagi.
    - *Qatlam:* DB / JSON | *SP:* 3

59. **TASK-059: Zaxira QR kod yaratish va tekshirish servisi**
    - *Tavsif:* Raqam o'qilmagan holatlarda shifrlangan bir martalik QR chipta generatsiya qilish API.
    - *Qatlam:* Python / QR | *SP:* 3

60. **TASK-060: Slot boshqaruvi va sessiyalar bo'yicha integratsion testlar**
    - *Tavsif:* 50 ta avtomobil bir vaqtda kirib-chiqqanda poyga holati (race condition) yo'qligini tekshirish.
    - *Qatlam:* QA / Testing | *SP:* 4

---

## 📅 MODUL 7: Joy Band Qilish (Booking & Reservation) (Tasks 61–70)

61. **TASK-061: `Reservation` ma'lumotlar bazasi modelini yaratish**
    - *Tavsif:* `user_id`, `slot_id`, `start_time`, `end_time`, `status: PENDING/CONFIRMED/EXPIRED/CANCELLED`.
    - *Qatlam:* DB / Models | *SP:* 3

62. **TASK-062: Vaqt to'qnashuvini (Overlap Conflict) tekshirish algoritmi**
    - *Tavsif:* PostgreSQL `tstzrange` va `EXCLUDE` cheklovi orqali bitta slotga 2 kishi tushishini nolga tushirish.
    - *Qatlam:* DB / Algoritm | *SP:* 4

63. **TASK-063: Joyni oldindan bron qilish API (Create Reservation)**
    - *Tavsif:* Haydovchi vaqt oralig'ini tanlab, bo'sh joyni ma'lum muddatga ushlab turish so'rovi.
    - *Qatlam:* Python / API | *SP:* 4

64. **TASK-064: Bron qilishda ushlab turish vaqti (Hold Timeout) mexanizmi**
    - *Tavsif:* To'lov yoki tasdiq bo'lmasa, 10 daqiqadan so'ng vaqtincha band qilingan joyni avtomatik ochib yuborish.
    - *Qatlam:* Redis / Celery | *SP:* 4

65. **TASK-065: Bronni bekor qilish (Cancellation) API**
    - *Tavsif:* Foydalanuvchi yoki admin tomonidan bronni bekor qilish va qaytarish qoidalari.
    - *Qatlam:* Python / API | *SP:* 3

66. **TASK-066: Muddati o'tgan bronlarni tozalovchi fon vazifasi (Background Worker)**
    - *Tavsif:* Belgilangan vaqtdan 15 daqiqa o'tib kelmagan avtomobillar bronini `EXPIRED` qilish.
    - *Qatlam:* Python / Worker | *SP:* 3

67. **TASK-067: Bron qilingan avtomobil kirganda avtomatik tutashtirish**
    - *Tavsif:* Simulyatordan mashina raqami kelganda, uning faol broni bo'lsa, uni to'g'ri o'z slotiga yo'naltirish.
    - *Qatlam:* Python / Logic | *SP:* 4

68. **TASK-068: Haydovchining shaxsiy bronlar tarixi API**
    - *Tavsif:* O'tgan, joriy va rejadagi band qilingan joylar ro'yxatini sahifalab (pagination) olish.
    - *Qatlam:* Python / API | *SP:* 2

69. **TASK-069: Bron qilish qoidalarini sozlash (Admin Config)**
    - *Tavsif:* Necha soat oldin bron qilish mumkinligi va eng kam/ko'p vaqt chegaralarini belgilash.
    - *Qatlam:* Python / Admin | *SP:* 2

70. **TASK-070: Booking moduli uchun yuklama va konkurentlik (Concurrency) testlari**
    - *Tavsif:* 1 ta oxirgi bo'sh joyga bir vaqtda 20 ta so'rov kelganda to'g'ri ishlashini sinovdan o'tkazish.
    - *Qatlam:* QA / Load Test | *SP:* 4

---

## 💳 MODUL 8: Tariflar va To'lov Tizimi (Payme / Click Sandbox) (Tasks 71–80)

71. **TASK-071: Moslashuvchan tariflar ma'lumotlar bazasi modeli (`Tariff`)**
    - *Tavsif:* Bepul daqiqalar (Grace period: 15 min), soatlik stavka, kunlik maksimal chegara, kechki tarif.
    - *Qatlam:* DB / Models | *SP:* 3

72. **TASK-072: Avtomatik narx hisoblash biznes logikasi funksiyasi**
    - *Tavsif:* Kirish va chiqish daqiqalariga qarab 100% aniqlikda so'mda hisoblash algoritmi.
    - *Qatlam:* Python / Billing | *SP:* 4

73. **TASK-073: To'lov tranzaksiyalari modeli (`PaymentTransaction`)**
    - *Tavsif:* `provider: PAYME/CLICK`, `amount`, `status: PENDING/PAID/FAILED/REFUNDED`, `fiscal_sign`.
    - *Qatlam:* DB / Models | *SP:* 3

74. **TASK-074: Payme Sandbox Merchant API integratsiyasi**
    - *Tavsif:* `CheckPerformTransaction`, `CreateTransaction`, `PerformTransaction` metodlari realizatsiyasi.
    - *Qatlam:* Python / Payme | *SP:* 5

75. **TASK-075: Click Sandbox Shop API integratsiyasi**
    - *Tavsif:* `Prepare` va `Complete` so'rovlarini qabul qiluvchi xavfsiz webhook endpointlari.
    - *Qatlam:* Python / Click | *SP:* 5

76. **TASK-076: O'zbekiston Davlat Soliq Qo'mitasi Fiskal Chek ma'lumotlari modeli**
    - *Tavsif:* MXIK kodi, QQS stavkasi, fiskal belgi, QR-link simulyatsiya modeli.
    - *Qatlam:* Python / Fiscal | *SP:* 4

77. **TASK-077: Chiqish uchun bepul oraliq (Exit Grace Window)**
    - *Tavsif:* To'lov amalga oshirilgach, mashina chiqib ketishi uchun 10-15 daqiqa bepul vaqt berish logikasi.
    - *Qatlam:* Python / Billing | *SP:* 3

78. **TASK-078: Tranzaksiya holatini tekshirish va to'lov kvitansiyasi API**
    - *Tavsif:* To'lov muvaffaqiyatli o'tgach raqamli chek ma'lumotlarini JSON/PDF shaklda qaytarish.
    - *Qatlam:* Python / API | *SP:* 3

79. **TASK-079: To'lov qaytarish (Refund) va xatoliklarni qayta ishlash mexanizmi**
    - *Tavsif:* Sessiya xato bo'lganda yoki bekor qilinganda tranzaksiyani xavfsiz yopish.
    - *Qatlam:* Python / Billing | *SP:* 3

80. **TASK-080: To'lov va hisob-kitoblar bo'yicha to'liq Unit testlar**
    - *Tavsif:* Barcha vaqt kesimlari (14 min -> 0 so'm, 65 min -> 2 soatlik narx va h.k.) bo'yicha testlar.
    - *Qatlam:* QA / Test | *SP:* 4

---

## 🖥️ MODUL 9: Desktop Admin Panel (Desktop GUI) (Tasks 81–90)

81. **TASK-081: Desktop Admin ilovasi karkasini sozlash (PyQt / PySide / Electron)**
    - *Tavsif:* Asosiy oyna, navigatsiya paneli, zamonaviy qorong'i/yorug' mavzular.
    - *Qatlam:* Desktop / UI | *SP:* 4

82. **TASK-082: Desktop ilovada kirish va rollar bo'yicha cheklovlar**
    - *Tavsif:* Super-Admin, 2 ta Admin va 5 ta Smena Operatorlari uchun ruxsat berilgan menyularni ko'rsatish.
    - *Qatlam:* Desktop / Auth | *SP:* 4

83. **TASK-083: Operator oynasi: Jonli Kirish/Chiqish monitori (Live Traffic)**
    - *Tavsif:* Oxirgi kirgan avtomobillar ro'yxati, davlat raqami, vaqti va biriktirilgan sloti.
    - *Qatlam:* Desktop / UI | *SP:* 5

84. **TASK-084: Operator uchun shlagbaumni qo'lda ochish tugmasi (Manual Override)**
    - *Tavsif:* Favqulodda holatda operator bitta tugma bilan shlagbaumni ochishi va sababini yozishi (Audit).
    - *Qatlam:* Desktop / Action | *SP:* 3

85. **TASK-085: 2D Interaktiv Parkovka Slotlari xaritasi (Visual Grid)**
    - *Tavsif:* Yashil (Bo'sh), Qizil (Band), Sariq (Bron) ranglarda jonli yangilanuvchi slotlar sxemasi.
    - *Qatlam:* Desktop / Canvas | *SP:* 5

86. **TASK-086: Admin uchun Parkovka va Slotlar CRUD tahrirlash oynasi**
    - *Tavsif:* 2 ta Admin o'z filialidagi slotlarni tahrirlashi, vaqtincha yopishi yoki ta'mirlash holatiga o'tkazishi.
    - *Qatlam:* Desktop / CRUD | *SP:* 4

87. **TASK-087: Super-Admin uchun Xodimlar (Operatorlar) boshqaruv bo'limi**
    - *Tavsif:* Yangi operatorlarni qo'shish, smenaga tayinlash, parolini yangilash interfeysi.
    - *Qatlam:* Desktop / Admin | *SP:* 3

88. **TASK-088: Moliyaviy tahlil va daromadlar dashboardi (Charts & Stats)**
    - *Tavsif:* Kunlik, haftalik tushumlar, Payme/Click to'lovlari taqsimoti, eng gavjum soatlar grafigi.
    - *Qatlam:* Desktop / Charts | *SP:* 4

89. **TASK-089: Hisobotlarni Excel va PDF formatida eksport qilish**
    - *Tavsif:* Smena hisoboti, moliya va to'lovlar reyestrini faylga yuklab olish moduli.
    - *Qatlam:* Desktop / Export | *SP:* 3

90. **TASK-090: Desktop ilovani Windows uchun o'rnatuvchi (Installer / .exe) paketlash**
    - *Tavsif:* PyInstaller yoki Inno Setup orqali operatorlar kompyuteriga o'rnatiladigan tayyor `.exe`.
    - *Qatlam:* Desktop / Build | *SP:* 4

---

## 🛡️ MODUL 10: Sifat Nazorati (QA), Xavfsizlik va Taqdimot (Tasks 91–100)

91. **TASK-091: E2E (End-to-End) Tizimli test-case'lar yozish**
    - *Tavsif:* "Mashina keldi -> Simulyator bildirdi -> Slot band bo'ldi -> Chiqdi -> Payme to'landi -> Shlagbaum ochildi".
    - *Qatlam:* QA / E2E | *SP:* 5

92. **TASK-092: API Rate Limiting va Brute-Force himoyasi**
    - *Tavsif:* Login va to'lov endpointlariga limit o'rnatish (masalan: daqiqasiga 10 ta so'rov).
    - *Qatlam:* Security / Python | *SP:* 3

93. **TASK-093: SQL Injection va XSS xavfsizlik auditi**
    - *Tavsif:* Barcha kiruvchi parametrlarni Pydantic va SQLAlchemy orqali to'liq sanitizatsiya qilish.
    - *Qatlam:* Security / Audit | *SP:* 3

94. **TASK-094: Tarmoq uzilishi va tizim tiklanishi (Disaster Recovery Test)**
    - *Tavsif:* Simulyator yoki baza 30 soniyaga o'chib qolganda tizimning xatosiz qayta tiklanishini sinash.
    - *Qatlam:* Reliability / QA | *SP:* 4

95. **TASK-095: API Swagger / OpenAPI hujjatlarini to'liq tavsiflash**
    - *Tavsif:* `/docs` sahifasida har bir endpoint uchun namunaviy JSON, tavsif va xato kodlarini keltirish.
    - *Qatlam:* Docs / OpenAPI | *SP:* 3

96. **TASK-096: Operator va Admin uchun qo'llanma (User Manual)**
    - *Tavsif:* Desktop ilovadan foydalanish bo'yicha skrinshotli PDF yo'riqnoma.
    - *Qatlam:* Docs / Guide | *SP:* 3

97. **TASK-097: Ishga tushirish va deploy qilish bo'yicha DevOps qo'llanmasi**
    - *Tavsif:* Serverda barcha konteynerlar va simulyatorni bir martada ishga tushirish yo'riqnomasi.
    - *Qatlam:* DevOps / Docs | *SP:* 2

98. **TASK-098: Loyiha GitHub README va arxitektura fayllarini yakuniy yangilash**
    - *Tavsif:* Barcha havolalar, status belgilari (badges) va jamoa ma'lumotlarini to'ldirish.
    - *Qatlam:* Docs / GitHub | *SP:* 2

99. **TASK-099: Jonli Demo ssenariysi va video taqdimot tayyorlash**
    - *Tavsif:* Simulyator va Desktop Admin birgalikda real vaqtda ishlashini ko'rsatuvchi 3-5 daqiqalik demo.
    - *Qatlam:* Presentation / Demo | *SP:* 4

100. **TASK-100: Yakuniy loyiha himoyasi slaydlari (Pitch Deck / Presentation)**
     - *Tavsif:* Muammo, yechim, arxitektura, C++/Python simulyator yutug'i va moliyaviy natijalarni jamlagan slaydlar.
     - *Qatlam:* Presentation / PPTX | *SP:* 4
