"""
Parkly.uz — Perspective Correction & Homography Alignment
Kamera rakursidan kelib chiquvchi qiyshayishlarni to'g'rilovchi geometrik transformatsiya.
"""

import cv2
import numpy as np
from typing import Tuple


class PerspectiveCorrector:
    """
    Raqam trapetsiya yoki qiyshiq burchak ostida turganda uni to'g'ri to'rtburchak
    (Frontal View) shakliga aylantirib tekislaydi.
    """

    @staticmethod
    def order_points(pts: np.ndarray) -> np.ndarray:
        """
        4 ta burchak nuqtani soat strelkasi bo'yicha tartiblash:
        [Yuqori-chap, Yuqori-o'ng, Pastki-o'ng, Pastki-chap]
        """
        rect = np.zeros((4, 2), dtype="float32")

        # Yuqori-chap (x + y eng kichik), Pastki-o'ng (x + y eng katta)
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # Yuqori-o'ng (y - x eng kichik / diff), Pastki-chap (y - x eng katta)
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    @classmethod
    def four_point_transform(cls, image: np.ndarray, pts: np.ndarray) -> np.ndarray:
        """
        OpenCV Homography matritsasi orqali tekis frontal tasvirga o'tkazish.
        """
        rect = cls.order_points(pts)
        (tl, tr, br, bl) = rect

        # Yangi to'g'rilangan to'rtburchakning eni (width) va bo'yini (height) hisoblash
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b))

        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b))

        if max_width <= 0 or max_height <= 0:
            return image

        # O'zbekiston davlat raqami uchun standart proporsiya (taxminan 4.5:1)
        # 470px x 110px o'lchamga normallashtirish
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype="float32")

        # Homography matritsasi
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (max_width, max_height))

        return warped

    @classmethod
    def align_plate(cls, plate_crop: np.ndarray, corners: np.ndarray = None) -> np.ndarray:
        """
        Raqam kesmasini tekislash va gorizontal holatga keltirish.
        """
        if corners is not None and len(corners) == 4:
            return cls.four_point_transform(plate_crop, corners.astype("float32"))

        # Agar burchaklar alohida berilmagan bo'lsa, kontur burchaklarini avtomatik qidiramiz
        gray = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)

        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                pts = approx.reshape(4, 2)
                return cls.four_point_transform(plate_crop, pts.astype("float32"))

        # Zaxira: rasmni o'z holicha qaytarish
        return plate_crop
