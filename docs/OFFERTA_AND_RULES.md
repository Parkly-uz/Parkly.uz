# 📜 Parkly.uz — Ommaviy Oferta Shartnomasi, Xavfsizlik Qoidalari va Tailgating Protokoli

> **Hujjat Turi:** Huquqiy Oferta, Xavfsizlik Qoidalari va Texnik Xavfsizlik Protokollari  
> **Loyihaning Joylashuvi:** Parkly.uz Aqlli Avtoturargoh Ekotizimi  
> **Til:** O'zbek tili  

---

## 🚨 1. Tailgating (Ergashtirib / Dumalab Kirish) Shlagbaum Himoya Protokoli

Tailgating — bu ruxsat etilgan (to'lov qilgan yoki obunasi bor) avtomobil ortidan boshqa bir avtomobilning shlagbaum yopilishiga ulgurmasdan yopishib kirib olish holatidir. Parkly.uz tizimi ushbu qoidabuzarlikning oldini olish uchun quyidagi avtomatlashgan texnik protokolni qo'llaydi:

### A. Texnik Aniqlash Mexanizmlari (Detection)
1. **Fotorele va Induktiv Ilmoqlar (Loop Detectors):** Shlagbaum ostida va chiqish/kirish zonasida o'rnatilgan datchiklar avtomobilning g'ildirak o'qini aniqlaydi. Agar birinchi mashina o'tmagaturib ikkinchi ob'ekt harakatlansa, tizim signal beradi.
2. **ANPR Kamera Taqibi:** Kirish va chiqish kameralari kadr tezligida (10+ FPS) mashinalar orasidagi masofani masofaviy o'lchaydi. Mashinalar orasidagi masofa 1.5 metrdan qisqa bo'lsa, "Tailgating" xavfi qayd etiladi.

### B. Shlagbaumning Favqulodda Reaksiyasi (Action)
1. **Darhol To'xtatish (Instant Stop):** Agar ikkinchi mashina ruxsatsiz ergashib kelayotgan bo'lsa, shlagbaum mexanizmi avtomatik ravishda to'xtatiladi yoki darhol pastga tushib, yo'lni to'sadi (to'qnashuvni oldini olish uchun xavfsizlik datchiklari ishlaydi).
2. **Qoidabuzarni Fotografik Qayd Etish:** Ruxsatsiz kirishga urinayotgan transport vositasining davlat raqami ANPR kamera tomonidan yuqori aniqlikda suratga olinib, bazaga **"TAILGATING_VIOLATION"** sifatida saqlanadi.
3. **Operatorga Signal va Blokirovka:** Admin panelning real-time bildirishnomalar paneliga darhol qizil rangli ogohlantirish yuboriladi va tizim ushbu mashinaga xizmat ko'rsatishni vaqtincha bloklaydi.

---

## 🛡️ 2. Avtoturargoh Xavfsizlik va Saqlash Qoidalari (Parking Save-Rules)

1. **Kirish va Mas'uliyat:** Avtoturargohga kirgan har bir haydovchi ushbu qoidalarga so'zsiz amal qilishni o'z zimmasiga oladi. Avtoturargoh ma'muriyati avtomobilda qoldirilgan shaxsiy buyumlar, pul va qimmatbaho narsalar uchun moddiy javobgar emas.
2. **Tezlik Cheklovi:** Avtoturargoh hududida transport vositalarining maksimal harakatlanish tezligi **10 km/soat** etib belgilanadi.
3. **Yong'in xavfsizligi va taqiqlangan moddalar:**
   - Avtoturargoh hududida ochiq olovdan foydalanish, yonilg'i quyish yoki texnik nosoz transport vositalarini qoldirish qat'iyan taqiqlanadi.
   - Portlovchi, zaharli, tez yonuvchi moddalar va qurol-yarog'larni avtomobilda saqlash taqiqlanadi.
4. **Elektromobillar (EV):** Faqat belgilangan EV zaryadlash stansiyalari joylashgan slotlardagina elektromobillarni zaryadga ulash mumkin. Zaryad tugagach, joyni boshqa mashinalarga bo'shatib qo'yish shart.

---

## 📄 3. Ommaviy Oferta Shartnomasi (Public Offer Agreement)

**1-Bobi. Umumiy qoidalar**
1.1. Ushbu hujjat "Parkly.uz" avtoturargoh tizimi (keyingi o'rinlarda — "Ijrochi") tomonidan taqdim etiladigan avtoturargoh va saqlash xizmatlaridan foydalanish bo'yicha ommaviy oferta (shartnoma) hisoblanadi.
1.2. O'zbekiston Respublikasi Fuqarolik Kodeksining 367 va 369-moddalariga muvofiq, shartnoma shartlarini qabul qilgan (aksept qilgan) jismoniy yoki yuridik shaxs (keyingi o'rinlarda — "Mijoz") ushbu shartnomaning to'laqonli ishtirokchisiga aylanadi.

**2-Bobi. Shartnomaning Predmeti**
2.1. Ijrochi Mijozning transport vositasiga Parkly.uz avtoturargoh hududida vaqtinchalik to'xtab turish, saqlash va xavfsizlik xizmatlarini ko'rsatadi, Mijoz esa ko'rsatilgan xizmatlar uchun tasdiqlangan tariflar asosida haq to'laydi.
2.2. Avtoturargoh yirik obyektlar uchun mo'ljallangan bo'lib, yagona markazlashgan hududda faoliyat yuritadi.

**3-Bobi. Hisob-kitob va To'lov Shartlari (Payment Offer)**
3.1. Xizmatlar haqi faqat **naqd pulsiz (Cashless)** usulda — Click, Payme, Uzum Pay yoki bank kartalari orqali amalga oshiriladi.
3.2. Dastlabki **15 daqiqa (Grace Period)** bepul hisoblanadi. Ushbu muddatdan oshgan har bir soat uchun tasdiqlangan soatlik stavka bo'yicha haq olinadi.
3.3. Oylik obunalar (`1 oylik`, `3 oylik`, `6 oylik` paketlar) oldindan 100% to'lov asosida faollashtiriladi. Obuna muddati tugagach, avtomatik ravishda to'xtatiladi yoki Mijozning roziligi bilan uzaytiriladi.
3.4. Xodimlar va xizmat ko'rsatuvchi personel uchun avtoturargoh xizmatlari bepul (to'lov olinmaydi).

**4-Bobi. Tomonlarning Javobgarligi va Yakuniy Qoidalar**
4.1. Mijoz avtoturargoh qoidalarini buzgan, tailgating sodir etgan yoki to'lovdan bo'yin tovlagan taqdirda, Ijrochi xizmat ko'rsatishni to'xtatish va avtomobilni hududdan chiqarib yuborish huquqiga ega.
4.2. Ushbu oferta O'zbekiston Respublikasining amaldagi qonunchiligiga muvofiq tartibga solinadi.
