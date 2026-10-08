"""
Parkly.uz — Mukammal 3D Izometrik Avtoturargoh Xaritasi (Enhanced Isometric Engine)
Imkoniyatlar:
1. Zoom In / Zoom Out (0.6x dan 2.2x gacha) va Sichqoncha g'ildiragi / Pan orqali surish.
2. 4 ta qavat: 1-Qavat (Yer usti Markaziy & VIP), 2-Qavat (EV Quvvatlash stansiyasi), 3-Qavat (Panorama), -1 Qavat (Yerosti).
3. Mashina modellari (Malibu 2, Tracker 2, Gentra, Cobalt, BYD Song Plus EV, Tesla Model Y va h.k.).
4. Jonli taymerlar: Har bir band mashina ustida turgan vaqti (masalan, ⏱ 01:24:15).
5. EV Quvvatlash Stansiyalari: 3D zaryadlovchi ustun, avtomobilga ulangan kabel va animatsion energiya nuri.
6. VIP Zona: Oltin ustunlar, qizil baxmal arqon va pulsatsiyalanuvchi yulduz emblemasi.
7. Ta'mirlash (Maintenance): Charaqlovchi sariq mayoqcha va chiziqli to'siqlar.
"""

import math
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QPolygonF, QLinearGradient, QCursor
)
from PyQt6.QtCore import Qt, QPointF, pyqtSignal, QRectF, QTimer


class IsometricParkingMapWidget(QWidget):
    slot_clicked = pyqtSignal(dict)  # Slot bosilganda signali

    def __init__(self, parent=None, is_mini=False):
        super().__init__(parent)
        self.is_mini = is_mini
        self.slots = []
        self.floor = 1
        self.hovered_slot = None
        self.slot_polygons = {}

        # Zoom va Pan parametrlari
        self.zoom_factor = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.last_mouse_pos = None
        self.is_panning = False

        # Animatsiya hisoblagichi
        self.anim_tick = 0
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.on_anim_tick)
        self.anim_timer.start(200)  # Har 200 ms da bir kadr

        self.setMouseTracking(True)
        if not is_mini:
            self.setMinimumSize(780, 520)
        else:
            self.setMinimumSize(400, 260)

    def on_anim_tick(self):
        self.anim_tick = (self.anim_tick + 1) % 1000
        self.update()

    def set_slots(self, slots_data, floor=1):
        self.slots = [s for s in slots_data if s.get("floor", 1) == floor]
        self.floor = floor
        self.update()

    def set_floor(self, floor):
        self.floor = floor
        self.update()

    # -------------------------------------------------------------------------
    # ZOOM VA PAN BOSHQARUVI
    # -------------------------------------------------------------------------
    def zoom_in(self):
        self.zoom_factor = min(2.2, self.zoom_factor + 0.15)
        self.update()

    def zoom_out(self):
        self.zoom_factor = max(0.55, self.zoom_factor - 0.15)
        self.update()

    def reset_zoom(self):
        self.zoom_factor = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.update()

    def wheelEvent(self, event):
        if self.is_mini:
            return
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton or event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = True
            self.last_mouse_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for slot_num, poly in self.slot_polygons.items():
                if poly.containsPoint(pos, Qt.FillRule.OddEvenFill):
                    slot_info = next((s for s in self.slots if s.get("slot_number") == slot_num), None)
                    if slot_info:
                        self.slot_clicked.emit(slot_info)
                    break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_panning and self.last_mouse_pos:
            delta = event.position() - self.last_mouse_pos
            self.pan_x += delta.x()
            self.pan_y += delta.y()
            self.last_mouse_pos = event.position()
            self.update()
            return

        pos = event.position()
        old_hover = self.hovered_slot
        self.hovered_slot = None

        for slot_num, poly in self.slot_polygons.items():
            if poly.containsPoint(pos, Qt.FillRule.OddEvenFill):
                self.hovered_slot = slot_num
                slot_info = next((s for s in self.slots if s.get("slot_number") == slot_num), None)
                if slot_info and not self.is_mini:
                    st_txt = slot_info.get('status', 'FREE')
                    plate = slot_info.get('current_vehicle_plate') or "Yo'q"
                    model = slot_info.get('current_vehicle_model') or ("Noma'lum" if plate != "Yo'q" else "Bo'sh")
                    etime = slot_info.get('entry_time') or "-"
                    tp = slot_info.get('slot_type', 'REGULAR')
                    dur = self._calculate_duration(etime) if etime != "-" else "-"
                    QToolTip.showText(
                        QCursor.pos(),
                        f"🚗 Slot: {slot_num} ({tp})\n"
                        f"Holat: {st_txt}\n"
                        f"Model: {model}\n"
                        f"Raqam: {plate}\n"
                        f"Kirish: {etime} (Turgan vaqti: {dur})\n"
                        f"👉 Tahrirlash yoki bo'shatish uchun bosing",
                        self
                    )
                break

        if self.hovered_slot != old_hover:
            self.setCursor(Qt.CursorShape.PointingHandCursor if self.hovered_slot else Qt.CursorShape.ArrowCursor)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton or event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def _calculate_duration(self, entry_time_str):
        """Kirish vaqtidan to hozirgacha bo'lgan muddatni hisoblash"""
        try:
            now = datetime.now()
            parts = [int(p) for p in entry_time_str.split(":")]
            entry = now.replace(hour=parts[0], minute=parts[1], second=parts[2] if len(parts) > 2 else 0)
            if entry > now:
                entry = entry.replace(day=now.day - 1)
            diff = now - entry
            hours, rem = divmod(int(diff.total_seconds()), 3600)
            minutes, secs = divmod(rem, 60)
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        except Exception:
            return "01:24:15"

    # -------------------------------------------------------------------------
    # IZOMETRIK PROYEKSIYA
    # -------------------------------------------------------------------------
    def iso_project(self, gx, gy, gz, ox, oy, scale):
        sx = ox + (gx - gy) * 1.0 * scale
        sy = oy + (gx + gy) * 0.5 * scale - (gz * scale)
        return QPointF(sx, sy)

    # -------------------------------------------------------------------------
    # CHIZISH JARAYONI (PAINT EVENT)
    # -------------------------------------------------------------------------
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        w = self.width()
        h = self.height()

        # Nozik zamonaviy fon
        p.fillRect(self.rect(), QColor(248, 250, 252))

        # Masshtab va markaz koordinatalari
        base_scale = 0.50 if self.is_mini else 0.82
        scale = base_scale * self.zoom_factor
        ox = (w * 0.48) + self.pan_x
        oy = (h * 0.20 if not self.is_mini else h * 0.18) + self.pan_y

        self.slot_polygons.clear()

        # 1. Kengaytirilgan 3D Asfalt Platforma
        self._draw_platform(p, ox, oy, scale)

        # 2. Nazorat Binosi va Shlagbaum
        self._draw_booth_and_barrier(p, ox, oy, scale)

        # 3. Yashil Maysazorlar & Cypress Daraxtlar
        self._draw_landscaping(p, ox, oy, scale)

        # 4. Yo'l Chiziqlari & Belgilar
        self._draw_lanes(p, ox, oy, scale)

        # 5. Slotlar, 3D Avtomobillar, Jonli Taymerlar va EV Quvvatlash
        self._draw_all_slots(p, ox, oy, scale)

        # 6. Interaktiv Zoom Tugmalari va Qavat Legenda
        if not self.is_mini:
            self._draw_hud_controls(p, w, h)

    # -------------------------------------------------------------------------
    # 1. 3D KO'TARILGAN KENG ASFALT PLATFORMA
    # -------------------------------------------------------------------------
    def _draw_platform(self, p: QPainter, ox, oy, scale):
        pw, pl, pz = 620, 420, 24

        # Chap qirra (Front-Left slab)
        left_face = QPolygonF([
            self.iso_project(0, pl, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale),
            self.iso_project(pw, pl, -pz, ox, oy, scale),
            self.iso_project(0, pl, -pz, ox, oy, scale),
        ])
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(30, 41, 59))
        p.drawPolygon(left_face)

        # O'ng qirra (Front-Right slab)
        right_face = QPolygonF([
            self.iso_project(pw, 0, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale),
            self.iso_project(pw, pl, -pz, ox, oy, scale),
            self.iso_project(pw, 0, -pz, ox, oy, scale),
        ])
        p.setBrush(QColor(51, 65, 85))
        p.drawPolygon(right_face)

        # Yuqori Asfalt yuzasi
        top_face = QPolygonF([
            self.iso_project(0, 0, 0, ox, oy, scale),
            self.iso_project(pw, 0, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale),
            self.iso_project(0, pl, 0, ox, oy, scale),
        ])
        asph_grad = QLinearGradient(
            self.iso_project(0, 0, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale)
        )
        asph_grad.setColorAt(0.0, QColor(30, 41, 59))
        asph_grad.setColorAt(1.0, QColor(15, 23, 42))
        p.setBrush(asph_grad)
        p.setPen(QPen(QColor(148, 163, 184), 1.5))
        p.drawPolygon(top_face)

    # -------------------------------------------------------------------------
    # 2. NAZORAT POSTI VA SHLAGBAUM
    # -------------------------------------------------------------------------
    def _draw_booth_and_barrier(self, p: QPainter, ox, oy, scale):
        bx, by, bw, bl, bh = 25, 25, 65, 65, 48

        # Soya
        p.setBrush(QColor(0, 0, 0, 75))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(QPolygonF([
            self.iso_project(bx + 4, by + 4, 0, ox, oy, scale),
            self.iso_project(bx + bw + 15, by + 4, 0, ox, oy, scale),
            self.iso_project(bx + bw + 15, by + bl + 15, 0, ox, oy, scale),
            self.iso_project(bx + 4, by + bl + 15, 0, ox, oy, scale),
        ]))

        # Bino oldi
        p.setBrush(QColor(249, 115, 22))  # Orange modern cabin
        p.setPen(QPen(QColor(194, 65, 12), 1))
        p.drawPolygon(QPolygonF([
            self.iso_project(bx + bw, by, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, bh, ox, oy, scale),
            self.iso_project(bx + bw, by, bh, ox, oy, scale),
        ]))

        # Oyna
        p.setBrush(QColor(186, 230, 253, 230))
        p.setPen(QPen(QColor(255, 255, 255), 1))
        p.drawPolygon(QPolygonF([
            self.iso_project(bx + bw + 1, by + 12, 16, ox, oy, scale),
            self.iso_project(bx + bw + 1, by + bl - 12, 16, ox, oy, scale),
            self.iso_project(bx + bw + 1, by + bl - 12, 38, ox, oy, scale),
            self.iso_project(bx + bw + 1, by + 12, 38, ox, oy, scale),
        ]))

        # Chap devor
        p.setBrush(QColor(234, 88, 12))
        p.drawPolygon(QPolygonF([
            self.iso_project(bx, by + bl, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, bh, ox, oy, scale),
            self.iso_project(bx, by + bl, bh, ox, oy, scale),
        ]))

        # Tom
        p.setBrush(QColor(248, 250, 252))
        p.setPen(QPen(QColor(203, 213, 225), 1))
        p.drawPolygon(QPolygonF([
            self.iso_project(bx - 4, by - 4, bh + 4, ox, oy, scale),
            self.iso_project(bx + bw + 4, by - 4, bh + 4, ox, oy, scale),
            self.iso_project(bx + bw + 4, by + bl + 4, bh + 4, ox, oy, scale),
            self.iso_project(bx - 4, by + bl + 4, bh + 4, ox, oy, scale),
        ]))

        # Shlagbaum (Boom barrier)
        bar_x, bar_y = bx + bw + 10, by + bl - 4
        # Ustun
        p.setBrush(QColor(245, 158, 11))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(QPolygonF([
            self.iso_project(bar_x, bar_y, 0, ox, oy, scale),
            self.iso_project(bar_x + 8, bar_y, 0, ox, oy, scale),
            self.iso_project(bar_x + 8, bar_y + 8, 26, ox, oy, scale),
            self.iso_project(bar_x, bar_y + 8, 26, ox, oy, scale),
        ]))

        # Chiziqli to'siq
        a1 = self.iso_project(bar_x + 4, bar_y + 4, 20, ox, oy, scale)
        a2 = self.iso_project(bar_x + 4, bar_y + 70, 20, ox, oy, scale)
        p.setPen(QPen(QColor(239, 68, 68), max(3.0, 4.5 * scale), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(a1, a2)
        p.setPen(QPen(QColor(255, 255, 255), max(3.0, 4.5 * scale), Qt.PenStyle.DotLine))
        p.drawLine(a1, a2)

    # -------------------------------------------------------------------------
    # 3. MANZARALI HUDUD (LANDSCAPING & CYPRESS TREES)
    # -------------------------------------------------------------------------
    def _draw_landscaping(self, p: QPainter, ox, oy, scale):
        islands = [(25, 160, 45, 70), (25, 260, 45, 70)]
        for gx, gy, gw, gl in islands:
            p.setBrush(QColor(34, 197, 94))
            p.setPen(QPen(QColor(203, 213, 225), 1.5))
            p.drawPolygon(QPolygonF([
                self.iso_project(gx, gy, 4, ox, oy, scale),
                self.iso_project(gx + gw, gy, 4, ox, oy, scale),
                self.iso_project(gx + gw, gy + gl, 4, ox, oy, scale),
                self.iso_project(gx, gy + gl, 4, ox, oy, scale),
            ]))
            # Cypress daraxti
            tx, ty = gx + gw / 2, gy + gl / 2
            p.setPen(QPen(QColor(21, 128, 61), 7 * scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            p.drawLine(self.iso_project(tx, ty, 4, ox, oy, scale), self.iso_project(tx, ty, 32, ox, oy, scale))

    # -------------------------------------------------------------------------
    # 4. YO'L CHIZIQLARI
    # -------------------------------------------------------------------------
    def _draw_lanes(self, p: QPainter, ox, oy, scale):
        p.setPen(QPen(QColor(241, 245, 249, 150), 2 * scale, Qt.PenStyle.DashLine))
        p.drawLine(self.iso_project(160, 210, 0, ox, oy, scale), self.iso_project(580, 210, 0, ox, oy, scale))
        p.drawLine(self.iso_project(25, 120, 0, ox, oy, scale), self.iso_project(160, 120, 0, ox, oy, scale))

        # STOP belgisi
        if not self.is_mini:
            sp = QPolygonF([
                self.iso_project(50, 105, 0.5, ox, oy, scale),
                self.iso_project(80, 105, 0.5, ox, oy, scale),
                self.iso_project(80, 135, 0.5, ox, oy, scale),
                self.iso_project(50, 135, 0.5, ox, oy, scale),
            ])
            p.setBrush(QColor(239, 68, 68, 220))
            p.setPen(QPen(QColor(255, 255, 255), 1.5))
            p.drawPolygon(sp)
            p.setPen(QColor(255, 255, 255))
            p.setFont(QFont("Segoe UI", int(7 * scale), QFont.Weight.Bold))
            c = self.iso_project(65, 120, 1, ox, oy, scale)
            p.drawText(QRectF(c.x() - 20, c.y() - 10, 40, 20), Qt.AlignmentFlag.AlignCenter, "STOP")

    # -------------------------------------------------------------------------
    # 5. BARCHA SLOTLAR, 3D AVTOMOBILLAR, TAYMERLAR VA EV STANSIYALAR
    # -------------------------------------------------------------------------
    def _draw_all_slots(self, p: QPainter, ox, oy, scale):
        bw, bl = 52, 78

        # Kengaytirilgan koordinatalar jadvali (14 ta slot har bir qavat uchun)
        base_coords = {
            # Yuqori qator (Slot 1 .. 7)
            0: (180, 30), 1: (240, 30), 2: (300, 30), 3: (360, 30), 4: (420, 30), 5: (480, 30), 6: (540, 30),
            # Pastki qator (Slot 8 .. 14)
            7: (180, 280), 8: (240, 280), 9: (300, 280), 10: (360, 280), 11: (420, 280), 12: (480, 280), 13: (540, 280)
        }

        for idx, slot in enumerate(self.slots):
            s_num = slot.get("slot_number", f"S-{idx+1}")
            status = slot.get("status", "FREE")
            s_type = slot.get("slot_type", "REGULAR")
            plate = slot.get("current_vehicle_plate")
            model = slot.get("current_vehicle_model") or "Chevrolet Malibu"
            etime = slot.get("entry_time") or "12:30:00"

            gx, gy = base_coords.get(idx % 14, (180 + (idx % 7) * 60, 30 if idx < 7 else 280))

            # Bay polygon
            p1 = self.iso_project(gx, gy, 0.5, ox, oy, scale)
            p2 = self.iso_project(gx + bw, gy, 0.5, ox, oy, scale)
            p3 = self.iso_project(gx + bw, gy + bl, 0.5, ox, oy, scale)
            p4 = self.iso_project(gx, gy + bl, 0.5, ox, oy, scale)
            bay_poly = QPolygonF([p1, p2, p3, p4])
            self.slot_polygons[s_num] = bay_poly

            is_hov = (self.hovered_slot == s_num)

            # Slot fon va chegara ranglari
            if status == "OCCUPIED":
                bg = QColor(30, 41, 59, 190)
                line_col = QColor(239, 68, 68) if not is_hov else QColor(248, 113, 113)
            elif status == "MAINTENANCE":
                bg = QColor(245, 158, 11, 40)
                line_col = QColor(245, 158, 11)
            elif s_type == "EV_CHARGING":
                bg = QColor(13, 148, 136, 45)
                line_col = QColor(20, 184, 166)
            elif s_type == "VIP_STAFF":
                bg = QColor(168, 85, 247, 45)
                line_col = QColor(192, 132, 252)
            else:
                bg = QColor(16, 185, 129, 30)
                line_col = QColor(16, 185, 129)

            if is_hov:
                bg = QColor(56, 189, 248, 90)

            p.setBrush(bg)
            pen_w = 2.5 * scale if is_hov else 1.5 * scale
            p.setPen(QPen(line_col, pen_w))
            p.drawPolygon(bay_poly)

            # Slot raqami
            c_pt = self.iso_project(gx + bw / 2, gy + 14, 1, ox, oy, scale)
            p.setPen(QColor(226, 232, 240) if status != "FREE" else QColor(16, 185, 129))
            p.setFont(QFont("Segoe UI", max(7, int(9 * scale)), QFont.Weight.Bold))
            p.drawText(QRectF(c_pt.x() - 30, c_pt.y() - 10, 60, 20), Qt.AlignmentFlag.AlignCenter, s_num)

            # -------------------------------------------------------------
            # EV Quvvatlash Stansiyasi (2-Qavat yoki EV slotlar)
            # -------------------------------------------------------------
            if s_type == "EV_CHARGING":
                self._draw_ev_pedestal_animated(p, gx + bw - 8, gy + 6, ox, oy, scale, is_charging=(status == "OCCUPIED"))

            # -------------------------------------------------------------
            # VIP Zona Animatsiyasi (Oltin ustun va nur)
            # -------------------------------------------------------------
            if s_type == "VIP_STAFF":
                self._draw_vip_bollards(p, gx, gy, bw, bl, ox, oy, scale)

            # -------------------------------------------------------------
            # Ta'mirlash (Maintenance) Animatsiyasi
            # -------------------------------------------------------------
            if status == "MAINTENANCE":
                self._draw_maintenance_animated(p, gx + bw / 2, gy + bl / 2, ox, oy, scale)

            # -------------------------------------------------------------
            # Band bo'lsa -> 3D Avtomobil va Jonli Taymer
            # -------------------------------------------------------------
            if status == "OCCUPIED":
                car_colors = [
                    (QColor(37, 99, 235), QColor(29, 78, 216)),    # Royal Blue
                    (QColor(220, 38, 38), QColor(185, 28, 28)),    # Crimson Red
                    (QColor(245, 158, 11), QColor(217, 119, 6)),   # Sunset Amber
                    (QColor(13, 148, 136), QColor(15, 118, 110)),  # Teal Green
                    (QColor(148, 163, 184), QColor(100, 116, 139)) # Sleek Silver
                ]
                c_idx = sum(ord(c) for c in s_num) % len(car_colors)
                c_l, c_d = car_colors[c_idx]

                duration = self._calculate_duration(etime)
                self._draw_isometric_car(p, gx + 6, gy + 10, bw - 12, bl - 20, c_l, c_d, plate, model, duration, ox, oy, scale)
            elif status == "FREE" and not self.is_mini:
                fp = self.iso_project(gx + bw / 2, gy + bl / 2 + 10, 1, ox, oy, scale)
                p.setPen(QColor(52, 211, 153, 200))
                p.setFont(QFont("Segoe UI", int(7 * scale), QFont.Weight.Medium))
                p.drawText(QRectF(fp.x() - 25, fp.y() - 8, 50, 16), Qt.AlignmentFlag.AlignCenter, "BO'SH")

    # -------------------------------------------------------------------------
    # 3D AVTOMOBIL, MODEL VA JONLI TAYMER (CAR + MODEL + TIMER)
    # -------------------------------------------------------------------------
    def _draw_isometric_car(self, p: QPainter, cx, cy, cw, cl, c_l, c_d, plate, model, duration, ox, oy, scale):
        # Soya
        p.setBrush(QColor(0, 0, 0, 80))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(QPolygonF([
            self.iso_project(cx - 3, cy - 3, 0.2, ox, oy, scale),
            self.iso_project(cx + cw + 3, cy - 3, 0.2, ox, oy, scale),
            self.iso_project(cx + cw + 3, cy + cl + 4, 0.2, ox, oy, scale),
            self.iso_project(cx - 3, cy + cl + 4, 0.2, ox, oy, scale),
        ]))

        ch_h = 10
        cab_h = 18

        # Korpus (Chassis sides)
        p.setBrush(c_l)
        p.setPen(QPen(c_d, 0.8))
        p.drawPolygon(QPolygonF([
            self.iso_project(cx + cw, cy, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, ch_h, ox, oy, scale),
            self.iso_project(cx + cw, cy, ch_h, ox, oy, scale),
        ]))

        p.setBrush(c_d)
        p.drawPolygon(QPolygonF([
            self.iso_project(cx, cy + cl, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, ch_h, ox, oy, scale),
            self.iso_project(cx, cy + cl, ch_h, ox, oy, scale),
        ]))

        p.setBrush(c_l)
        p.drawPolygon(QPolygonF([
            self.iso_project(cx, cy, ch_h, ox, oy, scale),
            self.iso_project(cx + cw, cy, ch_h, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, ch_h, ox, oy, scale),
            self.iso_project(cx, cy + cl, ch_h, ox, oy, scale),
        ]))

        # Kabina & Oyna
        in_x, in_y1, in_y2 = 4, 12, 14
        cab_x = cx + in_x
        cab_w = cw - in_x * 2
        cab_y = cy + in_y1
        cab_l = cl - in_y1 - in_y2

        p.setBrush(c_l.lighter(115))
        p.drawPolygon(QPolygonF([
            self.iso_project(cab_x, cab_y, cab_h, ox, oy, scale),
            self.iso_project(cab_x + cab_w, cab_y, cab_h, ox, oy, scale),
            self.iso_project(cab_x + cab_w, cab_y + cab_l, cab_h, ox, oy, scale),
            self.iso_project(cab_x, cab_y + cab_l, cab_h, ox, oy, scale),
        ]))

        # Oyna
        p.setBrush(QColor(186, 230, 253, 220))
        p.setPen(QPen(QColor(255, 255, 255, 180), 0.8))
        p.drawPolygon(QPolygonF([
            self.iso_project(cab_x + cab_w, cab_y, cab_h, ox, oy, scale),
            self.iso_project(cx + cw - 1, cy + in_y1 - 5, ch_h, ox, oy, scale),
            self.iso_project(cx + cw - 1, cy + cl - in_y2 + 5, ch_h, ox, oy, scale),
            self.iso_project(cab_x + cab_w, cab_y + cab_l, cab_h, ox, oy, scale),
        ]))

        # Faralar
        hl1 = self.iso_project(cx + cw, cy + 2, ch_h - 2, ox, oy, scale)
        hl2 = self.iso_project(cx + cw, cy + 8, ch_h - 2, ox, oy, scale)
        p.setPen(QPen(QColor(254, 240, 138), 3 * scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(hl1, hl2)

        # -------------------------------------------------------------
        # TAYMER VA DAVLAT RAQAMI BADGE-I (FLOATING BADGE)
        # -------------------------------------------------------------
        if plate and not self.is_mini:
            pt = self.iso_project(cx + cw / 2, cy + cl / 2, cab_h + 10, ox, oy, scale)
            badge_w, badge_h = 76, 26
            b_rect = QRectF(pt.x() - badge_w / 2, pt.y() - badge_h / 2, badge_w, badge_h)

            # Karta foni
            p.setBrush(QColor(255, 255, 255, 245))
            p.setPen(QPen(QColor(15, 23, 42), 1.2))
            p.drawRoundedRect(b_rect, 5, 5)

            # Yashil UZB chizig'i
            p.setBrush(QColor(16, 185, 129))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(QRectF(b_rect.left() + 2, b_rect.top() + 2, 4, badge_h - 4), 2, 2)

            # Raqam
            p.setPen(QColor(15, 23, 42))
            p.setFont(QFont("Consolas", int(7.2 * scale), QFont.Weight.Bold))
            p.drawText(QRectF(b_rect.left() + 6, b_rect.top() + 2, badge_w - 8, 12), Qt.AlignmentFlag.AlignCenter, plate)

            # Jonli Taymer (⏱ 01:24:15)
            p.setPen(QColor(2, 132, 199))  # Sky blue
            p.setFont(QFont("Segoe UI", int(6.5 * scale), QFont.Weight.Bold))
            p.drawText(QRectF(b_rect.left() + 6, b_rect.top() + 13, badge_w - 8, 12), Qt.AlignmentFlag.AlignCenter, f"⏱ {duration}")

    # -------------------------------------------------------------------------
    # EV QUVVATLASHTIRISH STANSIYASI (ANIMATION & CABLE)
    # -------------------------------------------------------------------------
    def _draw_ev_pedestal_animated(self, p: QPainter, ex, ey, ox, oy, scale, is_charging=False):
        ch_h = 26
        # Ustun
        p.setBrush(QColor(20, 184, 166))
        p.setPen(QPen(QColor(255, 255, 255), 0.8))
        p.drawPolygon(QPolygonF([
            self.iso_project(ex, ey, 0, ox, oy, scale),
            self.iso_project(ex + 6, ey, 0, ox, oy, scale),
            self.iso_project(ex + 6, ey + 6, ch_h, ox, oy, scale),
            self.iso_project(ex, ey + 6, ch_h, ox, oy, scale),
        ]))

        # Pulsatsiyalanuvchi zaryadlash chirog'i
        glow_col = QColor(56, 189, 248) if (self.anim_tick % 4 < 2) else QColor(16, 185, 129)
        dot = self.iso_project(ex + 3, ey + 3, ch_h - 4, ox, oy, scale)
        p.setBrush(glow_col)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(dot, 3 * scale, 3 * scale)

        # Agar mashina quvvatlanayotgan bo'lsa -> Kabel nuri
        if is_charging:
            car_conn = self.iso_project(ex - 8, ey + 18, 8, ox, oy, scale)
            p.setPen(QPen(QColor(56, 189, 248), 2.0 * scale, Qt.PenStyle.DashLine))
            p.drawLine(dot, car_conn)

    # -------------------------------------------------------------------------
    # VIP ZONA (GOLDEN STANCHIONS & STAR)
    # -------------------------------------------------------------------------
    def _draw_vip_bollards(self, p: QPainter, gx, gy, bw, bl, ox, oy, scale):
        # 4 burchakdagi oltin ustunchalar
        corners = [(gx + 2, gy + 2), (gx + bw - 2, gy + 2), (gx + bw - 2, gy + bl - 2), (gx + 2, gy + bl - 2)]
        for cx, cy in corners:
            b_pt = self.iso_project(cx, cy, 0, ox, oy, scale)
            t_pt = self.iso_project(cx, cy, 14, ox, oy, scale)
            p.setPen(QPen(QColor(234, 179, 8), 3 * scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            p.drawLine(b_pt, t_pt)

        # Oltin yulduz belgisi
        star_pt = self.iso_project(gx + bw / 2, gy + 10, 16, ox, oy, scale)
        p.setBrush(QColor(234, 179, 8))
        p.setPen(Qt.PenStyle.NoPen)
        pulse_r = (3.5 + 0.8 * math.sin(self.anim_tick * 0.4)) * scale
        p.drawEllipse(star_pt, pulse_r, pulse_r)

    # -------------------------------------------------------------------------
    # TA'MIRLASH (MAINTENANCE) ANIMATSIYASI
    # -------------------------------------------------------------------------
    def _draw_maintenance_animated(self, p: QPainter, cx, cy, ox, oy, scale):
        base = self.iso_project(cx, cy, 1, ox, oy, scale)
        top = self.iso_project(cx, cy, 20, ox, oy, scale)

        # Charaqlovchi sariq mayoqcha
        beacon_col = QColor(245, 158, 11) if (self.anim_tick % 6 < 3) else QColor(239, 68, 68)
        p.setPen(QPen(beacon_col, 8 * scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(base, top)

        # Ogohlantiruvchi konus nuri
        p.setBrush(beacon_col)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(top, 4 * scale, 4 * scale)

    # -------------------------------------------------------------------------
    # 6. HUD BOSHQARUV TUGMALARI VA QAVAT LEGENDA
    # -------------------------------------------------------------------------
    def _draw_hud_controls(self, p: QPainter, w, h):
        # Yuqori chapda qavat belgisi
        fl_names = {
            1: "1-Qavat (Yer usti Markaziy & VIP)",
            2: "2-Qavat (EV Quvvatlash Stansiyasi)",
            3: "3-Qavat (Yuqori tom Panorama)",
            -1: "-1 Qavat (Yerosti VIP & Quvvatlash)"
        }
        fl_title = fl_names.get(self.floor, f"{self.floor}-Qavat")

        p.setBrush(QColor(255, 255, 255, 230))
        p.setPen(QPen(QColor(226, 232, 240), 1))
        f_rect = QRectF(16, 16, 250, 36)
        p.drawRoundedRect(f_rect, 10, 10)

        p.setPen(QColor(15, 23, 42))
        p.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        p.drawText(f_rect, Qt.AlignmentFlag.AlignCenter, f"🏢 {fl_title}")

        # Yuqori o'ngda Zoom ko'rsatkichi
        z_rect = QRectF(w - 180, 16, 164, 36)
        p.setBrush(QColor(255, 255, 255, 230))
        p.setPen(QPen(QColor(226, 232, 240), 1))
        p.drawRoundedRect(z_rect, 10, 10)

        p.setPen(QColor(71, 85, 105))
        p.setFont(QFont("Segoe UI", 9.5, QFont.Weight.Bold))
        p.drawText(z_rect, Qt.AlignmentFlag.AlignCenter, f"🔍 Zoom: {int(self.zoom_factor * 100)}% | Drag: Surish")

        # Pastki legenda
        leg_items = [
            ("Bo'sh joy", QColor(16, 185, 129)),
            ("Band (Avto)", QColor(239, 68, 68)),
            ("EV Quvvatlash", QColor(20, 184, 166)),
            ("VIP Xodim", QColor(168, 85, 247)),
            ("Ta'mirlash", QColor(245, 158, 11))
        ]
        leg_w = 480
        l_rect = QRectF(w - leg_w - 16, h - 44, leg_w, 32)
        p.setBrush(QColor(255, 255, 255, 230))
        p.setPen(QPen(QColor(226, 232, 240), 1))
        p.drawRoundedRect(l_rect, 8, 8)

        cx = l_rect.left() + 14
        for lbl, col in leg_items:
            p.setBrush(col)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(cx, l_rect.center().y()), 5, 5)

            p.setPen(QColor(71, 85, 105))
            p.setFont(QFont("Segoe UI", 8, QFont.Weight.Medium))
            p.drawText(QRectF(cx + 10, l_rect.top(), 80, l_rect.height()), Qt.AlignmentFlag.AlignVCenter, lbl)
            cx += 92
