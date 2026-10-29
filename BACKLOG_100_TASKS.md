# 📋 Parkly.uz — Top 100 Mukammal Backlog Tasklar Ro'yxati

> **Loyiha:** Parkly.uz — Smart Parking Management System  
> **Texnologik stek:** Python (FastAPI/Core API), PostgreSQL / SQLite, C/C++ (Hardware/Simulyator datchiklar boshqaruvi)  
> **Kamera va ANPR:** Real-time RTSP/IP Kameralar, Two-Stage Detektor, Temporal Voting va **10 daqiqalik maksimal kutish SLA'si (User Wait Max 10 Min)**  
> **Admin panel:** Desktop ilova (2 ta Super-Admin, 4 ta Oddiy Admin, 2 ta Smena Operatori)  
> **Navigatsiyada 4-o'rin:** 💳 **Moliya va Tranzaksiyalar bo'limi** (Kunlik/haftalik/oylik tushum, 7 kunlik bar chart, Excel UTF-8 BOM eksport, Super-Admin tariflari)  
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
   - *Tavsif:* Texnik (kamera uzilishi, 10 daqiqa SLA buzilishi, simulyator kechikishi) va tashkiliy xatarlar reestri.
   - *Qatlam:* PM / Docs | *SP:* 2

4. **TASK-004: Taskcafe & GitHub Projects Kanban doskasini sozlash**
   - *Tavsif:* `Product Backlog` -> `Sprint Ready` -> `In Progress` -> `Review & QA` -> `Done` ustunlari, SLA taymerlari va swimlanelar.
   - *Qatlam:* PM / GitHub / Taskcafe | *SP:* 2

5. **TASK-005: GitHub Label'lar va Milestone'lar tizimini yaratish**
   - *Tavsif:* `Sprint 1-4` milestonelari, `epic`, `story`, `task`, `bug`, `priority:p0/p1/p2/p3`, `sla:max-10min` yorliqlari.
   - *Qatlam:* PM / GitHub | *SP:* 1

6. **TASK-006: Foydalanuvchi talablarini yig'ish (Stakeholder Interviews)**
   - *Tavsif:* Haydovchi, Super-admin (2 kishi), Oddiy admin (4 kishi) va Smena operatori (2 kishi) talablarini tahlil qilish.
   - *Qatlam:* Tahlil / Docs | *SP:* 3

7. **TASK-007: Raqobatchilar va mavjud yechimlarni tahlil qilish**
   - *Tavsif:* Mahalliy va xorijiy smart parking tizimlari kuchli/zaif tomonlarini solishtirish.
   - *Qatlam:* Tahlil / Docs | *SP:* 2

8. **TASK-008: SRS (Software Requirements Specification) yozish**
   - *Tavsif:* Funksional va nofunksional talablarni (shu jumladan 10 minutlik kutish SLA) IEEE standarti asosida rasmiylashtirish.
   - *Qatlam:* Tahlil / Docs | *SP:* 5

9. **TASK-009: Foydalanuvchi yo'li xaritasi (User Journey Map)**
   - *Tavsif:* Haydovchining kirishdan to'lov qilib chiqib ketishigacha bo'lgan qadamlari va maksimal kutish oraliqlari xaritasi.
   - *Qatlam:* UI/UX / Tahlil | *SP:* 2

10. **TASK-010: Sprint 1 backlogini tasdiqlash va vazifalarni taqsimlash**
    - *Tavsif:* Birinchi 2 haftalik sprint maqsadini belgilash va dasturchilarga biriktirish.
    - *Qatlam:* PM / Sprint | *SP:* 2

---

## 💻 MODUL 2: Arxitektura, DB Dizayni va C/C++ Hardware Asosi (Tasks 11–20)

11. **TASK-011: Tizimning umumiy C4 arxitektura diagrammasini chizish**
    - *Tavsif:* Python Backend API, Desktop Admin, C/C++ Simulyator va PostgreSQL/SQLite o'zaro aloqa chizmasi.
    - *Qatlam:* Arxitektura | *SP:* 3

12. **TASK-012: PostgreSQL ERD (Entity Relationship Diagram) ishlab chiqish**
    - *Tavsif:* Barcha modellar (`users`, `roles`, `parking_lots`, `slots`, `sessions`, `transactions`, `tariffs`).
    - *Qatlam:* PostgreSQL / DB | *SP:* 5

13. **TASK-013: DB Indekslash va Cheklovlar (Constraints) strategiyasi**
    - *Tavsif:* Mashina raqamlari, slot holati va vaqt oraliqlari bo'yicha tezkor qidiruv indekslari.
    - *Qatlam:* PostgreSQL / DB | *SP:* 3

14. **TASK-014: C/C++ va Python o'rtasidagi aloqa protokolini loyihalash**
    - *Tavsif:* TCP Socket, IPC yoki REST orqali tezkor binar/JSON xabarlar almashish spetsifikatsiyasi.
    - *Qatlam:* C/C++ / Python | *SP:* 4

15. **TASK-015: Ma'lumotlar bazasi migratsiya mexanizmini sozlash**
    - *Tavsif:* Schema migratsiyalari va avtomatik seeder (2 Super-Admin, 4 Oddiy Admin, 2 Operator) yozish.
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

## ⚙️ MODUL 3: Dasturlash Muhiti va CI/CD (Tasks 21–30)

21. **TASK-021: Repozitoriya papkalar strukturasini standartlashtirish**
    - *Tavsif:* `/backend`, `/desktop_admin`, `/simulator`, `/tests`, `/docs` toza va modulli strukturasi.
    - *Qatlam:* DevOps / Git | *SP:* 2

22. **TASK-022: `.env.example` va konfiguratsiya boshqaruv tizimi**
    - *Tavsif:* Muhit o'zgaruvchilari (Development, Test, Production) xavfsiz boshqaruvi.
    - *Qatlam:* DevOps / Python | *SP:* 2

23. **TASK-023: Lokal PostgreSQL va Redis serverini native o'rnatish va sozlash**
    - *Tavsif:* Ishlab chiquvchilar uchun to'g'ridan-to'g'ri operatsion tizimda DB va Cache muhitini tayyorlash.
    - *Qatlam:* Native Setup | *SP:* 3

24. **TASK-024: Python virtual environment va paketlar menejmenti**
    - *Tavsif:* venv yaratish va talab qilinadigan kutubxonalarni sozlash.
    - *Qatlam:* Python | *SP:* 2

25. **TASK-025: C/C++ simulyatori uchun CMakeLists.txt sozlash**
    - *Tavsif:* CMakeLists.txt, Qt5/Qt6 bog'lamalari va avtomatik kompilyatsiya.
    - *Qatlam:* C/C++ / Build | *SP:* 3

26. **TASK-026: Python virtual environment va `requirements.txt` ni yangilash**
    - *Tavsif:* PyQt6, opencv-python, numpy, pydantic, sqlalchemy, pytest paketlarini aniq versiyalar bilan yozish.
    - *Qatlam:* Python / DevOps | *SP:* 1

27. **TASK-027: Linter va Formatter sozlash (Ruff / Black / Clang-Format)**
    - *Tavsif:* PEP8 va Google C++ uslubini avtomatik tekshirish.
    - *Qatlam:* Code Quality | *SP:* 2

28. **TASK-028: GitHub Actions CI: Avtomatik Testlar (Workflow)**
    - *Tavsif:* Har bir PR ochilganda 20 ta unit/integratsion testlarni avtomatik ishga tushirish.
    - *Qatlam:* CI/CD | *SP:* 4

29. **TASK-029: Git Branch Protection qoidalarini joriy qilish (`main` va `Mirhamid`)**
    - *Tavsif:* Faqat PR va tasdiq (Approval) orqali merge qilish tartibi.
    - *Qatlam:* GitHub / Security | *SP:* 2

30. **TASK-030: Ishlab chiquvchi uchun tezkor start qo'llanmasi (CONTRIBUTING.md)**
    - *Tavsif:* Loyihani 5 daqiqada ishga tushirish bo'yicha yo'riqnoma.
    - *Qatlam:* Docs | *SP:* 2

---

## 👥 MODUL 4: Foydalanuvchilar, RBAC Rollar va Xavfsizlik (Tasks 31–40)

31. **TASK-031: Foydalanuvchilar va Rollar DB jadvallarini yaratish**
    - *Tavsif:* `users`, `roles`, `permissions` jadvallari va seeder.
    - *Qatlam:* DB / Models | *SP:* 3

32. **TASK-032: Huquqlar Matritsasini realizatsiya qilish (RBAC)**
    - *Tavsif:* **2 ta Super-Admin** (to'liq kirish), **4 ta Oddiy Admin** (monitoring va 4-moliya ko'rish, lekin sozlamalar/xodimlar qulflangan), **2 ta Operator** (smena nazorati).
    - *Qatlam:* Python / Auth | *SP:* 4

33. **TASK-033: Parollarni xavfsiz hash qilish (Argon2 / BCrypt)**
    - *Tavsif:* Tuz (salt) bilan parollarni xavfsiz saqlash va tekshirish servisi.
    - *Qatlam:* Security / Core | *SP:* 2

34. **TASK-034: JWT token autentifikatsiyasi (Access & Refresh Token)**
    - *Tavsif:* Qisqa muddatli Access token (15 min) va xavfsiz Refresh token (7 kun) mexanizmi.
    - *Qatlam:* Python / Auth | *SP:* 4

35. **TASK-035: Role-based Permission Guard Middleware**
    - *Tavsif:* Oddiy admin yoki operator ruxsatsiz bo'limga kirganda 403 Forbidden berish.
    - *Qatlam:* Python / API | *SP:* 3

36. **TASK-036: Haydovchi profili va avtomobillarni saqlash API**
    - *Tavsif:* Davlat raqami, mashina modeli va rangini profilga biriktirish CRUD.
    - *Qatlam:* Python / API | *SP:* 3

37. **TASK-037: Super-Admin tomonidan admin va operatorlarni yaratish API**
    - *Tavsif:* Faqat Super-Admin yangi 4 ta admin va 2 ta operator akkauntlarini ochishi va o'chirishi.
    - *Qatlam:* Python / API | *SP:* 3

38. **TASK-038: Smenalarni boshqarish va navbatchilik logikasi**
    - *Tavsif:* Smena 1 (08:00 - 20:00) va Smena 2 (20:00 - 08:00) operatorlarini biriktirish.
    - *Qatlam:* Python / API | *SP:* 3

39. **TASK-039: Akkauntni bloklash va sessiyalarni bekor qilish API**
    - *Tavsif:* Xavfsizlik buzilganda darhol tokenlarni blacklistga kiritish.
    - *Qatlam:* Python / Redis | *SP:* 3

40. **TASK-040: RBAC va Auth moduli uchun to'liq Unit testlar**
    - *Tavsif:* Super-Admin ruxsatlari, Oddiy Admin cheklovlari va Operator taqiqlari testlari.
    - *Qatlam:* Testing / QA | *SP:* 4

---

## 📟 MODUL 5: C/C++ va Python Sensor Simulyatori (Tasks 41–50)

41. **TASK-041: Sensor simulyatori dvigatelini qurish**
    - *Tavsif:* Multi-threaded arxitektura: virtual datchiklar oqimini yaratish.
    - *Qatlam:* C/C++ / Python | *SP:* 5

42. **TASK-042: O'zbekiston avtomobil raqamlari tasodifiy generatori**
    - *Tavsif:* `01 A 777 AA`, `10 123 BBA` formatidagi davlat raqamlarini generatsiya qilish.
    - *Qatlam:* C/C++ / Python | *SP:* 2

43. **TASK-043: CLI konsol foydalanuvchi interfeysi (UTF-8 Xavfsiz)**
    - *Tavsif:* Windows terminallarida `UnicodeEncodeError` bermaydigan toza ANSI jadvali.
    - *Qatlam:* CLI / Python | *SP:* 3

44. **TASK-044: Tasodifiy mashinalar kirish/chiqish oqimi generatori**
    - *Tavsif:* Real hayotga o'xshash: ertalab va kechqurun gavjum, tushda o'rtacha trafik oqimi.
    - *Qatlam:* Algoritm | *SP:* 4

45. **TASK-045: Virtual slot datchiklari holatini boshqarish (Free / Occupied)**
    - *Tavsif:* Har bir joy uchun virtual datchik: avto joylashganda `OCCUPIED`, chiqsa `FREE`.
    - *Qatlam:* C/C++ | *SP:* 3

46. **TASK-046: Backend API bilan tezkor aloqa (Socket / REST Client)**
    - *Tavsif:* Simulyatordan Python Backendga real-vaqt kirish/chiqish hodisalarini yuborish.
    - *Qatlam:* Network | *SP:* 4

47. **TASK-047: CLI orqali simulyator tezligi va parametrlarini boshqarish**
    - *Tavsif:* `--interval=2.0` (sekund tezligi) argumentlari orqali boshqarish.
    - *Qatlam:* CLI | *SP:* 2

48. **TASK-048: Virtual Shlagbaum holati simulyatsiyasi (Barrier State Machine)**
    - *Tavsif:* Ochilish va yopilish vaqt sikllari (OPENING -> OPEN -> CLOSING -> CLOSED).
    - *Qatlam:* C/C++ | *SP:* 3

49. **TASK-049: Slotlar xaritasi bilan simulyator sinxronizatsiyasi**
    - *Tavsif:* Desktop interaktiv xaritasida slot ranglari simulyator bilan bir vaqtda o'zgarishi.
    - *Qatlam:* Integration | *SP:* 4

50. **TASK-050: Simulyator barqarorligi va yuklama testlari**
    - *Tavsif:* 1000 ta mashina oqimida xotira oqib ketmasligini (Memory leak) tekshirish.
    - *Qatlam:* QA | *SP:* 3

---

## 📷 MODUL 6: Computer Vision, ANPR va Kameralar Mantiqi (Tasks 51–60)

51. **TASK-051 (CAM-01): Multi-Source Zero-Latency RTSP Streamer**
    - *Tavsif:* RTSP, IP-kamera, USB web-kamera oqimini bufer to'lib ketishisiz qabul qilish va Reconnect Watchdog.
    - *Qatlam:* OpenCV / Threading | *SP:* 5

52. **TASK-052 (CAM-02): Adaptive CLAHE & Glare Suppression**
    - *Tavsif:* Tungi qorong'ilik va faralar nurini bartaraf etuvchi dinamik yorug'lik va kontrast filtri.
    - *Qatlam:* OpenCV | *SP:* 5

53. **TASK-053 (CAM-03): Two-Stage Plate Region Detector (YOLO/Haar)**
    - *Tavsif:* Avval avtomobil korpusini, so'ngra 4.5:1 proporsiyadagi raqam to'rtburchagini ajratib olish.
    - *Qatlam:* PyTorch / OpenCV | *SP:* 8

54. **TASK-054 (CAM-04): Homography Perspective Rectification**
    - *Tavsif:* 30°–45° burchak ostida turgan qiyshiq raqam rasmini tekis to'rtburchakka aylantirish (Warp).
    - *Qatlam:* OpenCV (Homography) | *SP:* 5

55. **TASK-055 (CAM-05): Uzbekistan Plate Disambiguation OCR Engine**
    - *Tavsif:* `01 A 777 AA` va `01 123 AAA` formatlari bo'yicha harf-raqam chalkashliklarini tuzatish (`O`<->`0`, `B`<->`8`, `Z`<->`2`).
    - *Qatlam:* Regex / OCR | *SP:* 5

56. **TASK-056 (CAM-06): Multi-Frame Temporal Consensus Tracker**
    - *Tavsif:* Ketma-ket 3–5 kadr konsensusi asosida ko'pchilik ovozi bilan yakuniy raqamni tasdiqlash.
    - *Qatlam:* Python DS | *SP:* 5

57. **TASK-057 (CAM-07): Confidence Score Decision Engine**
    - *Tavsif:* `>= 85%` bo'lsa shlagbaum avto ochiladi, `< 85%` bo'lsa operator monitoriga snapshot bilan tushadi.
    - *Qatlam:* Backend / Logic | *SP:* 3

58. **TASK-058 (CAM-08): 10-Minute SLA Watchdog & Emergency Fail-Safe**
    - *Tavsif:* **Foydalanuvchi kutish vaqti ≤ 10 daqiqa:** 5-minutda sariq, 7-minutda qizil eskalatsiya, 10-minutda avtomatik favqulodda ochish.
    - *Qatlam:* Background Worker / SLA | *SP:* 5

59. **TASK-059 (CAM-09): Desktop ANPR Live Stream & Manual Override Widget**
    - *Tavsif:* Operator uchun real-vaqt video oynasi, confidence ko'rsatkichi va 1-tugmali tezkor tasdiqlash dialogi.
    - *Qatlam:* PyQt6 / Desktop | *SP:* 5

60. **TASK-060 (CAM-10): Offline Camera Fallback & Audit Logger**
    - *Tavsif:* Kamera uzilganda test rejimiga o'tish, shlagbaum harakatlarini audit bazasida qayd etish.
    - *Qatlam:* SQLite / Postgres | *SP:* 3

---

## 📅 MODUL 7: Joy Band Qilish (Booking & Reservation) (Tasks 61–70)

61. **TASK-061: Joy band qilish ma'lumotlar modeli (DB Schema)**
    - *Tavsif:* `reservations` jadvali (`slot_id`, `start_time`, `end_time`, `status`).
    - *Qatlam:* DB / Models | *SP:* 3

62. **TASK-062: Vaqt to'qnashuvini (Overlap Conflict) tekshirish algoritmi**
    - *Tavsif:* `max(start_a, start_b) < min(end_a, end_b)` qoidasi bo'yicha to'qnashuvlarni aniqlash.
    - *Qatlam:* Python / Algoritm | *SP:* 4

63. **TASK-063: Slotni oldindan bron qilish API (Create Reservation)**
    - *Tavsif:* Xavfsiz tranzaksiya orqali joyni bron qilish va unikal QR-kod tokeni generatsiya qilish.
    - *Qatlam:* Python / API | *SP:* 4

64. **TASK-064: Bron muddati tugashi va avtomatik bekor qilish (Expired Worker)**
    - *Tavsif:* Agar haydovchi belgilangan vaqtdan 15 daqiqa kechiksa, bronni bekor qilish va slotni bo'shatish.
    - *Qatlam:* Background Worker | *SP:* 4

65. **TASK-065: Bronni haydovchi tomonidan bekor qilish (Cancel Reservation) API**
    - *Tavsif:* Jarimasiz yoki jarima bilan bekor qilish logikasi.
    - *Qatlam:* Python / API | *SP:* 3

66. **TASK-066: Bron qilingan avtomobil kelganda shlagbaumni ochish logikasi**
    - *Tavsif:* ANPR raqamni o'qiganda faol bron bilan solishtirish va to'g'ridan-to'g'ri o'tkazish.
    - *Qatlam:* Gate Controller | *SP:* 3

67. **TASK-067: Bron statistikasi va bandlik prognozi**
    - *Tavsif:* Ertangi kun uchun soatlar bo'yicha bandlik ehtimolini hisoblash.
    - *Qatlam:* Analytics | *SP:* 4

68. **TASK-068: Bron tasdiqlash bildirishnomalari (SMS / Push mock)**
    - *Tavsif:* Haydovchiga manzil, slot raqami va vaqt ko'rsatilgan bildirishnoma yuborish.
    - *Qatlam:* Notifications | *SP:* 3

69. **TASK-069: Desktop Admin xaritasida bron qilingan slotlar (Sariq rang)**
    - *Tavsif:* 3D izometrik xaritada sariq indikator va bron tafsilotlari kartochkasi.
    - *Qatlam:* Desktop / Map | *SP:* 3

70. **TASK-070: Reservation Matcher uchun Unit va Stress testlar**
    - *Tavsif:* 100 ta parallel bron so'rovlarida to'qnashuv (double-booking) yuz bermasligini tekshirish.
    - *Qatlam:* Testing / QA | *SP:* 4

---

## 💳 MODUL 8: Tariflar va To'lov Tizimi (Tasks 71–80)

71. **TASK-071: Tarif modeli va hisoblash qoidalari (Tariff Engine)**
    - *Tavsif:* Kunduzgi (08:00-20:00: 5000 so'm), tungi (20:00-08:00: 3000 so'm), EV (+10000 so'm) stavkalari.
    - *Qatlam:* Python / Algoritm | *SP:* 4

72. **TASK-072: Dastlabki 15 daqiqalik bepul muddat (Grace Period)**
    - *Tavsif:* 15 daqiqa ichida kirib-chiqqan transportlar uchun to'lov summasi 0 so'm hisoblanishi.
    - *Qatlam:* Algoritm | *SP:* 2

73. **TASK-073: To'lovdan keyingi 15 daqiqalik chiqish imtiyozi (Exit Grace)**
    - *Tavsif:* To'lov qilgandan keyin shlagbaumgacha yetib borish uchun beriladigan bepul darcha.
    - *Qatlam:* Algoritm | *SP:* 3

74. **TASK-074: Payme va Click Sandbox integratsiyasi**
    - *Tavsif:* Merchant API, tranzaksiya yaratish va webhook callback qayta ishlash.
    - *Qatlam:* Billing / Integratsiya | *SP:* 5

75. **TASK-075: Tranzaksiyalar bazasi va fiskal chek modeli**
    - *Tavsif:* `transactions` jadvali (`amount`, `provider`, `duration`, `status`, `fiscal_sign`).
    - *Qatlam:* DB / Models | *SP:* 4

76. **TASK-076: Chiqishda to'lov tekshiruvi (Gate Payment Verifier)**
    - *Tavsif:* Shlagbaum oldiga kelgan transportning to'lov holatini tekshirish.
    - *Qatlam:* Gate Controller | *SP:* 3

77. **TASK-077: To'lov tizimi ishlamay qolgandagi Post-Pay himoyasi (10 Min SLA)**
    - *Tavsif:* Chiqishda bank API uzilsa, haydovchi 10 daqiqadan ko'p qolmasligi uchun elektron qarz kvitansiyasi berib chiqarish.
    - *Qatlam:* SLA / Fail-Safe | *SP:* 4

78. **TASK-078: Kassa smenasi va operator balansi hisoboti**
    - *Tavsif:* Smena yakunida naqd pul va onlayn to'lovlar summasini solishtirish.
    - *Qatlam:* Finance | *SP:* 3

79. **TASK-079: Chegirma va vaucherlar mexanizmi**
    - *Tavsif:* VIP mehmonlar va xodimlar uchun 100% yoki foizli promo-kodlar.
    - *Qatlam:* Billing | *SP:* 3

80. **TASK-080: Tariff Calculator Unit testlari**
    - *Tavsif:* Grace period, tungi/kunduzgi almashinuv, EV qo'shimchasi va kunlik maksimal to'lov testlari.
    - *Qatlam:* Testing / QA | *SP:* 4

---

## 🖥️ MODUL 9: Desktop Admin Paneli va 4-Moliya Moduli (Tasks 81–90)

81. **TASK-081: Desktop Admin karkasini sozlash (PyQt6 / C++ Qt)**
    - *Tavsif:* Zamonaviy Figma/Dribbble minimalist dizayni, container shadowlar, sidebar va header.
    - *Qatlam:* Desktop / UI | *SP:* 5

82. **TASK-082: 7 ta to'liq navigatsiya bo'limini tartiblash**
    - *Tavsif:* 1.Dashboard, 2.Xarita, 3.Kameralar, **4.Moliya va Tranzaksiyalar (aynan 4-o'rinda!)**, 5.Sessiyalar, 6.Xodimlar, 7.Sozlamalar.
    - *Qatlam:* Desktop / Navigation | *SP:* 3

83. **TASK-083: 4-Moliya moduli: Kunlik, haftalik va oylik analitika kartochkalari**
    - *Tavsif:* Deep Slate Gradient (`#0F172A` -> `#0066FF`), Payme, Click, Naqd va Uzum to'lovlari monitoringi.
    - *Qatlam:* Desktop / Finance | *SP:* 5

84. **TASK-084: 4-Moliya moduli: Native 7 kunlik bar chart grafigi**
    - *Tavsif:* So'nggi 7 kunlik daromad dinamikasi, Y-o'qi chiziqlari va joriy kun ustuni ajralib turuvchi vektorli grafik.
    - *Qatlam:* Desktop / Charts | *SP:* 5

85. **TASK-085: 4-Moliya moduli: Excel/CSV rasmiy eksporti**
    - *Tavsif:* Excelda buzilmasdan ochiladigan UTF-8 BOM (`utf-8-sig`) va `;` ajratgichli moliyaviy hisobot eksporti.
    - *Qatlam:* Desktop / Export | *SP:* 4

86. **TASK-086: 4-Moliya moduli: Super-Admin tariflarni yangilash modali**
    - *Tavsif:* Soatbay, daqiqabay, EV va tungi stavkalarni faqat Super-Admin tomonidan tahrirlash dialogi.
    - *Qatlam:* Desktop / Modal | *SP:* 4

87. **TASK-087: RBAC qulflari (Oddiy Admin uchun 6- va 7-bo'limlar qulfi 🔒)**
    - *Tavsif:* Oddiy admin kirganda Xodimlar va Sozlamalarga qulf belgisi qo'yish, bosilganda ruxsat taqiqlanganligi dialogini chiqarish.
    - *Qatlam:* Desktop / Security | *SP:* 3

88. **TASK-088: 4 qavatli 3D Izometrik xarita va avtomobil modellari**
    - *Tavsif:* Har bir qavatda avto modellari, quvvatlash stansiyasi, jonli timerlar va zoom in/out funksiyasi.
    - *Qatlam:* Desktop / 3D Map | *SP:* 8

89. **TASK-089: Jonli avto raqamlari (Monospace stiker dizayni)**
    - *Tavsif:* O'zbekiston davlat raqamlari uchun maxsus monospace ramkali stiker vizualizatsiyasi.
    - *Qatlam:* Desktop / Styling | *SP:* 2

90. **TASK-090: Windows uchun `Parkly_Admin.bat` ishga tushirish skripti**
    - *Tavsif:* Ilovani 1-klik bilan avtomatik ochuvchi terminal skripti.
    - *Qatlam:* Deployment / Windows | *SP:* 2

---

## 🛡️ MODUL 10: Sifat Nazorati (QA), Testlar va Taqdimot (Tasks 91–100)

91. **TASK-091: 20 ta Unit va Integratsion testlarni to'liq qamrab olish**
    - *Tavsif:* `test_algorithms.py`, `test_rbac_finance.py`, `test_vision_pipeline.py` testlarining 100% yashil o'tishi.
    - *Qatlam:* QA / Automation | *SP:* 4

92. **TASK-092: 10 Daqiqalik Maksimal Kutish (SLA Fail-Safe) Unit Testlari**
    - *Tavsif:* `evaluate_wait_time_sla` ning 3m, 5m, 8m va 10.5m holatlarini avtotest bilan sinash.
    - *Qatlam:* Testing / SLA | *SP:* 3

93. **TASK-093: RBAC Ruxsatlar Matritsasi avtotestlari**
    - *Tavsif:* Super-Admin 7 modulga kirishi, Oddiy Admin esa 6- va 7-moduldan bloklanishi testlari.
    - *Qatlam:* Testing / Security | *SP:* 3

94. **TASK-094: Vision & ANPR kadrlar oqimi sinovi**
    - *Tavsif:* 6.78 ms kadr tezligi, temporal voting konsensusi va O'zbekiston raqamlari regex sinovi.
    - *Qatlam:* Testing / Vision | *SP:* 3

95. **TASK-095: SQL Injection va Xavfsizlik auditi**
    - *Tavsif:* Barcha query parametrlarini SQL inyeksiyalardan tozalash va tekshirish.
    - *Qatlam:* Security | *SP:* 3

96. **TASK-096: Xotira va resurslar auditi (Memory Leak Test)**
    - *Tavsif:* Simulyator va desktop ilovani 1 soat davomida ishlatib, RAM miqdorini nazorat qilish.
    - *Qatlam:* Performance | *SP:* 3

97. **TASK-097: Foydalanuvchi va Operator qo'llanmasi (User Manual)**
    - *Tavsif:* Tizimdan foydalanish bo'yicha illyustratsiyali rasmiy qo'llanma.
    - *Qatlam:* Docs | *SP:* 3

98. **TASK-098: Taskcafe & GitHub Projects yakuniy sinxronizatsiyasi**
    - *Tavsif:* Barcha 100 ta vazifaning kartochkalar holati, teglar va assigneelari tekshiruvi.
    - *Qatlam:* PM / GitHub | *SP:* 2

99. **TASK-099: Demo video va interaktiv taqdimot tayyorlash**
    - *Tavsif:* Shlagbaum, 3D izometrik xarita, ANPR kamera va 4-Moliya bo'limi ishlashini namoyish etuvchi video.
    - *Qatlam:* Presentation | *SP:* 4

100. **TASK-100: Yakuniy Reliz va Versiya Tag (`v1.0.0-mvp`)**
     - *Tavsif:* Kod bazasini muzlatish (Code Freeze), reliz tagini qo'yish va GitHub Releases sahifasiga joylash.
     - *Qatlam:* Release / Management | *SP:* 2
