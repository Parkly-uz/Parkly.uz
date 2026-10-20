"""
Parkly.uz — Advanced Adaptive Low-Light, Fog & Glare Enhancement
Qorong'i, tuman, xira va kuchli yorug'lik sharoitida ANPR aniqligini keskin oshiruvchi vizual filtrlar.
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any


class FrameEnhancer:
    """
    Og'ir ob-havo va yorug'lik sharoitlari uchun kadrni optimallashtiruvchi intellektual filtr.

    Qo'llaniladigan usullar:
    1. CLAHE (Contrast Limited Adaptive Histogram Equalization) - qorong'i va xira joylarni yoritish.
    2. Bilateral Filtering - tuman va shovqinni (noise) kamaytirish, ammo raqam qirralarini keskin saqlash.
    3. Adaptive Gamma Correction - faralar nuri (glare) yoki qorong'ulikni tarqatish.
    """

    LOW_LIGHT_THRESHOLD = 75.0
    HIGH_GLARE_THRESHOLD = 215.0

    @classmethod
    def calculate_brightness(cls, image: np.ndarray) -> float:
        """Tasvirning o'rtacha yorug'ligini hisoblash (LAB rang fazosining L kanali)"""
        if len(image.shape) == 3:
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l_channel = lab[:, :, 0]
            return float(np.mean(l_channel))
        return float(np.mean(image))

    @classmethod
    def apply_gamma_correction(cls, image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
        """Gamma korreksiyasi (yoritish yoki qorong'ilashtirish)"""
        if abs(gamma - 1.0) < 0.05:
            return image
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    @classmethod
    def apply_clahe(cls, image: np.ndarray, clip_limit: float = 3.0, grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """
        CLAHE: Lokal kontrastni kuchaytirish (raqam harflarini ajratib ko'rsatish uchun).
        """
        if len(image.shape) == 3:
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
            cl = clahe.apply(l)
            enhanced_lab = cv2.merge((cl, a, b))
            return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        else:
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
            return clahe.apply(image)

    @classmethod
    def reduce_fog_and_noise(cls, image: np.ndarray) -> np.ndarray:
        """
        Bilateral Filter yordamida tuman va shovqinni tozalash, shu bilan birga qirralarning o'tkirligini saqlash.
        """
        # Bilateral filter qirralarni yumshatmasdan shovqinni yo'qotadi
        filtered = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
        return filtered

    @classmethod
    def enhance_frame(cls, frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Kadrdagi ob-havo va yorug'lik sharoitini aniqlab, mos filtrlarni qo'llash.
        """
        if frame is None or frame.size == 0:
            return frame, {"mode": "EMPTY", "brightness": 0.0}

        brightness = cls.calculate_brightness(frame)
        mode = "NORMAL"
        processed = frame.copy()

        # 1. Shovqinni va tumanni kamaytirish
        processed = cls.reduce_fog_and_noise(processed)

        # 2. Yorug'lik darajasiga qarab korreksiya
        if brightness < cls.LOW_LIGHT_THRESHOLD:
            mode = "LOW_LIGHT_FOG"
            # Qorong'i yoki tumanli sharoit: kuchli gamma yoritish + CLAHE
            gamma = 0.55 + (brightness / cls.LOW_LIGHT_THRESHOLD) * 0.35
            processed = cls.apply_gamma_correction(processed, gamma=gamma)
            processed = cls.apply_clahe(processed, clip_limit=3.5)
        elif brightness > cls.HIGH_GLARE_THRESHOLD:
            mode = "HIGH_GLARE"
            # Faralar nuri porlashi (Glare): Gamma orqali yumshatish
            processed = cls.apply_gamma_correction(processed, gamma=1.4)
            processed = cls.apply_clahe(processed, clip_limit=2.0)
        else:
            # Standart rejim: standart CLAHE
            processed = cls.apply_clahe(processed, clip_limit=2.0)

        stats = {
            "mode": mode,
            "brightness": round(brightness, 2),
            "is_enhanced": mode != "NORMAL"
        }
        return processed, stats
