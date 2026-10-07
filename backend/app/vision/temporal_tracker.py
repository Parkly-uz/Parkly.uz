"""
Parkly.uz — Tracking & Temporal Voting (Multi-Frame Consensus)
Mashina harakatlanganda olingan 5-10 ta kadr natijalarini to'plab, ko'pchilik ovozi
(Majority Voting) va ishonchlilik (Confidence Score) bo'yicha yakuniy aniq raqamni chiqaradi.
"""

import time
from collections import defaultdict
from typing import List, Dict, Optional, Tuple


class TemporalPlateTracker:
    """
    Vaqtinchalik konsensus (Multi-frame Consensus) kuzatuvchisi.
    """

    def __init__(
        self,
        window_seconds: float = 2.0,
        min_consensus_votes: int = 3,
        min_confidence_threshold: float = 0.70
    ):
        """
        :param window_seconds: Kadrlarni birlashtirish vaqti (standart 2 soniya)
        :param min_consensus_votes: Tasdiqlash uchun kamida nechta kadr bir xil bo'lishi kerak
        :param min_confidence_threshold: Minimal ishonchlilik koeffitsienti
        """
        self.window_seconds = window_seconds
        self.min_consensus_votes = min_consensus_votes
        self.min_confidence_threshold = min_confidence_threshold

        # Tarix: list of dicts: {"plate": str, "confidence": float, "timestamp": float}
        self.history: List[Dict] = []

    def add_detection(self, plate_number: str, confidence: float, timestamp: Optional[float] = None):
        """Yangi aniqlangan kadr natijasini qo'shish"""
        ts = timestamp or time.time()
        if plate_number and confidence >= self.min_confidence_threshold:
            self.history.append({
                "plate": plate_number,
                "confidence": confidence,
                "timestamp": ts
            })
        self._prune_history(ts)

    def _prune_history(self, current_time: float):
        """Eski (2 soniyadan o'tib ketgan) kadrlarni tozalash"""
        cutoff = current_time - self.window_seconds
        self.history = [item for item in self.history if item["timestamp"] >= cutoff]

    def get_consensus(self) -> Optional[Tuple[str, float, int]]:
        """
        Ko'pchilik ovozi (Weighted Voting) orqali yakuniy natijani hisoblash.
        
        :return: (winner_plate, average_confidence, vote_count) yoki None
        """
        if not self.history:
            return None

        votes = defaultdict(int)
        conf_sum = defaultdict(float)

        for item in self.history:
            plate = item["plate"]
            votes[plate] += 1
            conf_sum[plate] += item["confidence"]

        # Eng ko'p ovoz olgan nomzodni topish
        sorted_plates = sorted(votes.items(), key=lambda x: (x[1], conf_sum[x[0]]), reverse=True)
        winner_plate, vote_count = sorted_plates[0]

        if vote_count >= self.min_consensus_votes:
            avg_conf = conf_sum[winner_plate] / vote_count
            return winner_plate, round(avg_conf, 2), vote_count

        return None

    def reset(self):
        """Yangi mashina kelganda buferni tozalash"""
        self.history.clear()
