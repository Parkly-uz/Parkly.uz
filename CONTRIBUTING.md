# 🤝 Parkly.uz da ishlash qoidalari (Contributing Guidelines)

Jamoaning barcha dasturchilari va texnik a'zolari quyidagi tartib-qoidalarga rioya qilishi shart.

---

## 1. Tarmoqlar (Branching) Qoidasi
1. Har doim yangi vazifani `develop` tarmog'idan olib boshlang:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/vazifa-nomi
   ```
2. Hech qachon `main` yoki `develop` ga to'g'ridan-to'g'ri `git push` qilmang.

---

## 2. Commit xabarlari formati (Conventional Commits)
Har bir commit aniq va tushunarli bo'lishi kerak:
- `feat: yangi funksiya qo'shilganda (masalan: feat: add payme webhook handler)`
- `fix: xatolik to'g'rilanganda (masalan: fix: resolve barrier response timeout)`
- `docs: hujjatlarga o'zgartirish kiritilganda`
- `refactor: kod yaxshilanganda`
- `test: testlar yozilganda`

---

## 3. Pull Request (PR) topshirish
1. Vazifa bitgach, o'z branchingizni GitHub'ga yuklang:
   ```bash
   git push origin feature/vazifa-nomi
   ```
2. GitHub'da `develop` tarmog'iga Pull Request oching.
3. PR sarlavhasi va tavsifida nima o'zgarganini va qaysi Issue (masalan: `Closes #12`) yopilishini ko'rsating.
4. Kamida 1 ta Lead / Senior dasturchi kodni tasdiqlashi (Approve) shart.
