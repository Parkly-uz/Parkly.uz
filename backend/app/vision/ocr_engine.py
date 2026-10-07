"""
Parkly.uz — OCR & Uzbekistan Plate Pattern Recognition Engine
Tekislangan raqam tasviridan matnni o'qish, O'zbekiston shabloniga tushirish va belgilarni tuzatish.
"""

import re
import cv2
import numpy as np
from typing import Dict, Any, Optional, Tuple


class UzbekistanPlateOCR:
    """
    O'zbekiston davlat raqamlari uchun ixtisoslashgan OCR va mantiqiy filtr.
    
    Qo'llab-quvvatlanadigan formatlar:
    1. Jismoniy shaxslar: '01 A 777 AA'  (2 raqam + 1 harf + 3 raqam + 2 harf)
    2. Yuridik shaxslar:  '01 777 AAA'   (2 raqam + 3 raqam + 3 harf)
    """

    # O'zbekiston viloyatlari kodlari
    VALID_REGIONS = {
        "01", "10", "20", "25", "30", "40", "50", "60", "70", "75", "80", "85", "90", "95"
    }

    # Raqam o'rnida xato o'qilgan harflarni tuzatish
    DIGIT_FIXES = {
        'O': '0', 'D': '0', 'Q': '0',
        'I': '1', 'L': '1', '|': '1', 'T': '1',
        'Z': '2',
        'S': '5',
        'G': '6', 'b': '6',
        'B': '8',
    }

    # Harf o'rnida xato o'qilgan raqamlarni tuzatish
    CHAR_FIXES = {
        '0': 'O',
        '1': 'I',
        '2': 'Z',
        '5': 'S',
        '6': 'G',
        '8': 'B'
    }

    @classmethod
    def preprocess_plate_for_ocr(cls, plate_image: np.ndarray) -> np.ndarray:
        """OCR sifatini oshirish uchun tasvirni binarizatsiya qilish va shovqinlarni tozalash"""
        if len(plate_image.shape) == 3:
            gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = plate_image

        # O'lchamni standartlashtirish (kattalashtirish harflarni o'qishni yengillashtiradi)
        resized = cv2.resize(gray, (240, 60), interpolation=cv2.INTER_CUBIC)

        # Otsu binarizatsiya
        blurred = cv2.GaussianBlur(resized, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    @classmethod
    def normalize_individual_plate(cls, text: str) -> Optional[str]:
        """
        Jismoniy shaxs formati: 01 A 777 AA (Jami 8 ta belgi)
        Pozitsiyalar:
        [0, 1] -> Raqam (Hudud)
        [2]    -> Harf (Seriya)
        [3,4,5]-> Raqam (Raqam bloki)
        [6, 7] -> Harf (Seriya)
        """
        clean = re.sub(r'[^A-Za-z0-9]', '', text).upper()
        if len(clean) != 8:
            return None

        chars = list(clean)

        # 0, 1 -> Raqam
        chars[0] = cls.DIGIT_FIXES.get(chars[0], chars[0])
        chars[1] = cls.DIGIT_FIXES.get(chars[1], chars[1])

        # 2 -> Harf
        chars[2] = cls.CHAR_FIXES.get(chars[2], chars[2])

        # 3, 4, 5 -> Raqam
        chars[3] = cls.DIGIT_FIXES.get(chars[3], chars[3])
        chars[4] = cls.DIGIT_FIXES.get(chars[4], chars[4])
        chars[5] = cls.DIGIT_FIXES.get(chars[5], chars[5])

        # 6, 7 -> Harf
        chars[6] = cls.CHAR_FIXES.get(chars[6], chars[6])
        chars[7] = cls.CHAR_FIXES.get(chars[7], chars[7])

        region = chars[0] + chars[1]
        letter_mid = chars[2]
        num_block = chars[3] + chars[4] + chars[5]
        letter_end = chars[6] + chars[7]

        # Tekshiruv: format to'g'ri keldimi?
        if region.isdigit() and letter_mid.isalpha() and num_block.isdigit() and letter_end.isalpha():
            return f"{region} {letter_mid} {num_block} {letter_end}"
        return None

    @classmethod
    def normalize_company_plate(cls, text: str) -> Optional[str]:
        """
        Yuridik shaxs formati: 01 777 AAA (Jami 8 ta belgi)
        Pozitsiyalar:
        [0, 1]   -> Raqam (Hudud)
        [2, 3, 4]-> Raqam (Raqam bloki)
        [5, 6, 7]-> Harf (Seriya)
        """
        clean = re.sub(r'[^A-Za-z0-9]', '', text).upper()
        if len(clean) != 8:
            return None

        chars = list(clean)

        # 0, 1, 2, 3, 4 -> Raqam
        for i in range(5):
            chars[i] = cls.DIGIT_FIXES.get(chars[i], chars[i])

        # 5, 6, 7 -> Harf
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
        Xom OCR natijasini O'zbekiston formatlariga solishtirish va eng ishonchlisini tanlash.
        """
        raw_clean = re.sub(r'[^A-Za-z0-9]', '', raw_text).upper()

        # 1. Jismoniy shaxs tekshiruvi
        individual = cls.normalize_individual_plate(raw_clean)
        if individual:
            return {
                "plate_number": individual,
                "type": "INDIVIDUAL",
                "is_valid": True,
                "confidence": 0.94
            }

        # 2. Yuridik shaxs tekshiruvi
        company = cls.normalize_company_plate(raw_clean)
        if company:
            return {
                "plate_number": company,
                "type": "COMPANY",
                "is_valid": True,
                "confidence": 0.92
            }

        # 3. Agar 8 tadan sal farq qilsa, umumiy tozalangan matnni qaytaramiz
        return {
            "plate_number": raw_clean,
            "type": "UNKNOWN",
            "is_valid": False,
            "confidence": 0.50
        }
