# 🛡️ GitHub Repositoriyasida Rollar va Ruxsatlar Qo'llanmasi (Parkly.uz)

Loyiha muvaffaqiyatli, xavfsiz va tizimli rivojlanishi uchun GitHub'da har bir jamoa a'zosiga uning mas'uliyatiga mos rol berish zarur.

---

## 1. Qaysi yo'l ma'qul: Shaxsiy profilmi yoki GitHub Organization?

> 💡 **Senior Developer Tavsiyasi:** Loyiha uchun alohida **GitHub Organization** ochish eng to'g'ri yo'l (masalan: `github.com/parkly-uz` yoki `ParklyUz`).
> 
> **Nima uchun?**
> - Tashkilotda (Org) rollar guruhlarga (Teams: `@parkly/developers`, `@parkly/managers`, `@parkly/devops`) bo'linadi.
> - Kengaytirilgan ruxsatlar (Role permissions) va loyihalar portfeli bitta joyda turadi.
> - Agar shaxsiy profilingizda (`github.com/sizning_username/Parkly.uz`) ochsangiz ham, quyidagi qoidalar aynan ishlaydi!

---

## 2. GitHub Rollari Matritsasi

GitHub'da 5 xil asosiy darajadagi ruxsat mavjud:

| Lavozim | GitHub Roli | Qila oladigan amallari | Nima uchun bu rol? |
| :--- | :--- | :--- | :--- |
| **Siz (Owner / Asoschisi)** | **Owner / Admin** | Barcha huquqlar: repozitoriy sozlamalari, billing, integratsiyalar, to'liq boshqaruv. | Loyihaning to'liq egasi sizsiz. |
| **Project Manager (PM)** | **Triage** yoki **Maintain** | Issue'lar, Project Kanban boardlar, Milestone va Label'larni boshqarish, vazifalar yuklash, PR'larni yopish/ochish. | Kod bazasini xavf ostiga qo'ymasdan jamoa jarayonini 100% boshqarishi uchun. |
| **Dasturchilar (Developers)** | **Write** | O'z tarmog'iga (feature branch) kod push qilish, Pull Request ochish. `main` ga to'g'ridan-to'g'ri push qilolmaydi. | Kod xavfsizligi va toza arxitektura ta'minlanadi. |
| **Lead / Senior Developer** | **Maintain** | Dasturchilarning Pull Request'larini tekshirish (Code Review), CI/CD holatini nazorat qilish, merge qilish. | Sifatli arxitektura va kod bazasini saqlash uchun. |
| **QA / Tester** | **Triage** | Issue (bug) ochish, reproduktsiya qilish, labellar qo'yish. | Faqat sinov va muammolar hisobotini yuritadi. |

---

## 3. GitHub'da A'zolarni Qo'shish Qadamlari (Step-by-Step)

### A. Agar oddiy (shaxsiy) repozitoriy bo'lsa:
1. Repozitoriyangizga kiring: `https://github.com/<sizning_username>/Parkly.uz`
2. Yuqoridagi menyudan **⚙️ Settings** bo'limiga o'ting.
3. Chap tomondagi menyudan **Collaborators** (yoki *Collaborators and teams*) bo'limini tanlang.
4. **"Add people"** yashil tugmasini bosing.
5. Jamoa a'zosining **GitHub username** yoki **email** manzilini kiriting.
6. Unga beriladigan rolni tanlang:
   - **Dasturchi uchun:** `Write`
   - **Project Manager uchun:** `Triage` (agar faqat task boshqarsa) yoki `Maintain`
7. **"Add ... to this repository"** tugmasini bosing.
8. Uning pochtasiga taklifnoma (invitation) boradi, u qabul qilgach tizimga qo'shiladi.

### B. Agar GitHub Organization ochsangiz:
1. `Settings` -> `Manage access` -> `Add teams` yoki `Add members`.
2. Jamoalarni yarating:
   - `core-devs` (Role: Write)
   - `project-managers` (Role: Triage / Maintain)
   - `leads` (Role: Admin / Maintain)
3. Yangi a'zoni shunchaki tegishli guruhga qo'shib qo'ysangiz kifoya.

---

## 4. Muhim Qoida: "Branch Protection Rule" Sozlash

Hech bir dasturchi yoki xodim tasodifan asosiy `main` tarmoqqa xato kod yuborib qo'ymasligi uchun himoya o'rnatish shart:

1. Repozitoriyaning **Settings** bo'limiga kiring.
2. Chap tarafdan **Branches** bo'limini tanlang.
3. **"Add branch protection rule"** tugmasini bosing.
4. **Branch name pattern** maydoniga `main` deb yozing.
5. Quyidagi muhim qutilarga belgi (✅) qo'ying:
   - ✅ **Require a pull request before merging** (To'g'ridan-to'g'ri push taqiqlanadi, faqat PR orqali qo'shiladi).
   - ✅ **Require approvals**: Kamida `1` ta (Senior dev tasdiqlashi shart).
   - ✅ **Dismiss stale pull request approvals when new commits are pushed**.
   - ✅ **Require status checks to pass before merging** (Testlar va CI muvaffaqiyatli o'tishi kerak).
6. **Save changes** tugmasini bosing.

Bu bilan siz loyihani professional standartlarga to'liq mos holatga keltirasiz!
