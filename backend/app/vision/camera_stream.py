"""
Parkly.uz — Universal Camera Stream Ingestion & Auto-Reconnect Driver
Istalgan RTSP kamera, USB veb-kamera yoki sinov video faylini qo'llab-quvvatlaydi.
Tarmoq uzilishlarida avtomatik qayta ulanish (Auto-reconnect) va bufer to'lib qolishining oldini oladi.
"""

import cv2
import time
import threading
import logging
from typing import Optional, Union, Generator, Tuple
import numpy as np

logger = logging.getLogger("CameraStream")

class CameraStream:
    """
    Universal va ishonchli kamera oqimi boshqaruvchisi.
    """

    def __init__(
        self,
        source: Union[str, int] = 0,
        target_fps: int = 10,
        name: str = "Camera-Node",
        reconnect_interval: float = 3.0
    ):
        """
        :param source: RTSP URL (masalan 'rtsp://user:pass@ip:557/stream'), USB (0, 1) yoki video fayl yo'li ('test.mp4')
        :param target_fps: AI ga uzatiladigan kadrlar chastotasi (standart: 10 FPS)
        :param name: Kamera nomi / identifikatori
        :param reconnect_interval: Tarmoq uzilganda qayta ulanishga urinish oralig'i (soniya)
        """
        self.source = source
        self.target_fps = target_fps
        self.name = name
        self.reconnect_interval = reconnect_interval
        self.sample_interval = 1.0 / max(1, target_fps)

        self.cap: Optional[cv2.VideoCapture] = None
        self.latest_frame: Optional[np.ndarray] = None
        self.frame_lock = threading.Lock()
        self.is_running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.last_sampled_time = 0.0
        self.is_connected = False

    def start(self) -> bool:
        """Kamera oqimini ishga tushirish va fondagi oqimni boshlash"""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._connection_and_capture_loop, daemon=True)
        self.worker_thread.start()
        return True

    def _connect(self) -> bool:
        """Kameraga ulanish va buferni minimal qilish"""
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass

        logger.info(f"[{self.name}] Kameraga ulanilmoqda: {self.source}")

        # Agar source raqam (masalan 0) bo'lsa int ga o'tkazamiz
        src = self.source
        if isinstance(src, str) and src.isdigit():
            src = int(src)

        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            logger.warning(f"[{self.name}] Kameraga ulanib bo'lmadi: {self.source}")
            self.is_connected = False
            return False

        # RTSP va veb-kamera uchun kadrlar buferini 1 ta kadrga cheklash (kechikishning oldini olish)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.is_connected = True
        logger.info(f"[{self.name}] Kamera muvaffaqiyatli ulandi!")
        return True

    def _connection_and_capture_loop(self):
        """Ulanishni doimiy kuzatuvchi va avtomatik qayta ulanuvchi (Auto-reconnect) asosiy sikl"""
        reconnect_attempts = 0

        while self.is_running:
            if not self.is_connected or not self.cap or not self.cap.isOpened():
                connected = self._connect()
                if not connected:
                    reconnect_attempts += 1
                    time.sleep(self.reconnect_interval)
                    continue
                reconnect_attempts = 0

            ret, frame = self.cap.read()
            if not ret or frame is None:
                logger.warning(f"[{self.name}] Kadr o'qishda xatolik yoki oqim uzildi. Qayta ulanmoqda...")
                self.is_connected = False
                time.sleep(1.0)
                continue

            with self.frame_lock:
                self.latest_frame = frame

    def get_latest_frame(self) -> Optional[np.ndarray]:
        """Eng oxirgi kadrni thread-safe tarzda olish"""
        with self.frame_lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
        return None

    def sample_generator(self) -> Generator[Tuple[np.ndarray, float], None, None]:
        """
        Frame Sampler: Kerakli FPS chastotasida kadrlar generatori.
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
        """Oqimni to'xtatish va resurslarni bo'shatish"""
        self.is_running = False
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)
        if self.cap:
            self.cap.release()
            self.cap = None
        self.is_connected = False
        logger.info(f"[{self.name}] Kamera oqimi yopildi.")
