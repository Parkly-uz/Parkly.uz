"""
Parkly.uz — Universal Camera Stream Ingestion & Frame Sampler
Har qanday kamera manbasi (RTSP, IP-kamera, USB Web-kamera, Video fayl) bilan real-time ishlaydi.
"""

import cv2
import time
import threading
from typing import Optional, Union, Generator, Tuple
import numpy as np


class CameraStream:
    """
    Kamera oqimini bufer to'lib ketishisiz (Zero-Latency) qabul qiluvchi asinxron oqim.
    
    Xususiyatlari:
    - Alohida fondagi oqim (Thread) orqali kadrlar o'qiladi (lag/kechikish bo'lmaydi).
    - Frame Sampler: 30 FPS oqimdan belgilangan miqdordagi (masalan 5-10 FPS) kadrlarni ajratib beradi.
    """

    def __init__(
        self,
        source: Union[str, int],
        target_fps: int = 10,
        name: str = "Entrance-Cam"
    ):
        """
        :param source: 'rtsp://...', 'http://...', 0 (USB webcam) yoki 'video.mp4'
        :param target_fps: AI ga yuboriladigan kadrlar soni (standart: 10 FPS)
        :param name: Kamera nomi / identifikatori
        """
        self.source = source
        self.target_fps = target_fps
        self.name = name
        self.sample_interval = 1.0 / max(1, target_fps)

        self.cap: Optional[cv2.VideoCapture] = None
        self.latest_frame: Optional[np.ndarray] = None
        self.frame_lock = threading.Lock()
        self.is_running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.last_sampled_time = 0.0

    def start(self) -> bool:
        """Kamera oqimini ishga tushirish"""
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            # Agar haqiqiy kamera topilmasa, xatolik qaytaramiz
            return False

        # RTSP va Web-kamera buferini 1 ga tushirish (kechikishni oldini olish)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.is_running = True
        self.worker_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.worker_thread.start()
        return True

    def _capture_loop(self):
        """Fondagi doimiy kadr o'qish sikli (faqat eng so'nggi kadrni saqlaydi)"""
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret or frame is None:
                time.sleep(0.01)
                continue

            with self.frame_lock:
                self.latest_frame = frame

    def get_latest_frame(self) -> Optional[np.ndarray]:
        """Eng oxirgi kadrni olish"""
        with self.frame_lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
        return None

    def sample_generator(self) -> Generator[Tuple[np.ndarray, float], None, None]:
        """
        Frame Sampler: Har bir kadr o'rniga belgilangan 5-10 FPS chastotada kadr beradi.
        """
        while self.is_running:
            now = time.time()
            if (now - self.last_sampled_time) >= self.sample_interval:
                frame = self.get_latest_frame()
                if frame is not None:
                    self.last_sampled_time = now
                    yield frame, now
            time.sleep(0.005)

    def stop(self):
        """Oqimni xavfsiz to'xtatish"""
        self.is_running = False
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
        self.cap = None
