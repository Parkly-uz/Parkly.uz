"""
Parkly.uz — Adaptive Low-Light & Glare Enhancement
Kechasi faralar yog'dusi (glare) yoki qorong'i atrofda kontrastni avtomatik moslashtiruvchi modul.
"""

import cv2
import numpy as np
from typing import Tuple


class FrameEnhancer:
    """
    Tasvir sifatini yaxshilash va kechki rejimni boshqarish moduli.
    
    Qo'llaniladigan usullar:
    1. Yoritilganlik darajasi tahlili (Luminance Mean).
    2. CLAHE (Contrast Limited Adaptive Histogram Equalization) — lokal kontrastni yaxshilash.
    3. Adaptive Gamma Correction — yorug'lik darajasiga qarab dinamik yoritish/so'ndirish.
    4. Glare Reduction — kuchli fara nurlari bo'yicha yaltiroqlikni bosish.
    """

    LOW_LIGHT_THRESHOLD = 80.0    # Agar o'rtacha yorug'lik 80 dan past bo'lsa -> Qorong'i rejim
    HIGH_GLARE_THRESHOLD = 210.0  # Agar o'rtacha yorug'lik 210 dan baland bo'lsa -> Faralar yorishi

    @classmethod
    def calculate_brightness(cls, image: np.ndarray) -> float:
        """Tasvirning o'rtacha yorug'ligini (0-255 shkalasida) hisoblash"""
        if len(image.shape) == 3:
            # LAB rang fazosiga o'tkazib L (Luminance) kanalini olamiz
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l_channel = lab[:, :, 0]
            return float(np.mean(l_channel))
        return float(np.mean(image))

    @classmethod
    def apply_gamma_correction(cls, image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
        """Gamma korreksiyasi: gamma < 1.0 yoritadi (masalan 0.5), gamma > 1.0 qorong'ilashtiradi"""
        if abs(gamma - 1.0) < 0.05:
            return image
        # gamma < 1.0 bo'lganda (x ** gamma) qiymatni oshiradi (yoritadi)
        table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    @classmethod
    def apply_clahe(cls, image: np.ndarray, clip_limit: float = 2.5, grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """
        CLAHE: Rangli tasvirning LAB rang modelidagi L (yorug'lik) kanaliga adaptiv gistogramma tenglashtirish.
        Ranglarni buzmasdan faqat kontrastni va harflar aniqligini kuchaytiradi.
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
    def enhance_frame(cls, frame: np.ndarray) -> Tuple[np.ndarray, dict]:
        """
        Kadrdagi yorug'lik holatini tahlil qilib avtomatik moslashtiradi.
        """
        brightness = cls.calculate_brightness(frame)
        mode = "NORMAL"

        if brightness < cls.LOW_LIGHT_THRESHOLD:
            # 1. Qorong'i rejim: Gamma < 1.0 bilan yoritamiz va CLAHE qo'llaymiz
            mode = "LOW_LIGHT"
            gamma = 0.6 + (brightness / cls.LOW_LIGHT_THRESHOLD) * 0.3  # 0.6 dan 0.9 gacha
            brightened = cls.apply_gamma_correction(frame, gamma=gamma)
            enhanced = cls.apply_clahe(brightened, clip_limit=3.0)
        elif brightness > cls.HIGH_GLARE_THRESHOLD:
            # 2. Faralar yog'dusi / Kuchli porlash (Glare): Gammadan yuqori qiymat bilan so'ndiramiz
            mode = "HIGH_GLARE"
            enhanced = cls.apply_gamma_correction(frame, gamma=1.3)
        else:
            # 3. Normal yorug'lik: Engil CLAHE bilan detallarni o'tkirlashtiramiz
            enhanced = cls.apply_clahe(frame, clip_limit=1.5)

        stats = {
            "mode": mode,
            "raw_brightness": round(brightness, 2),
            "is_enhanced": mode != "NORMAL"
        }
        return enhanced, stats
