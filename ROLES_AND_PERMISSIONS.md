# 🛡️ Parkly.uz — Rollar, Ruxsatlar va Huquqlar Matritsasi (RBAC & GitHub)

Loyiha muvaffaqiyatli, xavfsiz va tizimli rivojlanishi uchun GitHub repozitoriyasida hamda Desktop Admin boshqaruv panelida har bir ishtirokchiga uning mas'uliyatiga mos huquqlar belgilangan.

---

## 🏛️ 1. Dasturiy Tizim RBAC Huquqlar Matritsasi (Desktop Admin Panel)

Tizimda xavfsizlik va mas'uliyatni ajratish maqsadida 3 xil foydalanuvchi toifalari joriy etilgan:

| Rol | Miqdori | Foydalanuvchilar (Login) | Mas'uliyat Sohasi va Ruxsatlar |
| :--- | :---: | :--- | :--- |
| **Super-Admin** | **2 kishi** | • `admin` *(Erjigit - Bosh Rahbar)*<br>• `superadmin2` *(Sherzod Aliyev - Tizim Arxitektori)* | • **Barcha 7 ta bo'limga to'liq kirish va tahrirlash**<br>• Tizim sozlamalari va tariflarni o'zgartirish<br>• Oddiy adminlar akkauntini yaratish va o'chirish<br>• Favqulodda (Emergency Fail-Safe) shlagbaumni majburiy ochish<br>• 10 daqiqalik SLA buzilishi holatlarini audit qilish |
| **Oddiy Admin** | **4 kishi** | • `admin_yunusobod` *(Jahongir Qodirov)*<br>• `admin_chilonzor` *(Aziz Rustamov)*<br>• `admin_mirobod` *(Bobur Mirzayev)*<br>• `admin_sergeli` *(Dilshod Karimov)* | • Real-vaqt monitoringi va 3D Izometrik xaritaning joriy holati<br>• 4-Moliya bo'limini ko'rish va hisobotlarni Excel/CSV formatida yuklab olish<br>• Kameralar statusi va faol sessiyalarni kuzatish<br>• ❌ **Tizim sozlamalari (7) va Xodimlar (6) bo'limlariga kirish taqiqlangan (Qulflangan 🔒)**<br>• ❌ **Tarif stavkalarini o'zgartirish qat'iyan taqiqlangan** |
| **Smena Operatori** | **2 kishi** | • `operator1` *(Farrux Yusupov)*<br>• `operator2` *(G'ayrat Xoliqov)* | • Kirish va chiqishdagi ANPR kameralar oqimini kuzatish<br>• Noaniq raqamlarni (`Confidence < 85%`) 15 soniya ichida qo'lda tasdiqlash/tuzatish<br>• 10 daqiqalik kutish taymerini nazorat qilish va tirbandlikni oldini olish |

---

## ⏱️ 2. Shlagbaum va 10 Daqiqalik Maksimal Kutish (Emergency SLA Rule)

Foydalanuvchilar kirish yoki chiqish shlagbaumida **hech qachon 10 daqiqadan ko'p kutmasligi** shart:
1. **0 – 5 daqiqa (Normal):** Avtomatik ANPR va to'lov tekshiruvi.
2. **5 – 7 daqiqa (Warning):** Operator monitorida sariq xabarnoma chiqadi va zudlik bilan qo'lda tasdiqlash talab etiladi.
3. **7 – 10 daqiqa (Urgent):** Super-Admin panelida qizil favqulodda ogohlantirish signali chalinadi.
4. **10 daqiqa (Fail-Safe):** Tizim avtomobilni postda ushlab turmaydi — shlagbaum avtomatik bir martalik offline-talon bilan ochilib, haydovchiga chiqishga ruxsat beriladi va voqea auditga yoziladi.

---

## 💻 3. GitHub Repozitoriyasida Rollar va Ruxsatlar

GitHub repozitoriyasida jamoa a'zolari quyidagi ruxsat darajalariga ega:

| Lavozim | GitHub Roli | Qila oladigan amallari | Mas'uliyat |
| :--- | :--- | :--- | :--- |
| **Owner / Boshqaruvchi** | **Owner / Admin** | Repozitoriy sozlamalari, billing, branch protection, to'liq boshqaruv. | Barcha jarayonlarga yakuniy javobgar. |
| **Project Manager (PM)** | **Triage / Maintain** | Issue'lar, Taskcafe / GitHub Kanban doskasi, Milestone va Label boshqaruvi. | Vazifalar holati va sprint muddatlarini nazorat qilish. |
| **Dasturchilar (Developers)** | **Write** | Feature branch'lar ochish, kod yozish, Pull Request ochish. `main` ga to'g'ridan-to'g'ri push qilolmaydi. | Toza va xatosiz kod yetkazib berish. |
| **Lead / Senior Dev** | **Maintain** | Pull Request'larni tekshirish (Code Review), CI/CD avtotestlarini nazorat qilish, merge qilish. | Arxitektura sifati va barqarorlik. |
| **QA Tester** | **Triage** | Test-case'lar asosida bug ochish, test hisobotlarini yuritish. | Sifat kafolati. |

---

## 🔒 4. Branch Protection Qoidalari (`main` va `Mirhamid`):
1. To'g'ridan-to'g'ri `git push` qilish cheklangan.
2. Barcha o'zgarishlar Pull Request (PR) orqali yuboriladi.
3. PR merge bo'lishi uchun kamida 1 ta tasdiq (Approval) va CI testlari (`pytest`, `unittest` - 20/20 yashil) muvaffaqiyatli o'tishi shart.
