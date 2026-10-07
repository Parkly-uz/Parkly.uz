"""
Parkly.uz — Desktop Admin Panel Runner (PyQt6 / Python)
Foydalanuvchi yuklagan 3 ta dizayn andozasi asosida to'liq yaratilgan:
- Image 3: Ikki qismli split zamonaviy Login oynasi (Teal branding + Oq login forma)
- Image 1 & 2: Ultra-modern yengil mavzu (Floating chap navigatsiya, Yuqori pill tabs,
  Xush kelibsiz kartochkasi, Balans va bandlik ko'rsatkichlari, 2D interaktiv xarita,
  So'nggi harakatlar va Sozlamalar).
"""

import sys
import random
from datetime import datetime

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
        QGridLayout, QFrame, QLabel, QPushButton, QLineEdit, QComboBox,
        QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget,
        QButtonGroup, QMessageBox, QGroupBox
    )
    from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QLinearGradient
    from PyQt6.QtCore import Qt, QRect
except ImportError:
    print("PyQt6 kutubxonasi o'rnatilmoqda...")
    sys.exit(1)


# ==============================================================================
# 1. LOGIN OYNASI (Image 3 dizayni asosida)
# ==============================================================================
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parkly.uz — Tizimga Kirish")
        self.setFixedSize(760, 480)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.user_role = ""
        self.user_fullname = ""
        self.username = ""
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Chap qism (Teal branding & info)
        left_frame = QFrame(self)
        left_frame.setFixedWidth(320)
        left_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f766e, stop:1 #115e59);
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
                color: white;
            }
        """)
        l_layout = QVBoxLayout(left_frame)
        l_layout.setContentsMargins(35, 40, 35, 40)

        import os
        from PyQt6.QtGui import QPixmap
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

        pix = QPixmap(logo_path)
        if not pix.isNull():
            logo_widget = QLabel(left_frame)
            logo_widget.setPixmap(pix.scaledToWidth(240, Qt.TransformationMode.SmoothTransformation))
            logo_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            logo_widget = QLabel("🚗 <b>Parkly.uz</b>", left_frame)
            logo_widget.setStyleSheet("font-size: 26px; color: #ffffff;")
            logo_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_layout.addWidget(logo_widget)

        sub_lbl = QLabel("Aqlli Avtoturargoh Boshqaruv Tizimi", left_frame)
        sub_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #ccfbf1; margin-top: 15px;")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_layout.addWidget(sub_lbl)

        desc = QLabel(
            "• Real-time ANPR kamera oqimi\n"
            "• 2D interaktiv slotlar xaritasi\n"
            "• Avtomatlashgan to'lov va shlagbaum\n"
            "• Super-Admin va 5 ta operator nazorati", left_frame
        )
        desc.setStyleSheet("font-size: 11px; color: #99f6e4; line-height: 1.5; margin-top: 15px;")
        l_layout.addWidget(desc)
        l_layout.addStretch()

        footer = QLabel("© 2026 Parkly Ekotizimi v1.0", left_frame)
        footer.setStyleSheet("font-size: 10px; color: #5eead4;")
        l_layout.addWidget(footer)

        # O'ng qism (Oq Login formasi)
        right_frame = QFrame(self)
        right_frame.setStyleSheet("background-color: #ffffff; border-top-right-radius: 12px; border-bottom-right-radius: 12px;")
        r_layout = QVBoxLayout(right_frame)
        r_layout.setContentsMargins(45, 45, 45, 45)
        r_layout.setSpacing(12)

        title = QLabel("PARKLY ADMIN", right_frame)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0d9488;")

        sub = QLabel("Tizimga kirish (Foydalanuvchi hisobi)", right_frame)
        sub.setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 8px;")

        u_lbl = QLabel("Foydalanuvchi nomi yoki Email:", right_frame)
        u_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #334155;")
        self.user_edit = QLineEdit(right_frame)
        self.user_edit.setText("admin")
        self.user_edit.setStyleSheet("border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px; font-size: 13px;")

        p_lbl = QLabel("Maxfiy parol:", right_frame)
        p_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #334155;")
        self.pass_edit = QLineEdit(right_frame)
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setText("admin123")
        self.pass_edit.setStyleSheet("border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px; font-size: 13px;")

        self.remember_box = QCheckBox("Meni tizimda eslab qol", right_frame)
        self.remember_box.setChecked(True)
        self.remember_box.setStyleSheet("font-size: 12px; color: #64748b;")

        self.error_lbl = QLabel("", right_frame)
        self.error_lbl.setStyleSheet("color: #ef4444; font-size: 12px; font-weight: bold;")

        btn = QPushButton("Tizimga Kirish", right_frame)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #0d9488;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
                border: none;
            }
            QPushButton:hover { background-color: #0f766e; }
        """)
        btn.clicked.connect(self.handle_login)

        hint = QLabel("🔑 Sinov: Super-Admin: <b>admin</b> / <b>admin123</b> | Operator: <b>operator1</b> / <b>operator123</b>", right_frame)
        hint.setStyleSheet("font-size: 10px; color: #94a3b8;")
        hint.setWordWrap(True)

        r_layout.addWidget(title)
        r_layout.addWidget(sub)
        r_layout.addWidget(u_lbl)
        r_layout.addWidget(self.user_edit)
        r_layout.addWidget(p_lbl)
        r_layout.addWidget(self.pass_edit)
        r_layout.addWidget(self.remember_box)
        r_layout.addWidget(self.error_lbl)
        r_layout.addWidget(btn)
        r_layout.addWidget(hint)
        r_layout.addStretch()

        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame)

    def handle_login(self):
        u = self.user_edit.text().strip()
        p = self.pass_edit.text().strip()

        if u == "admin" and p == "admin123":
            self.username = "erjigitvv5"
            self.user_fullname = "Erjigit (Bosh Rahbar)"
            self.user_role = "SUPER_ADMIN"
            self.accept()
        elif u == "manager" and p == "manager123":
            self.username = "sherzod_ali"
            self.user_fullname = "Sherzod Aliyev (Filial Admini)"
            self.user_role = "ADMIN"
            self.accept()
        elif (u.startswith("operator") or u == "op") and p == "operator123":
            self.username = "aziz_rustamov"
            self.user_fullname = "Aziz Rustamov (Smena 1)"
            self.user_role = "OPERATOR"
            self.accept()
        else:
            self.error_lbl.setText("❌ Noto'g'ri login yoki parol kiritildi!")


# ==============================================================================
# 2. 2D INTERAKTIV XARITA WIDGETI
# ==============================================================================
class Parking2DMapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(700, 430)
        self.slots = [
            {"num": "A-101", "type": "REGULAR", "status": "FREE", "plate": "", "x": 50, "y": 50},
            {"num": "A-102", "type": "REGULAR", "status": "OCCUPIED", "plate": "01 A 777 AA", "x": 150, "y": 50},
            {"num": "A-103", "type": "REGULAR", "status": "FREE", "plate": "", "x": 250, "y": 50},
            {"num": "A-104", "type": "REGULAR", "status": "RESERVED", "plate": "", "x": 350, "y": 50},
            {"num": "A-105", "type": "REGULAR", "status": "PAYMENT_PENDING", "plate": "10 123 BBA", "x": 450, "y": 50},
            {"num": "A-106", "type": "REGULAR", "status": "MAINTENANCE", "plate": "", "x": 550, "y": 50},

            {"num": "EV-01", "type": "EV_CHARGING", "status": "FREE", "plate": "", "x": 50, "y": 240},
            {"num": "EV-02", "type": "EV_CHARGING", "status": "OCCUPIED", "plate": "01 888 ZZZ", "x": 150, "y": 240},
            {"num": "EV-03", "type": "EV_CHARGING", "status": "FREE", "plate": "", "x": 250, "y": 240},

            {"num": "VIP-01", "type": "VIP_STAFF", "status": "FREE", "plate": "", "x": 350, "y": 240},
            {"num": "VIP-02", "type": "VIP_STAFF", "status": "OCCUPIED", "plate": "01 001 PPP", "x": 450, "y": 240},
            {"num": "VIP-03", "type": "VIP_STAFF", "status": "RESERVED", "plate": "", "x": 550, "y": 240},
        ]
        self.selected_slot = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(26, 28, 35))

        # Yo'l chiziqlari
        road_pen = QPen(QColor(60, 64, 75), 2, Qt.PenStyle.DashLine)
        painter.setPen(road_pen)
        painter.drawLine(30, 200, self.width() - 30, 200)
        painter.drawLine(30, 390, self.width() - 30, 390)

        # Zonalarning sarlavhasi
        painter.setPen(QColor(180, 190, 205))
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        painter.drawText(50, 35, "ZONA A — STANDART YENGIL AVTO")
        painter.drawText(50, 225, "ZONA EV — ELEKTROMOBILLAR (CHARGING)")
        painter.drawText(350, 225, "ZONA VIP & XODIMLAR")

        color_map = {
            "FREE": QColor(46, 204, 113),
            "OCCUPIED": QColor(231, 76, 60),
            "RESERVED": QColor(241, 196, 15),
            "PAYMENT_PENDING": QColor(230, 126, 34),
            "MAINTENANCE": QColor(149, 165, 166)
        }

        for s in self.slots:
            rect = QRect(s["x"], s["y"], 80, 140)
            c = color_map.get(s["status"], QColor(100, 100, 100))

            painter.setBrush(c)
            painter.setPen(QPen(Qt.GlobalColor.white if self.selected_slot == s["num"] else QColor(30, 30, 30), 2))
            painter.drawRoundedRect(rect, 6, 6)

            # Slot raqami
            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            painter.drawText(rect.adjusted(0, 8, 0, 0), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter, s["num"])

            # Holat matni
            painter.setFont(QFont("Segoe UI", 7, QFont.Weight.DemiBold))
            painter.drawText(rect.adjusted(0, 0, 0, -8), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, s["status"])

            # Mashina raqami
            if s["plate"]:
                pb = QRect(rect.x() + 5, rect.y() + 45, rect.width() - 10, 24)
                painter.setBrush(Qt.GlobalColor.white)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawRoundedRect(pb, 3, 3)
                painter.setFont(QFont("Segoe UI", 7))
                painter.drawText(pb, Qt.AlignmentFlag.AlignCenter, s["plate"])

    def mousePressEvent(self, event):
        for s in self.slots:
            rect = QRect(s["x"], s["y"], 80, 140)
            if rect.contains(event.pos()):
                self.selected_slot = s["num"]
                self.update()
                if hasattr(self.parent(), "on_slot_selected_callback"):
                    self.parent().on_slot_selected_callback(s)
                return


# ==============================================================================
# 3. ASOSIY DASHBOARD OYNASI (Image 1 & 2 dizayni asosida)
# ==============================================================================
class MainDashboard(QMainWindow):
    def __init__(self, username, fullname, role):
        super().__init__()
        self.username = username
        self.fullname = fullname
        self.role = role

        self.setWindowTitle("Parkly.uz — Aqlli Avtoturargoh Boshqaruv Paneli")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 680)

        self.setup_ui()
        self.apply_role_permissions()

    def setup_ui(self):
        central = QWidget(self)
        central.setStyleSheet("background-color: #f1f5f9; font-family: 'Segoe UI', Arial, sans-serif;")
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        # 1. Chap vertikal floating bar
        sidebar = self.create_sidebar()
        root_layout.addWidget(sidebar)

        # 2. O'ng asosiy qism
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        header = self.create_header()
        content_layout.addWidget(header)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.create_dashboard_view())  # 0
        self.stack.addWidget(self.create_map_view())        # 1
        self.stack.addWidget(self.create_camera_view())     # 2
        self.stack.addWidget(self.create_staff_view())      # 3
        self.stack.addWidget(self.create_finance_view())    # 4
        self.stack.addWidget(self.create_settings_view())   # 5

        content_layout.addWidget(self.stack, 1)
        root_layout.addLayout(content_layout, 1)
        self.setCentralWidget(central)

    def create_sidebar(self):
        bar = QFrame(self)
        bar.setFixedWidth(72)
        bar.setStyleSheet("""
            QFrame { background-color: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; }
            QPushButton { background-color: transparent; border: none; border-radius: 14px; font-size: 20px; color: #64748b; }
            QPushButton:hover { background-color: #f1f5f9; color: #0f766e; }
            QPushButton:checked { background-color: #0d9488; color: #ffffff; }
        """)
        layout = QVBoxLayout(bar)
        layout.setContentsMargins(8, 18, 8, 18)
        layout.setSpacing(14)

        logo = QLabel("🚗", bar)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 26px; margin-bottom: 12px;")
        layout.addWidget(logo)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        items = [
            (0, "📊", "Bosh Sahifa"),
            (1, "🗺️", "2D Xarita"),
            (2, "📹", "Kameralar"),
            (3, "👥", "Xodimlar"),
            (4, "💳", "Moliya"),
            (5, "⚙️", "Sozlamalar")
        ]
        for idx, icon, tip in items:
            btn = QPushButton(icon, bar)
            btn.setCheckable(True)
            btn.setToolTip(tip)
            btn.setFixedSize(54, 46)
            self.nav_group.addButton(btn, idx)
            layout.addWidget(btn)
            if idx == 0:
                btn.setChecked(True)

        layout.addStretch()

        logout_btn = QPushButton("🚪", bar)
        logout_btn.setToolTip("Chiqish")
        logout_btn.setFixedSize(54, 46)
        logout_btn.setStyleSheet("color: #ef4444;")
        logout_btn.clicked.connect(self.close)
        layout.addWidget(logout_btn)

        self.nav_group.idClicked.connect(self.switch_tab)
        return bar

    def create_header(self):
        hdr = QFrame(self)
        hdr.setFixedHeight(68)
        hdr.setStyleSheet("QFrame { background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; }")
        l = QHBoxLayout(hdr)
        l.setContentsMargins(20, 10, 20, 10)
        l.setSpacing(14)

        import os
        from PyQt6.QtGui import QPixmap
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

        brand_logo = QLabel(hdr)
        pix = QPixmap(logo_path)
        if not pix.isNull():
            brand_logo.setPixmap(pix.scaledToHeight(38, Qt.TransformationMode.SmoothTransformation))
        else:
            brand_logo.setText("<b>Parkly.uz</b>")
            brand_logo.setStyleSheet("font-size: 18px; color: #0d9488;")
        l.addWidget(brand_logo)

        pills = QHBoxLayout()
        pills.setSpacing(6)
        self.pill_group = QButtonGroup(self)

        pill_names = ["Asosiy", "2D Xarita", "Kameralar", "Xodimlar", "Moliya", "Sozlamalar"]
        for idx, name in enumerate(pill_names):
            btn = QPushButton(name, hdr)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f8fafc; color: #475569; font-size: 12px; font-weight: 600;
                    padding: 7px 16px; border-radius: 16px; border: 1px solid #e2e8f0;
                }
                QPushButton:hover { background-color: #e2e8f0; }
                QPushButton:checked { background-color: #0f172a; color: #ffffff; border: 1px solid #0f172a; }
            """)
            self.pill_group.addButton(btn, idx)
            pills.addWidget(btn)
            if idx == 0:
                btn.setChecked(True)

        self.pill_group.idClicked.connect(self.switch_tab)
        l.addLayout(pills)
        l.addStretch()

        # Profil
        prof = QLabel(f"👤 <b>{self.fullname}</b> ({self.role})", hdr)
        prof.setStyleSheet("background-color: #f0fdfa; color: #0d9488; border: 1px solid #ccfbf1; padding: 6px 14px; border-radius: 16px; font-size: 12px;")
        l.addWidget(prof)
        return hdr

    def create_dashboard_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(14)

        # Banner (Image 1/2)
        banner = QFrame(page)
        banner.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 14px;")
        b_layout = QHBoxLayout(banner)
        tl = QVBoxLayout()
        t1 = QLabel(f"Xayrli kun, {self.fullname} 👋", banner)
        t1.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;")
        t2 = QLabel("Parkly.uz — avtoturargoh holati, tushumlar va xodimlar nazorati.", banner)
        t2.setStyleSheet("font-size: 13px; color: #64748b;")
        tl.addWidget(t1)
        tl.addWidget(t2)
        b_layout.addLayout(tl)
        b_layout.addStretch()

        dt = QLabel(datetime.now().strftime("%d-%B, %Y"), banner)
        dt.setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 8px 16px; font-weight: 600; color: #334155;")
        b_layout.addWidget(dt)
        l.addWidget(banner)

        # Ko'rsatkichlar kartalari
        grid = QGridLayout()
        grid.setSpacing(14)

        card_rev = QFrame(page)
        card_rev.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f766e, stop:1 #115e59);
                border-radius: 18px; color: white; padding: 16px;
            }
        """)
        rl = QVBoxLayout(card_rev)
        rl.addWidget(QLabel("Bugungi Jami Tushum", card_rev))
        rl.addWidget(QLabel("4,850,000 UZS", card_rev))
        rl.addWidget(QLabel("↑ +14.2% o'tgan haftaga nisbatan (Bandlik: 68%)", card_rev))
        grid.addWidget(card_rev, 0, 0, 1, 2)

        def make_stat(title, val, badge, b_color, v_color):
            card = QFrame()
            card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 14px;")
            cl = QVBoxLayout(card)
            th = QHBoxLayout()
            th.addWidget(QLabel(title))
            th.addStretch()
            bl = QLabel(badge)
            bl.setStyleSheet(f"background-color: {b_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;")
            th.addWidget(bl)
            cl.addLayout(th)
            vl = QLabel(val)
            vl.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {v_color}; margin-top: 4px;")
            cl.addWidget(vl)
            return card

        grid.addWidget(make_stat("Bo'sh Joylar", "48 ta", "Erkin", "#10b981", "#10b981"), 0, 2)
        grid.addWidget(make_stat("Band Joylar", "92 ta", "Band", "#ef4444", "#ef4444"), 0, 3)
        grid.addWidget(make_stat("Faol Bronlar", "14 ta", "Rezerv", "#f59e0b", "#f59e0b"), 0, 4)
        l.addLayout(grid)

        # So'nggi harakatlar
        t_card = QFrame(page)
        t_card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        tl = QVBoxLayout(t_card)
        tl.addWidget(QLabel("<b>So'nggi Kirish-Chiqish va To'lov Harakatlari</b>", t_card))

        tbl = QTableWidget(0, 6, t_card)
        tbl.setHorizontalHeaderLabels(["Seans ID", "Avtomobil Raqami", "Slot", "Kirish Vaqti", "Summa", "Holat"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setStyleSheet("border: none; font-size: 12px;")

        rows = [
            ("SES-1049", "01 A 777 AA", "A-102", "14:22:10", "15,000 UZS", "✅ To'langan (Payme)"),
            ("SES-1048", "10 123 BBA", "A-105", "14:18:05", "10,000 UZS", "⏳ To'lov kutilmoqda"),
            ("SES-1047", "01 888 ZZZ", "EV-02", "14:05:40", "35,000 UZS", "⚡ Zaryadlanmoqda"),
            ("SES-1046", "01 001 PPP", "VIP-02", "13:40:12", "0 UZS", "⭐ VIP Xodim"),
        ]
        for r_idx, r in enumerate(rows):
            tbl.insertRow(r_idx)
            for c_idx, val in enumerate(r):
                tbl.setItem(r_idx, c_idx, QTableWidgetItem(val))

        tl.addWidget(tbl)
        l.addWidget(t_card, 1)
        return page

    def create_map_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)

        card = QFrame(page)
        card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        cl = QVBoxLayout(card)

        th = QHBoxLayout()
        th.addWidget(QLabel("<b>Qavatni tanlang:</b>"))
        combo = QComboBox()
        combo.addItems(["1-Qavat (Markaziy)", "2-Qavat (Yuqori)"])
        th.addWidget(combo)
        self.slot_info = QLabel("Tanlangan slot: [Katak ustiga bosing]")
        self.slot_info.setStyleSheet("color: #0d9488; font-weight: bold; padding-left: 15px;")
        th.addWidget(self.slot_info)
        th.addStretch()
        cl.addLayout(th)

        self.map_widget = Parking2DMapWidget(card)
        card.on_slot_selected_callback = self.on_slot_selected
        cl.addWidget(self.map_widget, 1)

        l.addWidget(card)
        return page

    def on_slot_selected(self, slot):
        p = slot["plate"] if slot["plate"] else "Yo'q"
        self.slot_info.setText(f"Tanlangan: <b>{slot['num']}</b> | Turi: <b>{slot['type']}</b> | Holat: <b>{slot['status']}</b> | Mashina: <b>{p}</b>")

    def create_camera_view(self):
        page = QWidget()
        l = QHBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(14)

        # Video
        v_card = QFrame(page)
        v_card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        vl = QVBoxLayout(v_card)
        vl.addWidget(QLabel("<b>📷 Jonli Kirish Kameralari & ANPR (10 FPS)</b>"))
        cam = QLabel("ANPR Kamera Oqimi Faol\n[RTSP / Web-Kamera / Adaptive CLAHE]", v_card)
        cam.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cam.setStyleSheet("background-color: #0f172a; color: #2dd4bf; font-size: 15px; border-radius: 12px; min-height: 380px; font-weight: bold;")
        vl.addWidget(cam, 1)

        btn = QPushButton("🚗 Yangi Mashina Kirishini Simulyatsiya Qilish", v_card)
        btn.setStyleSheet("background-color: #0d9488; color: white; padding: 10px; border-radius: 10px; font-weight: bold;")
        btn.clicked.connect(self.sim_detection)
        vl.addWidget(btn)
        l.addWidget(v_card, 1)

        # Log
        l_card = QFrame(page)
        l_card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        ll = QVBoxLayout(l_card)
        ll.addWidget(QLabel("<b>So'nggi O'qilgan Raqamlar (Konsensus)</b>"))
        self.anpr_tbl = QTableWidget(0, 4, l_card)
        self.anpr_tbl.setHorizontalHeaderLabels(["Vaqt", "Davlat Raqami", "Aniqlik", "Holat"])
        self.anpr_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.anpr_tbl.setStyleSheet("border: none; font-size: 12px;")
        ll.addWidget(self.anpr_tbl)
        l.addWidget(l_card, 1)
        return page

    def sim_detection(self):
        r = self.anpr_tbl.rowCount()
        self.anpr_tbl.insertRow(0)
        p = f"01 A {random.randint(100, 999)} AA"
        self.anpr_tbl.setItem(0, 0, QTableWidgetItem(datetime.now().strftime("%H:%M:%S")))
        self.anpr_tbl.setItem(0, 1, QTableWidgetItem(p))
        self.anpr_tbl.setItem(0, 2, QTableWidgetItem("98.5%"))
        self.anpr_tbl.setItem(0, 3, QTableWidgetItem("KIRISH GA RUXSAT"))

    def create_staff_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        card = QFrame(page)
        card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("<b>Xodimlar va Ruxsatlar Boshqaruvi (Super-Admin, Adminlar, 5 Operator)</b>"))

        tbl = QTableWidget(0, 5, card)
        tbl.setHorizontalHeaderLabels(["ID", "Login", "F.I.SH", "Roli", "Smenasi"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setStyleSheet("border: none; font-size: 12px;")

        staff = [
            ("1", "super_admin", "Erjigit (Bosh Rahbar)", "SUPER_ADMIN", "Hammasi"),
            ("2", "admin_toshkent", "Sherzod Aliyev", "ADMIN", "Filial 1"),
            ("3", "admin_chilonzor", "Jahongir Qodirov", "ADMIN", "Filial 2"),
            ("4", "op_smena_1", "Aziz Rustamov", "OPERATOR", "Smena 1 (08:00 - 16:00)"),
            ("5", "op_smena_2", "Bobur Mirzayev", "OPERATOR", "Smena 2 (16:00 - 00:00)"),
            ("6", "op_smena_3", "Dilshod Karimov", "OPERATOR", "Smena 3 (00:00 - 08:00)"),
            ("7", "op_zaxira_1", "Farrux Yusupov", "OPERATOR", "Zaxira 1"),
            ("8", "op_zaxira_2", "G'ayrat Xoliqov", "OPERATOR", "Zaxira 2"),
        ]
        for idx, s in enumerate(staff):
            tbl.insertRow(idx)
            for c, v in enumerate(s):
                tbl.setItem(idx, c, QTableWidgetItem(v))

        cl.addWidget(tbl)
        l.addWidget(card)
        return page

    def create_finance_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        card = QFrame(page)
        card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("<b>💳 Moliya, Kassa va To'lovlar Tahlili</b>"))

        grid = QGridLayout()
        def fin_box(n, a, c):
            box = QFrame()
            box.setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 14px;")
            bl = QVBoxLayout(box)
            bl.addWidget(QLabel(n))
            val = QLabel(a)
            val.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {c};")
            bl.addWidget(val)
            return box

        grid.addWidget(fin_box("Payme To'lovlari", "2,450,000 UZS", "#0ea5e9"), 0, 0)
        grid.addWidget(fin_box("Click To'lovlari", "1,650,000 UZS", "#8b5cf6"), 0, 1)
        grid.addWidget(fin_box("Naqd / Terminal Kassa", "750,000 UZS", "#f59e0b"), 0, 2)
        cl.addLayout(grid)

        tbl = QTableWidget(0, 5, card)
        tbl.setHorizontalHeaderLabels(["Tranzaksiya ID", "To'lovchi", "Provayder", "Summa", "Fiskal Chek"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setStyleSheet("border: none; font-size: 12px; margin-top: 10px;")

        txs = [
            ("PAY-9921", "01 A 777 AA", "Payme", "15,000 UZS", "FISC-88214"),
            ("CLK-8812", "10 123 BBA", "Click", "10,000 UZS", "FISC-88213"),
            ("PAY-9920", "01 888 ZZZ", "Payme", "35,000 UZS", "FISC-88212"),
        ]
        for idx, t in enumerate(txs):
            tbl.insertRow(idx)
            for c, v in enumerate(t):
                tbl.setItem(idx, c, QTableWidgetItem(v))

        cl.addWidget(tbl, 1)
        l.addWidget(card)
        return page

    def create_settings_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)

        card = QFrame(page)
        card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 20px;")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("<b>⚙️ Parkovka Tizimi va Tarif Sozlamalari</b>"))

        grid = QGridLayout()
        grid.addWidget(QLabel("Kunduzgi soatlik stavka (08:00 - 20:00):"), 0, 0)
        grid.addWidget(QLineEdit("5000 UZS"), 0, 1)

        grid.addWidget(QLabel("Tungi soatlik stavka (20:00 - 08:00):"), 1, 0)
        grid.addWidget(QLineEdit("3000 UZS"), 1, 1)

        grid.addWidget(QLabel("Dastlabki bepul oraliq (Grace Period):"), 2, 0)
        grid.addWidget(QLineEdit("15 daqiqa"), 2, 1)

        grid.addWidget(QLabel("To'lovdan so'ng chiqish oralig'i:"), 3, 0)
        grid.addWidget(QLineEdit("15 daqiqa"), 3, 1)

        grid.addWidget(QLabel("Kunlik maksimal to'lov (Daily Cap):"), 4, 0)
        grid.addWidget(QLineEdit("50000 UZS"), 4, 1)

        cl.addLayout(grid)

        save_btn = QPushButton("💾 Sozlamalarni Saqlash", card)
        save_btn.setStyleSheet("background-color: #0d9488; color: white; padding: 10px 24px; border-radius: 10px; font-weight: bold; margin-top: 15px;")
        save_btn.clicked.connect(lambda: QMessageBox.information(self, "Sozlamalar", "✅ Barcha sozlamalar muvaffaqiyatli saqlandi!"))
        cl.addWidget(save_btn, 0, Qt.AlignmentFlag.AlignLeft)
        cl.addStretch()

        l.addWidget(card)
        return page

    def switch_tab(self, idx):
        self.stack.setCurrentIndex(idx)
        if self.nav_group.button(idx):
            self.nav_group.button(idx).setChecked(True)
        if self.pill_group.button(idx):
            self.pill_group.button(idx).setChecked(True)

    def apply_role_permissions(self):
        if self.role == "OPERATOR":
            for i in [3, 4, 5]:
                if self.nav_group.button(i):
                    self.nav_group.button(i).setEnabled(False)
                if self.pill_group.button(i):
                    self.pill_group.button(i).setEnabled(False)


def main():
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Accepted:
        win = MainDashboard(login.username, login.user_fullname, login.user_role)
        win.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
