---
name: "User Story"
about: "Parkly.uz — Standart Agile User Story andozasi (SLA va Acceptance Criteria bilan)"
title: "[STORY]: "
labels: ["story", "needs-triage"]
assignees: []
---

## 👤 User Story
**[Rol] sifatida**, men **[xatti-harakat/funksiya]**ni xohlayman,  
**toki** **[biznes qiymati / maqsad]**ga erishilsin.

---

## ⏱️ Foydalanuvchi Kutish Vaqti Cheklovi (SLA Constraint)
- **Maksimal ruxsat etilgan kutish:** `≤ 10 daqiqa`
- [ ] 0–3 daqiqa: Avtomatik qayta ishlash
- [ ] 5 daqiqa: Sariq ogohlantirish (Operator taymeri)
- [ ] 7 daqiqa: Qizil favqulodda ogohlantirish (Super-Admin eskalatsiyasi)
- [ ] 10 daqiqa: Fail-Safe avtomatik o'tkazish (Offline talon / Favqulodda ochilish)

---

## 📋 Acceptance Criteria (Qabul Qilish Mezonlari - Given/When/Then)
- [ ] **AC-1:** Given [boshlang'ich shart], When [harakat sodir bo'lganda], Then [kutilgan natija].
- [ ] **AC-2:** Given [boshlang'ich shart], When [harakat sodir bo'lganda], Then [kutilgan natija].
- [ ] **AC-3:** Kutish vaqti hech qachon 10 daqiqadan oshmasligi kafolatlangan.

---

## 🛠️ Texnik Vazifalar (Technical Tasks Checklist)
- [ ] Task 1: API / Backend logikasi
- [ ] Task 2: Camera / Vision yoki Frontend komponenti
- [ ] Task 3: Unit va integratsion testlar

---

## 🏷️ Ma'lumotlar
* **Priority:** `P0 (Critical)` / `P1 (High)` / `P2 (Medium)` / `P3 (Low)`
* **MoSCoW:** `Must Have` / `Should Have` / `Could Have`
* **Story Points:** `1` / `2` / `3` / `5` / `8` / `13`
* **Sprint:** `Sprint 1` / `Sprint 2` / `Sprint 3` / `Sprint 4`
* **Mas'ul:** @username

> **Definition of Done (DoD):**
> 1. Barcha Acceptance Criteria'lar bajarilgan.
> 2. 10 minutlik maksimal kutish chegarasi tekshirilgan.
> 3. Avtomatlashgan testlar (pytest/unittest) 100% yashil.
> 4. Kod `main` ga PR orqali merge qilingan.
