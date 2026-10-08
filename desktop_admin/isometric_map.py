"""
Parkly.uz — 3D Isometric Parking Map Widget
Haqiqiy 3D Izometrik proyeksiyada avtoturargoh, avtomobillar, shlagbaum va nazorat binosini chizuvchi interaktiv vidjet.
Foydalanuvchi talabi asosida to'liq dinamik va chiroyli dizaynda tayyorlangan.
"""

import math
from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QPolygonF, QLinearGradient, QRadialGradient, QCursor
)
from PyQt6.QtCore import Qt, QPointF, pyqtSignal, QRectF


class IsometricParkingMapWidget(QWidget):
    """
    3D Izometrik Avtoturargoh Chizmasi Vidjeti
    """
    slot_clicked = pyqtSignal(dict)  # Slot bosilganda signali

    def __init__(self, parent=None, is_mini=False):
        super().__init__(parent)
        self.is_mini = is_mini
        self.slots = []
        self.floor = 1
        self.hovered_slot = None
        self.slot_polygons = {}  # slot_number -> QPolygonF (hover/click uchun)

        self.setMouseTracking(True)
        if not is_mini:
            self.setMinimumSize(700, 480)
        else:
            self.setMinimumSize(400, 260)

    def set_slots(self, slots_data, floor=1):
        """Slotlar ma'lumotlarini qabul qilish va qayta chizish"""
        self.slots = [s for s in slots_data if s.get("floor", 1) == floor]
        self.floor = floor
        self.update()

    def set_floor(self, floor):
        self.floor = floor
        self.update()

    # -------------------------------------------------------------------------
    # IZOMETRIK KOORDINATA O'ZGARISHLARI (2:1 ISOMETRIC PROJECTION)
    # -------------------------------------------------------------------------
    def iso_project(self, gx, gy, gz, ox, oy, scale):
        """
        3D dunyo koordinatalarini (gx, gy, gz) 2D ekran nuqtasiga o'tkazish
        gx: o'ng-pastga o'q (+30 gradus)
        gy: chap-pastga o'q (-30 gradus)
        gz: yuqoriga vertikal balandlik (-Y ekran bo'yicha)
        """
        # Standart 2:1 izometrik nisbat
        sx = ox + (gx - gy) * 1.0 * scale
        sy = oy + (gx + gy) * 0.5 * scale - (gz * scale)
        return QPointF(sx, sy)

    def mouseMoveEvent(self, event):
        pos = event.position()
        old_hover = self.hovered_slot
        self.hovered_slot = None

        for slot_num, poly in self.slot_polygons.items():
            if poly.containsPoint(pos, Qt.FillRule.OddEvenFill):
                self.hovered_slot = slot_num
                # Hover qilingan slot ma'lumotini topish
                slot_info = next((s for s in self.slots if s.get("slot_number") == slot_num), None)
                if slot_info and not self.is_mini:
                    st_txt = slot_info.get('status', 'FREE')
                    plate = slot_info.get('current_vehicle_plate') or "Yo'q"
                    tp = slot_info.get('slot_type', 'REGULAR')
                    QToolTip.showText(
                        QCursor.pos(),
                        f"Slot: {slot_num} ({tp})\nHolat: {st_txt}\nAvto: {plate}\nO'zgartirish uchun bosing",
                        self
                    )
                break

        if self.hovered_slot != old_hover:
            self.setCursor(Qt.CursorShape.PointingHandCursor if self.hovered_slot else Qt.CursorShape.ArrowCursor)
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for slot_num, poly in self.slot_polygons.items():
                if poly.containsPoint(pos, Qt.FillRule.OddEvenFill):
                    slot_info = next((s for s in self.slots if s.get("slot_number") == slot_num), None)
                    if slot_info:
                        self.slot_clicked.emit(slot_info)
                    break

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        w = self.width()
        h = self.height()

        # Shaffof zamonaviy fon (Glassmorphism backdrop)
        bg_grad = QLinearGradient(0, 0, w, h)
        bg_grad.setColorAt(0.0, QColor(241, 245, 249, 140))
        bg_grad.setColorAt(1.0, QColor(226, 232, 240, 180))
        painter.fillRect(self.rect(), bg_grad)

        # O'lcham va masshtabni hisoblash
        scale = 0.52 if self.is_mini else 0.85
        ox = w * 0.48
        oy = h * 0.22 if not self.is_mini else h * 0.20

        self.slot_polygons.clear()

        # 1. 3D KO'TARILGAN ASFALT PLATFORMA (RAISED ISOMETRIC SLAB)
        self._draw_platform(painter, ox, oy, scale)

        # 2. NAZORAT POSTI VA SHLAGBAUM (SECURITY BOOTH & BARRIER)
        self._draw_security_booth(painter, ox, oy, scale)

        # 3. YO'L CHIZIQLARI VA KIRISH YO'LI
        self._draw_road_markings(painter, ox, oy, scale)

        # 4. YASHIL MAYDONCHALAR (ISOMETRIC GREEN PLANTERS & TREES)
        self._draw_greenery(painter, ox, oy, scale)

        # 5. PARKOVKA JOY LARI VA 3D AVTOMOBILLAR (PARKING BAYS & 3D CARS)
        self._draw_slots_and_cars(painter, ox, oy, scale)

        # 6. MINI LEGENDA (FAKAT KATTA KO'RINISHDA)
        if not self.is_mini:
            self._draw_overlay_legend(painter, w, h)

    # -------------------------------------------------------------------------
    # 1. PLATFORMA (ASPHALT BASE & CONCRETE SLAB)
    # -------------------------------------------------------------------------
    def _draw_platform(self, p: QPainter, ox, oy, scale):
        # Platforma o'lchamlari
        pw, pl, pz = 520, 360, 20

        # Chap qirra (Front-Left slab edge)
        left_face = QPolygonF([
            self.iso_project(0, pl, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale),
            self.iso_project(pw, pl, -pz, ox, oy, scale),
            self.iso_project(0, pl, -pz, ox, oy, scale),
        ])
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(30, 41, 59))  # Dark slate concrete
        p.drawPolygon(left_face)

        # O'ng qirra (Front-Right slab edge)
        right_face = QPolygonF([
            self.iso_project(pw, 0, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale),
            self.iso_project(pw, pl, -pz, ox, oy, scale),
            self.iso_project(pw, 0, -pz, ox, oy, scale),
        ])
        p.setBrush(QColor(51, 65, 85))  # Medium slate
        p.drawPolygon(right_face)

        # Yuqori tekislik (Asphalt top surface)
        top_face = QPolygonF([
            self.iso_project(0, 0, 0, ox, oy, scale),
            self.iso_project(pw, 0, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale),
            self.iso_project(0, pl, 0, ox, oy, scale),
        ])
        asphalt_grad = QLinearGradient(
            self.iso_project(0, 0, 0, ox, oy, scale),
            self.iso_project(pw, pl, 0, ox, oy, scale)
        )
        asphalt_grad.setColorAt(0.0, QColor(30, 41, 59))   # #1e293b
        asphalt_grad.setColorAt(1.0, QColor(15, 23, 42))   # #0f172a
        p.setBrush(asphalt_grad)
        p.setPen(QPen(QColor(100, 116, 139), 1.5))
        p.drawPolygon(top_face)

    # -------------------------------------------------------------------------
    # 2. NAZORAT POSTI VA SHLAGBAUM (SECURITY BOOTH & BOOM BARRIER)
    # -------------------------------------------------------------------------
    def _draw_security_booth(self, p: QPainter, ox, oy, scale):
        bx, by = 20, 20
        bw, bl, bh = 60, 60, 45

        # Bino poydevor soyasi
        shadow = QPolygonF([
            self.iso_project(bx + 5, by + 5, 0, ox, oy, scale),
            self.iso_project(bx + bw + 15, by + 5, 0, ox, oy, scale),
            self.iso_project(bx + bw + 15, by + bl + 15, 0, ox, oy, scale),
            self.iso_project(bx + 5, by + bl + 15, 0, ox, oy, scale),
        ])
        p.setBrush(QColor(0, 0, 0, 70))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(shadow)

        # Bino old devori (Facing Right/South-East)
        front_wall = QPolygonF([
            self.iso_project(bx + bw, by, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, bh, ox, oy, scale),
            self.iso_project(bx + bw, by, bh, ox, oy, scale),
        ])
        p.setBrush(QColor(249, 115, 22))  # Orange modern booth (#f97316)
        p.setPen(QPen(QColor(194, 65, 12), 1))
        p.drawPolygon(front_wall)

        # Oyna (Front Window)
        win_front = QPolygonF([
            self.iso_project(bx + bw + 1, by + 12, 15, ox, oy, scale),
            self.iso_project(bx + bw + 1, by + bl - 12, 15, ox, oy, scale),
            self.iso_project(bx + bw + 1, by + bl - 12, 35, ox, oy, scale),
            self.iso_project(bx + bw + 1, by + 12, 35, ox, oy, scale),
        ])
        p.setBrush(QColor(186, 230, 253, 230))  # Light sky cyan glass
        p.setPen(QPen(QColor(255, 255, 255), 1))
        p.drawPolygon(win_front)

        # Bino chap devori (Facing Left/South-West)
        left_wall = QPolygonF([
            self.iso_project(bx, by + bl, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, 0, ox, oy, scale),
            self.iso_project(bx + bw, by + bl, bh, ox, oy, scale),
            self.iso_project(bx, by + bl, bh, ox, oy, scale),
        ])
        p.setBrush(QColor(234, 88, 12))  # Darker orange
        p.drawPolygon(left_wall)

        # Tom (Roof slab with overhang)
        roof = QPolygonF([
            self.iso_project(bx - 4, by - 4, bh + 4, ox, oy, scale),
            self.iso_project(bx + bw + 4, by - 4, bh + 4, ox, oy, scale),
            self.iso_project(bx + bw + 4, by + bl + 4, bh + 4, ox, oy, scale),
            self.iso_project(bx - 4, by + bl + 4, bh + 4, ox, oy, scale),
        ])
        p.setBrush(QColor(248, 250, 252))  # White sleek roof
        p.setPen(QPen(QColor(203, 213, 225), 1))
        p.drawPolygon(roof)

        # ----------------- SHLAGBAUM (BOOM BARRIER) -----------------
        bar_x, bar_y = bx + bw + 10, by + bl - 5
        # Post ustuni (Orange post)
        post = QPolygonF([
            self.iso_project(bar_x, bar_y, 0, ox, oy, scale),
            self.iso_project(bar_x + 8, bar_y, 0, ox, oy, scale),
            self.iso_project(bar_x + 8, bar_y + 8, 24, ox, oy, scale),
            self.iso_project(bar_x, bar_y + 8, 24, ox, oy, scale),
        ])
        p.setBrush(QColor(245, 158, 11))  # Amber/Yellow pillar
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(post)

        # To'siq to'sini (Barrier arm striped)
        arm_p1 = self.iso_project(bar_x + 4, bar_y + 4, 18, ox, oy, scale)
        arm_p2 = self.iso_project(bar_x + 4, bar_y + 65, 18, ox, oy, scale)
        arm_pen = QPen(QColor(239, 68, 68), max(3.0, 4.0 * scale))
        arm_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(arm_pen)
        p.drawLine(arm_p1, arm_p2)

        # Oq chiziqlar (white stripes on barrier arm)
        arm_dash_pen = QPen(QColor(255, 255, 255), max(3.0, 4.0 * scale))
        arm_dash_pen.setStyle(Qt.PenStyle.DotLine)
        p.setPen(arm_dash_pen)
        p.drawLine(arm_p1, arm_p2)

    # -------------------------------------------------------------------------
    # 3. YO'L CHIZIQLARI VA KIRISH BELGILARI
    # -------------------------------------------------------------------------
    def _draw_road_markings(self, p: QPainter, ox, oy, scale):
        p.setPen(QPen(QColor(241, 245, 249, 160), 2 * scale, Qt.PenStyle.DashLine))

        # Markaziy harakatlanish chizig'i
        m1 = self.iso_project(140, 180, 0, ox, oy, scale)
        m2 = self.iso_project(480, 180, 0, ox, oy, scale)
        p.drawLine(m1, m2)

        # Kirish yo'li (Entry lane from left)
        e1 = self.iso_project(20, 110, 0, ox, oy, scale)
        e2 = self.iso_project(140, 110, 0, ox, oy, scale)
        p.drawLine(e1, e2)

        # STOP belgisi (Qizil doira yoki to'rtburchak kirishda)
        if not self.is_mini:
            stop_poly = QPolygonF([
                self.iso_project(45, 95, 0.5, ox, oy, scale),
                self.iso_project(75, 95, 0.5, ox, oy, scale),
                self.iso_project(75, 125, 0.5, ox, oy, scale),
                self.iso_project(45, 125, 0.5, ox, oy, scale),
            ])
            p.setBrush(QColor(239, 68, 68, 220))
            p.setPen(QPen(QColor(255, 255, 255), 1.5))
            p.drawPolygon(stop_poly)

            p.setPen(QColor(255, 255, 255))
            p.setFont(QFont("Segoe UI", int(7 * scale), QFont.Weight.Bold))
            sp = self.iso_project(60, 110, 1, ox, oy, scale)
            p.drawText(QRectF(sp.x() - 20, sp.y() - 10, 40, 20), Qt.AlignmentFlag.AlignCenter, "STOP")

    # -------------------------------------------------------------------------
    # 4. YASHIL MAYDONCHALAR VA BUTALAR (GREENERY)
    # -------------------------------------------------------------------------
    def _draw_greenery(self, p: QPainter, ox, oy, scale):
        # Kirish yonidagi maysazor orolchasi
        planters = [
            (20, 150, 40, 60),
            (20, 230, 40, 60)
        ]
        for gx, gy, gw, gl in planters:
            # Curb
            curb = QPolygonF([
                self.iso_project(gx, gy, 4, ox, oy, scale),
                self.iso_project(gx + gw, gy, 4, ox, oy, scale),
                self.iso_project(gx + gw, gy + gl, 4, ox, oy, scale),
                self.iso_project(gx, gy + gl, 4, ox, oy, scale),
            ])
            p.setBrush(QColor(34, 197, 94))  # Emerald grass
            p.setPen(QPen(QColor(203, 213, 225), 1.5))
            p.drawPolygon(curb)

            # Markazidagi manzarali konus daraxt (Cypress tree)
            tx, ty = gx + gw / 2, gy + gl / 2
            tree_base = self.iso_project(tx, ty, 4, ox, oy, scale)
            tree_top = self.iso_project(tx, ty, 28, ox, oy, scale)
            p.setPen(QPen(QColor(22, 101, 52), 6 * scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            p.drawLine(tree_base, tree_top)

    # -------------------------------------------------------------------------
    # 5. PARKOVKA JOY LARI VA 3D AVTOMOBILLAR (SLOTS & 3D CARS)
    # -------------------------------------------------------------------------
    def _draw_slots_and_cars(self, p: QPainter, ox, oy, scale):
        """
        Slotlar joylashuvi:
        1-Qator (Yuqori): A-101 .. A-106 (yoki B-201 .. B-206)
        2-Qator (Pastki): EV-01 .. EV-03, VIP-01 .. VIP-03
        """
        # Standart slot o'lchamlari
        bw = 50   # Kenglik (gx)
        bl = 75   # Uzunlik (gy)

        # 1-Qavat slot konfiguratsiyasi
        slot_coords = {
            # Yuqori qator (A-Zona)
            "A-101": (160, 30),
            "A-102": (220, 30),
            "A-103": (280, 30),
            "A-104": (340, 30),
            "A-105": (400, 30),
            "A-106": (460, 30),
            # Pastki qator (EV & VIP Zona)
            "EV-01": (160, 240),
            "EV-02": (220, 240),
            "EV-03": (280, 240),
            "VIP-01": (340, 240),
            "VIP-02": (400, 240),
            "VIP-03": (460, 240),

            # 2-Qavat uchun moslashuv
            "B-201": (160, 30),
            "B-202": (220, 30),
            "B-203": (280, 30),
            "B-204": (340, 30),
            "B-205": (400, 30),
            "B-206": (460, 30),
            "EV-21": (160, 240),
            "EV-22": (220, 240),
        }

        # Agar slot xaritada topilmasa dinamik joylashtirish
        curr_gx, curr_gy = 160, 30
        for slot in self.slots:
            s_num = slot.get("slot_number", "A-101")
            status = slot.get("status", "FREE")
            s_type = slot.get("slot_type", "REGULAR")
            plate = slot.get("current_vehicle_plate")

            if s_num in slot_coords:
                gx, gy = slot_coords[s_num]
            else:
                gx, gy = curr_gx, curr_gy
                curr_gx += 60

            # Slot asosi (Ground Bay polygon)
            p1 = self.iso_project(gx, gy, 0.5, ox, oy, scale)
            p2 = self.iso_project(gx + bw, gy, 0.5, ox, oy, scale)
            p3 = self.iso_project(gx + bw, gy + bl, 0.5, ox, oy, scale)
            p4 = self.iso_project(gx, gy + bl, 0.5, ox, oy, scale)
            bay_poly = QPolygonF([p1, p2, p3, p4])
            self.slot_polygons[s_num] = bay_poly

            is_hover = (self.hovered_slot == s_num)

            # Slot chizig'i va fon rangi
            if status == "OCCUPIED":
                bay_bg = QColor(30, 41, 59, 200)
                line_color = QColor(239, 68, 68) if not is_hover else QColor(248, 113, 113)
            elif status == "RESERVED":
                bay_bg = QColor(245, 158, 11, 40)
                line_color = QColor(245, 158, 11)
            elif s_type == "EV_CHARGING":
                bay_bg = QColor(13, 148, 136, 45)
                line_color = QColor(20, 184, 166)
            elif s_type == "VIP_STAFF":
                bay_bg = QColor(168, 85, 247, 45)
                line_color = QColor(192, 132, 252)
            else:  # FREE
                bay_bg = QColor(16, 185, 129, 30)
                line_color = QColor(16, 185, 129)

            if is_hover:
                bay_bg = QColor(56, 189, 248, 90)  # Bright cyan glow on hover

            p.setBrush(bay_bg)
            pen_w = 2.5 * scale if is_hover else 1.5 * scale
            p.setPen(QPen(line_color, pen_w, Qt.PenStyle.SolidLine))
            p.drawPolygon(bay_poly)

            # Slot raqami yozuvi
            center_pt = self.iso_project(gx + bw / 2, gy + 15, 1, ox, oy, scale)
            p.setPen(QColor(226, 232, 240) if status != "FREE" else QColor(16, 185, 129))
            font_size = max(7, int(9 * scale))
            p.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
            p.drawText(QRectF(center_pt.x() - 30, center_pt.y() - 10, 60, 20), Qt.AlignmentFlag.AlignCenter, s_num)

            # EV zaryadlash ustuni (EV Charging Pedestal)
            if s_type == "EV_CHARGING":
                self._draw_ev_charger(p, gx + bw - 8, gy + 6, ox, oy, scale)

            # Agar slot BAND bo'lsa -> 3D AVTOMOBIL CHIZISH
            if status == "OCCUPIED":
                # Mashina rangi (har xil ranglar)
                car_colors = [
                    (QColor(37, 99, 235), QColor(29, 78, 216)),    # Royal Blue
                    (QColor(220, 38, 38), QColor(185, 28, 28)),    # Crimson Red
                    (QColor(245, 158, 11), QColor(217, 119, 6)),   # Sunset Amber
                    (QColor(13, 148, 136), QColor(15, 118, 110)),  # Teal Green
                    (QColor(148, 163, 184), QColor(100, 116, 139)) # Sleek Silver
                ]
                # Slot raqamiga qarab rang tanlash
                c_idx = sum(ord(c) for c in s_num) % len(car_colors)
                c_light, c_dark = car_colors[c_idx]

                self._draw_isometric_car(p, gx + 6, gy + 10, bw - 12, bl - 20, c_light, c_dark, plate, ox, oy, scale)
            elif status == "RESERVED":
                # Bron qilingan konus belgisi
                self._draw_reserved_cone(p, gx + bw / 2, gy + bl / 2, ox, oy, scale)
            elif status == "FREE" and not self.is_mini:
                # "BO'SH" yozuvi
                fp = self.iso_project(gx + bw / 2, gy + bl / 2 + 10, 1, ox, oy, scale)
                p.setPen(QColor(52, 211, 153, 200))
                p.setFont(QFont("Segoe UI", int(7 * scale), QFont.Weight.Medium))
                p.drawText(QRectF(fp.x() - 25, fp.y() - 8, 50, 16), Qt.AlignmentFlag.AlignCenter, "BO'SH")

    # -------------------------------------------------------------------------
    # 3D IZOMETRIK AVTOMOBIL CHIZISH (HIGH-QUALITY 3D ISOMETRIC CAR)
    # -------------------------------------------------------------------------
    def _draw_isometric_car(self, p: QPainter, cx, cy, cw, cl, c_light, c_dark, plate, ox, oy, scale):
        """
        Haqiqiy 3D Izometrik Avtomobil:
        Soya, g'ildiraklar, korpus (lower chassis), kabina, old/orqa oynalar, faralar va floating UZB davlat raqami.
        """
        # 1. Mashina ostidagi yumshoq soya
        car_shadow = QPolygonF([
            self.iso_project(cx - 3, cy - 3, 0.2, ox, oy, scale),
            self.iso_project(cx + cw + 3, cy - 3, 0.2, ox, oy, scale),
            self.iso_project(cx + cw + 3, cy + cl + 4, 0.2, ox, oy, scale),
            self.iso_project(cx - 3, cy + cl + 4, 0.2, ox, oy, scale),
        ])
        p.setBrush(QColor(0, 0, 0, 80))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(car_shadow)

        chassis_h = 10  # Korpus balandligi
        cabin_h = 18    # Tom balandligi

        # 2. Mashina korpusi pastki qismi (Chassis Sides)
        # Old qirra (Facing Front/South-East)
        front_side = QPolygonF([
            self.iso_project(cx + cw, cy, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, chassis_h, ox, oy, scale),
            self.iso_project(cx + cw, cy, chassis_h, ox, oy, scale),
        ])
        p.setBrush(c_light)
        p.setPen(QPen(c_dark, 0.8))
        p.drawPolygon(front_side)

        # Chap qirra (Facing Left/South-West)
        left_side = QPolygonF([
            self.iso_project(cx, cy + cl, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, 3, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, chassis_h, ox, oy, scale),
            self.iso_project(cx, cy + cl, chassis_h, ox, oy, scale),
        ])
        p.setBrush(c_dark)
        p.drawPolygon(left_side)

        # Korpus ustki yuzasi (Hood and Trunk deck)
        hood = QPolygonF([
            self.iso_project(cx, cy, chassis_h, ox, oy, scale),
            self.iso_project(cx + cw, cy, chassis_h, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl, chassis_h, ox, oy, scale),
            self.iso_project(cx, cy + cl, chassis_h, ox, oy, scale),
        ])
        p.setBrush(c_light)
        p.drawPolygon(hood)

        # 3. Mashina kabinasi (Cabin & Roof)
        in_x = 4
        in_y1 = 12
        in_y2 = 14
        cab_x = cx + in_x
        cab_w = cw - in_x * 2
        cab_y = cy + in_y1
        cab_l = cl - in_y1 - in_y2

        # Tom (Roof)
        roof = QPolygonF([
            self.iso_project(cab_x, cab_y, cabin_h, ox, oy, scale),
            self.iso_project(cab_x + cab_w, cab_y, cabin_h, ox, oy, scale),
            self.iso_project(cab_x + cab_w, cab_y + cab_l, cabin_h, ox, oy, scale),
            self.iso_project(cab_x, cab_y + cab_l, cabin_h, ox, oy, scale),
        ])
        p.setBrush(c_light.lighter(115))
        p.drawPolygon(roof)

        # Old oyna (Windshield facing South-East)
        windshield = QPolygonF([
            self.iso_project(cab_x + cab_w, cab_y, cabin_h, ox, oy, scale),
            self.iso_project(cx + cw - 1, cy + in_y1 - 5, chassis_h, ox, oy, scale),
            self.iso_project(cx + cw - 1, cy + cl - in_y2 + 5, chassis_h, ox, oy, scale),
            self.iso_project(cab_x + cab_w, cab_y + cab_l, cabin_h, ox, oy, scale),
        ])
        p.setBrush(QColor(186, 230, 253, 220))  # Tinted cyan glass
        p.setPen(QPen(QColor(255, 255, 255, 180), 0.8))
        p.drawPolygon(windshield)

        # Yon oyna (Side glass facing South-West)
        side_glass = QPolygonF([
            self.iso_project(cab_x, cab_y + cab_l, cabin_h, ox, oy, scale),
            self.iso_project(cab_x + cab_w, cab_y + cab_l, cabin_h, ox, oy, scale),
            self.iso_project(cx + cw, cy + cl - in_y2 + 2, chassis_h, ox, oy, scale),
            self.iso_project(cx, cy + cl - in_y2 + 2, chassis_h, ox, oy, scale),
        ])
        p.setBrush(QColor(125, 211, 252, 220))
        p.drawPolygon(side_glass)

        # Faralar (Headlights - Yellow glowing)
        hl1 = self.iso_project(cx + cw, cy + 2, chassis_h - 2, ox, oy, scale)
        hl2 = self.iso_project(cx + cw, cy + 8, chassis_h - 2, ox, oy, scale)
        p.setPen(QPen(QColor(254, 240, 138), 3 * scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(hl1, hl2)

        # 4. Mashina ustidagi davlat raqami (Floating License Plate Pill)
        if plate and not self.is_mini:
            plate_pt = self.iso_project(cx + cw / 2, cy + cl / 2, cabin_h + 8, ox, oy, scale)
            pw_tag, ph_tag = 64, 18
            plate_rect = QRectF(plate_pt.x() - pw_tag / 2, plate_pt.y() - ph_tag / 2, pw_tag, ph_tag)

            p.setBrush(QColor(255, 255, 255, 240))
            p.setPen(QPen(QColor(15, 23, 42), 1.2))
            p.drawRoundedRect(plate_rect, 4, 4)

            # Yashil UZB chizig'i
            p.setBrush(QColor(16, 185, 129))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(QRectF(plate_rect.left() + 2, plate_rect.top() + 2, 4, ph_tag - 4), 2, 2)

            # Raqam matni
            p.setPen(QColor(15, 23, 42))
            p.setFont(QFont("Consolas", int(7.5 * scale), QFont.Weight.Bold))
            p.drawText(plate_rect, Qt.AlignmentFlag.AlignCenter, plate)

    # -------------------------------------------------------------------------
    # EV ZARYADLASH USTUNI (EV CHARGING PEDESTAL)
    # -------------------------------------------------------------------------
    def _draw_ev_charger(self, p: QPainter, ex, ey, ox, oy, scale):
        ch_h = 24
        # Ustun korpusi
        col = QPolygonF([
            self.iso_project(ex, ey, 0, ox, oy, scale),
            self.iso_project(ex + 6, ey, 0, ox, oy, scale),
            self.iso_project(ex + 6, ey + 6, ch_h, ox, oy, scale),
            self.iso_project(ex, ey + 6, ch_h, ox, oy, scale),
        ])
        p.setBrush(QColor(20, 184, 166))  # Teal charger pillar
        p.setPen(QPen(QColor(255, 255, 255), 0.8))
        p.drawPolygon(col)

        # LED quvvatlash nuri (Cyan dot)
        dot = self.iso_project(ex + 3, ey + 3, ch_h - 4, ox, oy, scale)
        p.setBrush(QColor(56, 189, 248))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(dot, 2.5 * scale, 2.5 * scale)

    # -------------------------------------------------------------------------
    # BRON BELGISI (PARKING CONE)
    # -------------------------------------------------------------------------
    def _draw_reserved_cone(self, p: QPainter, cx, cy, ox, oy, scale):
        cone_base = self.iso_project(cx, cy, 1, ox, oy, scale)
        cone_tip = self.iso_project(cx, cy, 18, ox, oy, scale)
        p.setPen(QPen(QColor(245, 158, 11), 7 * scale, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(cone_base, cone_tip)

    # -------------------------------------------------------------------------
    # 6. LEGENDA OVERLAY (FLOATING GLASSMORPHISM STATUS PILLS)
    # -------------------------------------------------------------------------
    def _draw_overlay_legend(self, p: QPainter, w, h):
        # Yuqori chapda qavat belgisi
        p.setBrush(QColor(255, 255, 255, 210))
        p.setPen(QPen(QColor(226, 232, 240), 1))
        floor_rect = QRectF(16, 16, 180, 36)
        p.drawRoundedRect(floor_rect, 10, 10)

        p.setPen(QColor(15, 23, 42))
        p.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        fl_str = f"🏢 {self.floor}-Qavat (3D Izometrik)"
        p.drawText(floor_rect, Qt.AlignmentFlag.AlignCenter, fl_str)

        # Pastki o'ngda ranglar izohi
        items = [
            ("Bo'sh joy", QColor(16, 185, 129)),
            ("Band (Avto)", QColor(239, 68, 68)),
            ("Bron qilingan", QColor(245, 158, 11)),
            ("EV Zaryadlash", QColor(20, 184, 166)),
            ("VIP Xodim", QColor(168, 85, 247))
        ]

        leg_w = 460
        leg_rect = QRectF(w - leg_w - 16, h - 44, leg_w, 32)
        p.setBrush(QColor(255, 255, 255, 220))
        p.setPen(QPen(QColor(226, 232, 240), 1))
        p.drawRoundedRect(leg_rect, 8, 8)

        cur_x = leg_rect.left() + 14
        for lbl, col in items:
            p.setBrush(col)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(cur_x, leg_rect.center().y()), 5, 5)

            p.setPen(QColor(71, 85, 105))
            p.setFont(QFont("Segoe UI", 8, QFont.Weight.Medium))
            p.drawText(QRectF(cur_x + 10, leg_rect.top(), 80, leg_rect.height()), Qt.AlignmentFlag.AlignVCenter, lbl)
            cur_x += 90
