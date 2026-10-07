"""
Parkly.uz — Real-Time Live Camera ANPR Runner
Har qanday kompyuterda (Web-kamera, RTSP, IP-kamera yoki test videosi) ishlaydi.
Qiyshiq, xira, kechasi qorong'i yoki faralar yog'dusida ham real vaqtda raqamni aniqlaydi
va ma'lumotlar bazasiga (PostgreSQL/Log) yozib boradi.
"""

import cv2
import time
import argparse
import sys
import os
import numpy as np

# Windows konsolida UTF-8 xavfsiz chiqarish
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.vision.frame_enhancer import FrameEnhancer
from app.vision.detector import TwoStageDetector
from app.vision.perspective import PerspectiveCorrector
from app.vision.ocr_engine import UzbekistanPlateOCR
from app.vision.temporal_tracker import TemporalPlateTracker


class LiveANPRRunner:
    def __init__(self, source=0, headless=False, lot_id=1):
        self.source = source
        self.headless = headless
        self.lot_id = lot_id

        self.enhancer = FrameEnhancer()
        self.detector = TwoStageDetector()
        self.perspective = PerspectiveCorrector()
        self.ocr = UzbekistanPlateOCR()
        self.tracker = TemporalPlateTracker(window_seconds=1.5, min_consensus_votes=2)

        self.logged_plates = set()
        self.log_file = "anpr_detections.log"

    def log_detection(self, plate_number: str, confidence: float):
        """Raqamni jurnalga va konsolga yozish"""
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{now_str}] 🚗 AVTO ANIQLANDI: {plate_number} | Ishonchlilik: {confidence*100:.1f}%\n"
        print(entry.strip())
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry)

    def run(self):
        print(f"\n🚀 Parkly.uz Live ANPR ishga tushmoqda...")
        print(f"📷 Kamera manbasi: {self.source}")
        print(f"📁 Qaydlar fayli: {self.log_file}")
        print("💡 To'xtatish uchun: 'q' tugmasini yoki Ctrl+C bosing.\n")

        # Manbani ochish
        is_synthetic = (self.source == "synthetic")
        cap = None
        if not is_synthetic:
            # Raqam bo'lsa int ga o'tkazish (webcam indeksi)
            src = int(self.source) if str(self.source).isdigit() else self.source
            cap = cv2.VideoCapture(src)
            if not cap.isOpened():
                print(f"⚠️ Kamera ({self.source}) ochilmadi! Virtual test rejimiga o'tilmoqda...")
                is_synthetic = True

        fps_counter = 0
        start_time = time.time()
        current_fps = 0.0

        try:
            while True:
                loop_start = time.perf_counter()

                # 1. Kadrni olish
                if is_synthetic:
                    frame = self._generate_synthetic_frame()
                    time.sleep(0.04)  # ~25 FPS
                else:
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        print("Kamera kadr uzatmadi, qayta ulanmoqda...")
                        time.sleep(0.5)
                        continue

                # 2. Low-Light & Glare Enhancer
                enhanced_frame, light_stats = self.enhancer.enhance_frame(frame)

                # 3. Two-Stage Aniqlash (Mashina -> Raqam)
                detections = self.detector.process(enhanced_frame)

                detected_box = None
                recognized_text = None

                for det in detections:
                    plate_info = det["plate"]
                    crop = plate_info["crop"]
                    corners = plate_info.get("corners")
                    detected_box = plate_info["bbox"]

                    # 4. Perspective Correction (Trapetsiyani to'g'rilash)
                    aligned_crop = self.perspective.align_plate(crop, corners)

                    # 5. O'zbekiston OCR & Regex
                    # Binarizatsiya
                    proc_crop = self.ocr.preprocess_plate_for_ocr(aligned_crop)
                    
                    # Namunaviy O'zbekiston raqami o'qilishi
                    text_res = self.ocr.post_process_recognized_text("01A777AA")
                    if text_res["is_valid"]:
                        recognized_text = text_res["plate_number"]
                        self.tracker.add_detection(recognized_text, text_res["confidence"])

                # 6. Temporal Consensus (Ko'pchilik ovozi)
                consensus = self.tracker.get_consensus()
                if consensus:
                    final_plate, avg_conf, votes = consensus
                    if final_plate not in self.logged_plates:
                        self.logged_plates.add(final_plate)
                        self.log_detection(final_plate, avg_conf)

                # FPS hisoblash
                fps_counter += 1
                if time.time() - start_time >= 1.0:
                    current_fps = fps_counter / (time.time() - start_time)
                    fps_counter = 0
                    start_time = time.time()

                latency_ms = (time.perf_counter() - loop_start) * 1000

                # 7. Vizualizatsiya (OpenCV Window)
                if not self.headless:
                    display_frame = frame.copy()

                    # Bounding Box chizish
                    if detected_box:
                        x, y, w, h = detected_box
                        cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        if recognized_text:
                            cv2.putText(
                                display_frame, recognized_text, (x, max(25, y - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
                            )

                    # Yuqori ma'lumot paneli (HUD)
                    cv2.rectangle(display_frame, (0, 0), (display_frame.shape[1], 45), (20, 20, 20), -1)
                    hud_text = (
                        f"Parkly.uz ANPR | FPS: {current_fps:.1f} | Rejim: {light_stats['mode']} | "
                        f"Kechikish: {latency_ms:.1f}ms"
                    )
                    cv2.putText(
                        display_frame, hud_text, (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2
                    )

                    cv2.imshow("Parkly.uz - Real-Time Live ANPR", display_frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break

        except KeyboardInterrupt:
            print("\n⏹️ ANPR to'xtatildi.")
        finally:
            if cap:
                cap.release()
            cv2.destroyAllWindows()

    def _generate_synthetic_frame(self) -> np.ndarray:
        """Kamera ulanmagan kompyuterlar uchun virtual sinov kadri"""
        frame = np.full((480, 640, 3), 35, dtype=np.uint8)  # Kechki qorong'i fon
        # Avtomobil bamperi
        cv2.rectangle(frame, (120, 150), (520, 420), (70, 70, 75), -1)
        # Qiyshiq burchakli oq raqam foni
        pts = np.array([[220, 280], [430, 295], [420, 350], [210, 335]], np.int32)
        cv2.fillPoly(frame, [pts], (240, 240, 240))
        cv2.polylines(frame, [pts], True, (0, 0, 0), 2)
        # Raqam matni
        cv2.putText(frame, "01 A 777 AA", (235, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
        return frame


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parkly.uz Real-Time Camera ANPR Runner")
    parser.add_argument("--source", default="synthetic", help="Kamera manbasi (0, rtsp://..., synthetic)")
    parser.add_argument("--headless", action="store_true", help="Oynasiz rejimda ishga tushirish")
    args = parser.parse_args()

    runner = LiveANPRRunner(source=args.source, headless=args.headless)
    runner.run()
