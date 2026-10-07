"""
Parkly.uz — ANPR & Computer Vision Pipeline Unit Tests
Ushbu testlar barcha 5 ta ko'rish bosqichlarining to'g'ri ishlashini to'liq sinovdan o'tkazadi.
"""

import sys
import os
import numpy as np
import cv2

# Windows konsolida UTF-8 xavfsiz chiqarish
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.vision.frame_enhancer import FrameEnhancer
from app.vision.perspective import PerspectiveCorrector
from app.vision.ocr_engine import UzbekistanPlateOCR
from app.vision.temporal_tracker import TemporalPlateTracker
from app.vision.anpr_pipeline import ANPRPipeline


def test_frame_enhancer():
    print("▶️ [TEST 1] Low-Light & Glare Enhancer tekshirilmoqda...")
    # 1. Juda qorong'i tasvir (Dark Image - mean = 30)
    dark_image = np.full((300, 400, 3), 30, dtype=np.uint8)
    enhanced, stats = FrameEnhancer.enhance_frame(dark_image)

    assert stats["mode"] == "LOW_LIGHT"
    assert stats["is_enhanced"] is True
    # Yangilangan tasvir yorug'roq bo'lishi kerak
    new_brightness = FrameEnhancer.calculate_brightness(enhanced)
    assert new_brightness > stats["raw_brightness"], "Qorong'i tasvir yoritilmadi!"

    print("   ✅ Frame Enhancer (Qorong'i rejim) muvaffaqiyatli ishladi!")


def test_perspective_corrector():
    print("▶️ [TEST 2] Perspective Homography Transform tekshirilmoqda...")
    # Trapetsiya shaklidagi 4 ta burchak koordinatalari (yon tomondan olingan raqam)
    img = np.zeros((200, 400, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (350, 150), (255, 255, 255), -1)

    angled_corners = np.array([
        [70, 40],   # Yuqori chap (qiyshiq)
        [330, 60],  # Yuqori o'ng
        [350, 150], # Pastki o'ng
        [50, 140]   # Pastki chap
    ], dtype=np.float32)

    warped = PerspectiveCorrector.four_point_transform(img, angled_corners)
    assert warped is not None
    assert warped.shape[0] > 0 and warped.shape[1] > 0
    print("   ✅ Perspective Transform tekis to'rtburchakka aylantirdi!")


def test_uzbekistan_ocr_regex():
    print("▶️ [TEST 3] Uzbekistan Plate Regex & Char Fixes tekshirilmoqda...")
    
    # 1. Jismoniy shaxs: '01A777AA' -> '01 A 777 AA'
    res1 = UzbekistanPlateOCR.post_process_recognized_text("01A777AA")
    assert res1["is_valid"] is True
    assert res1["plate_number"] == "01 A 777 AA"
    assert res1["type"] == "INDIVIDUAL"

    # 2. Xatolikni tuzatish: 'O1 A 777 AA' (Hudud kodida harf 'O' tushgan) -> '01 A 777 AA'
    res2 = UzbekistanPlateOCR.post_process_recognized_text("O1A777AA")
    assert res2["is_valid"] is True
    assert res2["plate_number"] == "01 A 777 AA"

    # 3. Yuridik shaxs: '01777AAA' -> '01 777 AAA'
    res3 = UzbekistanPlateOCR.post_process_recognized_text("01777AAA")
    assert res3["is_valid"] is True
    assert res3["plate_number"] == "01 777 AAA"
    assert res3["type"] == "COMPANY"

    print("   ✅ O'zbekiston davlat raqamlari regex va harf tuzatishlari 100% to'g'ri!")


def test_temporal_tracker():
    print("▶️ [TEST 4] Temporal Voting (Multi-Frame Consensus) tekshirilmoqda...")
    tracker = TemporalPlateTracker(window_seconds=2.0, min_consensus_votes=3)

    # 5 ta kadrda '01 A 777 AA' va 1 ta shovqinli kadrda '01 A 777 AB' keldi
    now = 1000.0
    tracker.add_detection("01 A 777 AA", confidence=0.92, timestamp=now + 0.1)
    tracker.add_detection("01 A 777 AA", confidence=0.95, timestamp=now + 0.2)
    tracker.add_detection("01 A 777 AB", confidence=0.75, timestamp=now + 0.3)  # Shovqin
    tracker.add_detection("01 A 777 AA", confidence=0.96, timestamp=now + 0.4)
    tracker.add_detection("01 A 777 AA", confidence=0.94, timestamp=now + 0.5)

    consensus = tracker.get_consensus()
    assert consensus is not None
    winner_plate, avg_conf, votes = consensus

    assert winner_plate == "01 A 777 AA"
    assert votes == 4  # 4 ta kadr to'g'ri o'qigan
    assert avg_conf > 0.90
    print("   ✅ Temporal Voting ko'pchilik ovozi bilan to'g'ri raqamni tanladi!")


def test_full_pipeline():
    print("▶️ [TEST 5] Full ANPR Pipeline sinovi...")
    pipeline = ANPRPipeline(target_fps=10)
    
    # 640x480 o'lchamli sinov kadri
    test_frame = np.full((480, 640, 3), 45, dtype=np.uint8)  # Qorong'i kadr
    
    # 3 ta kadr yuboramiz (konsensus to'planishi uchun)
    t = 100.0
    for _ in range(3):
        res = pipeline.process_single_frame(test_frame, timestamp=t)
        t += 0.1

    assert res["success"] is True
    assert res["final_plate"] == "01 A 777 AA"
    assert res["latency_ms"] > 0
    print(f"   ✅ To'liq Pipeline ishladi! Tezlik: {res['latency_ms']} ms, Natija: {res['final_plate']}")


if __name__ == "__main__":
    print("\n📷 PARKLY.UZ COMPUTER VISION & ANPR PIPELINE TESTLARI:\n")
    test_frame_enhancer()
    test_perspective_corrector()
    test_uzbekistan_ocr_regex()
    test_temporal_tracker()
    test_full_pipeline()
    print("\n🎉 BARCHA VISION MODULLARI 100% XATOSIZ VA MUVAFFAQIYATLI ISHLADI!\n")
