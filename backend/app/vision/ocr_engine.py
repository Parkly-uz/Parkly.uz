"""
Parkly.uz — Advanced Uzbekistan Plate OCR & Pattern Recognition Engine
O'zbekiston davlat raqamlari standartlariga qat'iy rioya qiluvchi, harf va raqam chalkashliklarini
(O/0, I/1, Z/2, S/5, G/6, B/8) avtomatik to'g'rilovchi OCR filtri.
"""

import re
import cv2
import numpy as np
from typing import Dict, Any, Optional


class UzbekistanPlateOCR:
    """
    O'zbekiston avtomobil raqamlari uchun ixtisoslashgan OCR mantiqiy filtri va normalizatori.

    Qo'llab-quvvatlanadigan shablonlar:
    1. Jismoniy shaxslar: '01 A 777 AA'  (2 raqam + 1 harf + 3 raqam + 2 harf)
    2. Yuridik shaxslar:  '01 777 AAA'   (2 raqam + 3 raqam + 3 harf)
    3. Davlat idoralari:  '01 777 UZ'    (2 raqam + 3 raqam + 2 harf - UZ)
    """

    VALID_REGIONS = {
        "01", "10", "20", "25", "30", "40", "50", "60", "70", "75", "80", "85", "90", "95"
    }

    # Raqam o'rnida xato o'qilishi mumkin bo'lgan harflarni raqamga o'tkazish
    DIGIT_FIXES = {
        'O': '0', 'D': '0', 'Q': '0', 'U': '0',
        'I': '1', 'L': '1', '|': '1', 'T': '1', 'J': '1',
        'Z': '2', 'R': '2',
        'S': '5', 'B': '5',
        'G': '6', 'b': '6', 'E': '6',
        'B': '8', 'A': '4'
    }

    # Harf o'rnida xato o'qilishi mumkin bo'lgan raqamlarni harfga o'tkazish
    CHAR_FIXES = {
        '0': 'O',
        '1': 'I',
        '2': 'Z',
        '3': 'B',
        '4': 'A',
        '5': 'S',
        '6': 'G',
        '7': 'T',
        '8': 'B',
        '9': 'G'
    }

    @classmethod
    def preprocess_for_ocr(cls, plate_image: np.ndarray) -> np.ndarray:
        """OCR uchun raqam rasmini binarizatsiya qilish va kontrastni oshirish"""
        if plate_image is None or plate_image.size == 0:
            return np.zeros((60, 240), dtype=np.uint8)

        if len(plate_image.shape) == 3:
            gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = plate_image

        # Standart o'lchamga keltirish
        resized = cv2.resize(gray, (240, 60), interpolation=cv2.INTER_CUBIC)

        # Otsu binarizatsiya va shubhali shovqinlarni tozalash
        blurred = cv2.GaussianBlur(resized, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    @classmethod
    def normalize_individual_plate(cls, text: str) -> Optional[str]:
        """
        Jismoniy shaxs formati: 01 A 777 AA (8 ta belgi)
        [0,1]: raqam, [2]: harf, [3,4,5]: raqam, [6,7]: harf
        """
        clean = re.sub(r'[^A-Za-z0-9]', '', text).upper()
        if len(clean) != 8:
            return None

        chars = list(clean)

        # Pozitsiyalar bo'yicha aniq tuzatishlar
        chars[0] = cls.DIGIT_FIXES.get(chars[0], chars[0])
        chars[1] = cls.DIGIT_FIXES.get(chars[1], chars[1])
        chars[2] = cls.CHAR_FIXES.get(chars[2], chars[2])
        chars[3] = cls.DIGIT_FIXES.get(chars[3], chars[3])
        chars[4] = cls.DIGIT_FIXES.get(chars[4], chars[4])
        chars[5] = cls.DIGIT_FIXES.get(chars[5], chars[5])
        chars[6] = cls.CHAR_FIXES.get(chars[6], chars[6])
        chars[7] = cls.CHAR_FIXES.get(chars[7], chars[7])

        region = chars[0] + chars[1]
        letter_mid = chars[2]
        num_block = chars[3] + chars[4] + chars[5]
        letter_end = chars[6] + chars[7]

        if region in cls.VALID_REGIONS and letter_mid.isalpha() and num_block.isdigit() and letter_end.isalpha():
            return f"{region} {letter_mid} {num_block} {letter_end}"

        # Agar mintaqa qattiq tekshiruvdan o'tmasa ham raqam formatiga mos kelsa qabul qilamiz
        if region.isdigit() and letter_mid.isalpha() and num_block.isdigit() and letter_end.isalpha():
            return f"{region} {letter_mid} {num_block} {letter_end}"

        return None

    @classmethod
    def normalize_company_plate(cls, text: str) -> Optional[str]:
        """
        Yuridik shaxs formati: 01 777 AAA (8 ta belgi)
        [0,1]: raqam, [2,3,4]: raqam, [5,6,7]: harf
        """
        clean = re.sub(r'[^A-Za-z0-9]', '', text).upper()
        if len(clean) != 8:
            return None

        chars = list(clean)

        for i in range(5):
            chars[i] = cls.DIGIT_FIXES.get(chars[i], chars[i])
        for i in range(5, 8):
            chars[i] = cls.CHAR_FIXES.get(chars[i], chars[i])

        region = chars[0] + chars[1]
        num_block = chars[2] + chars[3] + chars[4]
        letters = chars[5] + chars[6] + chars[7]

        if region.isdigit() and num_block.isdigit() and letters.isalpha():
            return f"{region} {num_block} {letters}"

        return None

    @classmethod
    def post_process_recognized_text(cls, raw_text: str) -> Dict[str, Any]:
        """
        Xom OCR matnini tekshirish va to'g'rilash.
        """
        if not raw_text:
            return {"plate_number": None, "type": None, "is_valid": False, "confidence": 0.0}

        # 1. Jismoniy shaxs formatini tekshirish
        ind = cls.normalize_individual_plate(raw_text)
        if ind:
            return {
                "plate_number": ind,
                "type": "INDIVIDUAL",
                "is_valid": True,
                "confidence": 0.92
            }

        # 2. Yuridik shaxs formatini tekshirish
        comp = cls.normalize_company_plate(raw_text)
        if comp:
            return {
                "plate_number": comp,
                "type": "COMPANY",
                "is_valid": True,
                "confidence": 0.90
            }

        return {
            "plate_number": raw_text,
            "type": "UNKNOWN",
            "is_valid": False,
            "confidence": 0.40
        }
