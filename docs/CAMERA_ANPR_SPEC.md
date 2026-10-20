# 📷 Parkly.uz — Camera & Advanced ANPR Pipeline Specification

> **Modul:** Computer Vision & ANPR Subsystem  
> **Mas'ul Mutaxassis:** Omirboyev Said `[AI/CV]`  
> **Maqsad:** Tuman, qorong'i tun, xira yorug'lik va qiyshiq rakurslarda ham O'zbekiston davlat raqamlarini **≥ 95% aniqlikda** o'qish va kadrlar kechikishining (lag) oldini olish.

---

## 🏛️ 1. ANPR 6 Bosqichli Intellektual Quvur Liniyasi (Pipeline Architecture)

```
[ RTSP / USB Camera Stream ]
           │
           ▼
1. Universal Stream & Buffer (camera_stream.py) ──► Auto-Reconnect & Zero-Latency Queue
           │
           ▼
2. Low-Light & Glare Enhancement (frame_enhancer.py) ──► CLAHE + Bilateral Filtering
           │
           ▼
3. Two-Stage Plate Detector (detector.py) ──► Vehicle BBox ──► Plate ROI Crop
           │
           ▼
4. Perspective Homography (perspective.py) ──► Trapezoid to Frontal Rectification
           │
           ▼
5. Uzbekistan OCR & Ambiguity Filter (ocr_engine.py) ──► O/0, I/1 Normalization
           │
           ▼
6. Multi-Frame Temporal Consensus (temporal_tracker.py) ──► Final Plate (≥95% Accuracy)
```

---

## 📋 2. Texnik Vazifalar va Acceptance Criteria (User Stories)

### 📌 TASK-201: Multi-threading va Auto-reconnect Kamera Drayveri (`camera_stream.py`)
* **Mas'ul:** Omirboyev Said `[AI/CV]`
* **User Story:**
  > Sifatida AI & CV muhandisi, tarmoq uzilishlari va FPS tebranishlarida ham ishdan to'xtamaydigan, multi-threading asosida ishlovchi kamera drayverini yaratishni istayman.
* **Acceptance Criteria:**
  - [x] RTSP IP-kameralar, USB veb-kameralar va test video fayllarini `.env` orqali ulash imkoniyati.
  - [x] Tarmoq uzilganda (Network drop) avtomatik qayta ulanish (`Auto-reconnect`) mexanizmi.
  - [x] Kadrlar buferi to'lib qolishining (`Buffer overflow / Lag`) oldini oluvchi zero-latency queue boshqaruvi.

### 📌 TASK-203: Adaptiv Vizual Filtrlar (`frame_enhancer.py`)
* **Mas'ul:** Omirboyev Said `[AI/CV]`
* **User Story:**
  > Sifatida AI & CV muhandisi, qorong'i tun, tuman va yorqin faralar porlashida (glare) raqamlarni ochib beruvchi CLAHE va Bilateral filtrlarini kuchaytirishni istayman.
* **Acceptance Criteria:**
  - [x] Contrast Limited Adaptive Histogram Equalization (CLAHE) orqali tungi kadrlar yoritiladi.
  - [x] Bilateral filtering orqali shovqinlar tozalanadi, lekin raqam qirralari xiralashmaydi.

### 📌 TASK-204: Two-Stage Plate Detector (`detector.py`)
* **Mas'ul:** Omirboyev Said `[AI/CV]`
* **User Story:**
  > Sifatida AI & CV muhandisi, kadr ichidan avval transport vositasini, so'ngra uning raqam zonasini aniq qirqib oluvchi ikki bosqichli detektorni ulashni istayman.
* **Acceptance Criteria:**
  - [x] 1-bosqich: Mashina bounding box'ini aniqlash.
  - [x] 2-bosqich: Mashina bamperidan 4.5:1 proporsiyadagi raqam hududini aniq kesib olish.

### 📌 TASK-205: Perspektiv Homography Korreksiyasi (`perspective.py`)
* **Mas'ul:** Omirboyev Said `[AI/CV]`
* **User Story:**
  > Sifatida AI & CV muhandisi, 30°–45° burchak ostida olingan qiyshiq trapetsiya shaklidagi raqamlarni to'g'ri to'rtburchakka o'tkazishni istayman.
* **Acceptance Criteria:**
  - [x] To'rt nuqtali perspektiv transformatsiya (`Perspective Homography`) amalga oshirildi.
  - [x] Qiyshiq burchaklar OCR uchun qulay frontal ko'rinishga keltirildi.

### 📌 TASK-206: Uzbekistan Plate OCR & Ambiguity Correction (`ocr_engine.py`)
* **Mas'ul:** Omirboyev Said `[AI/CV]`
* **User Story:**
  > Sifatida AI & CV muhandisi, O'zbekiston davlat raqami shabloniga mos keluvchi va harf-raqam chalkashliklarini (`O` <-> `0`, `I` <-> `1`) pozitsion qoidalar asosida to'g'rilovchi OCR filtrini yaratishni istayman.
* **Acceptance Criteria:**
  - [x] 1-2 o'rin faqat raqam (`01`-`95`), o'rtadagi harflar lotin alifbosi ekanligi tekshiriladi.
  - [x] OCR xato o'qigan o'xshash belgilar pozitsiyasiga qarab avtomatik to'g'rilanadi.

### 📌 TASK-207: Multi-Frame Temporal Consensus (`temporal_tracker.py`)
* **Mas'ul:** Omirboyev Said `[AI/CV]`
* **User Story:**
  > Sifatida AI & CV muhandisi, ketma-ket kelgan bir nechta kadrlar bo'yicha ovoz berish (Temporal Consensus) orqali ANPR aniqligini 95%+ ga yetkazishni istayman.
* **Acceptance Criteria:**
  - [x] 2 soniya ichida kelgan o'xshash raqamlar klasterlanadi.
  - [x] Eng ko'p ovoz to'plagan valid raqam final natija sifatida qabul qilinadi.
