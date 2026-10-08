"""
Parkly.uz — Desktop Admin Panel (PyQt6 / Real Database Engine)
100% Dinamik, Real SQLite/PostgreSQL bazasi bilan ishlaydi.
Barcha emojilar haqiqiy zamonaviy SVG vektor piktogrammalari (Icons) bilan almashtirilgan.
Dizayn: Foydalanuvchi yuborgan andoza (Modern Card Layout, Left Sidebar, Top Navigation, 2D Xarita).
"""

import sys
import os
import random
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QLabel, QPushButton, QLineEdit, QComboBox,
    QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget,
    QButtonGroup, QMessageBox, QGroupBox, QSpinBox
)
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QLinearGradient, QPixmap, QIcon
from PyQt6.QtCore import Qt, QRect, QSize

from db_manager import ParklyDatabase

# Ikonkalar va aktivlar yo'li
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")


def get_icon(name: str) -> QIcon:
    """SVG ikonkani xavfsiz yuklab beruvchi yordamchi funksiya"""
    path = os.path.join(ICONS_DIR, name)
    if os.path.exists(path):
        return QIcon(path)
    return QIcon()


# ==============================================================================
# 1. TIZIMGA KIRISH OYNASI (Login Dialog — Haqiqiy DB bilan)
# ==============================================================================
class LoginDialog(QDialog):
    def __init__(self, db: ParklyDatabase, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Parkly.uz — Tizimga Kirish")
        self.setFixedSize(760, 480)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.user_data = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Chap qism (Teal brending va rasmiy logotip)
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

        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        pix = QPixmap(logo_path)
        logo_widget = QLabel(left_frame)
        if not pix.isNull():
            logo_widget.setPixmap(pix.scaledToWidth(240, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_widget.setText("PARKLY.UZ")
            logo_widget.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
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
        desc.setStyleSheet("font-size: 11px; color: #99f6e4; line-height: 1.6; margin-top: 15px;")
        l_layout.addWidget(desc)
        l_layout.addStretch()

        footer = QLabel("© 2026 Parkly Ekotizimi v1.0", left_frame)
        footer.setStyleSheet("font-size: 10px; color: #5eead4;")
        l_layout.addWidget(footer)

        # O'ng qism (Oq Login formasi)
        right_frame = QFrame(self)
        right_frame.setStyleSheet("background-color: #ffffff; border-top-right-radius: 12px; border-bottom-right-radius: 12px;")
        r_layout = QVBoxLayout(right_frame)
        r_layout.setContentsMargins(45, 40, 45, 40)
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
        btn.setIcon(get_icon("lock.svg"))
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

        hint = QLabel("Sinov: Super-Admin: <b>admin</b> / <b>admin123</b> | Operator: <b>operator1</b> / <b>operator123</b>", right_frame)
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

        user = self.db.authenticate(u, p)
        if user:
            self.user_data = user
            self.accept()
        else:
            self.error_lbl.setText("Xatolik: Noto'g'ri login yoki parol kiritildi!")


# ==============================================================================
# 2. 2D INTERAKTIV PARKONKA XARITASI (Slotni tahrirlash dialogi bilan)
# ==============================================================================
class SlotEditDialog(QDialog):
    """Slot ustiga bosilganda uning holatini o'zgartiruvchi dinamik dialog"""
    def __init__(self, slot_data, parent=None):
        super().__init__(parent)
        self.slot_data = slot_data
        self.setWindowTitle(f"Slot boshqaruvi: {slot_data['slot_number']}")
        self.setFixedSize(380, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(f"<b>Slot raqami: {self.slot_data['slot_number']}</b> ({self.slot_data['slot_type']})")
        title.setStyleSheet("font-size: 15px; color: #0d9488;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Holatini tanlang:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["FREE", "OCCUPIED", "RESERVED", "PAYMENT_PENDING", "MAINTENANCE"])
        self.status_combo.setCurrentText(self.slot_data["status"])
        layout.addWidget(self.status_combo)

        layout.addWidget(QLabel("Avtomobil davlat raqami:"))
        self.plate_edit = QLineEdit()
        self.plate_edit.setText(self.slot_data["current_vehicle_plate"] or "")
        self.plate_edit.setPlaceholderText("Masalan: 01 A 777 AA")
        layout.addWidget(self.plate_edit)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Saqlash")
        save_btn.setIcon(get_icon("save.svg"))
        save_btn.setStyleSheet("background-color: #0d9488; color: white; padding: 8px 16px; border-radius: 6px; font-weight: bold;")
        save_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Bekor qilish")
        cancel_btn.clicked.connect(self.reject)

        btn_box.addWidget(save_btn)
        btn_box.addWidget(cancel_btn)
        layout.addLayout(btn_box)

    def get_data(self):
        return {
            "status": self.status_combo.currentText(),
            "plate": self.plate_edit.text().strip() or None
        }


class Parking2DMapWidget(QWidget):
    def __init__(self, db: ParklyDatabase, parent=None):
        super().__init__(parent)
        self.db = db
        self.setMinimumSize(700, 430)
        self.current_floor = 1
        self.slots = []
        self.selected_slot = None
        self.reload_slots()

    def set_floor(self, floor):
        self.current_floor = floor
        self.reload_slots()

    def reload_slots(self):
        self.slots = self.db.get_slots(self.current_floor)
        self.update()

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
        painter.drawText(50, 35, f"ZONA A / {self.current_floor}-QAVAT (STANDART)")
        painter.drawText(50, 225, "ZONA EV — ELEKTROMOBILLAR (CHARGING)")
        painter.drawText(350, 225, "ZONA VIP & XODIMLAR")

        color_map = {
            "FREE": QColor(16, 185, 129),           # Yashil
            "OCCUPIED": QColor(239, 68, 68),        # Qizil
            "RESERVED": QColor(245, 158, 11),       # Sariq
            "PAYMENT_PENDING": QColor(234, 88, 12), # To'q sariq
            "MAINTENANCE": QColor(100, 116, 139)    # Kulrang
        }

        for s in self.slots:
            rect = QRect(s["pos_x"], s["pos_y"], s["width"], s["height"])
            c = color_map.get(s["status"], QColor(100, 100, 100))

            painter.setBrush(c)
            painter.setPen(QPen(Qt.GlobalColor.white if self.selected_slot == s["slot_number"] else QColor(30, 30, 30), 2))
            painter.drawRoundedRect(rect, 6, 6)

            # Slot raqami
            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            painter.drawText(rect.adjusted(0, 8, 0, 0), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter, s["slot_number"])

            # Holat matni
            painter.setFont(QFont("Segoe UI", 7, QFont.Weight.DemiBold))
            painter.drawText(rect.adjusted(0, 0, 0, -8), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, s["status"])

            # Mashina raqami
            plate = s["current_vehicle_plate"]
            if plate:
                pb = QRect(rect.x() + 5, rect.y() + 45, rect.width() - 10, 24)
                painter.setBrush(Qt.GlobalColor.white)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawRoundedRect(pb, 3, 3)
                painter.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
                painter.drawText(pb, Qt.AlignmentFlag.AlignCenter, plate)

    def mousePressEvent(self, event):
        for s in self.slots:
            rect = QRect(s["pos_x"], s["pos_y"], s["width"], s["height"])
            if rect.contains(event.pos()):
                self.selected_slot = s["slot_number"]
                self.update()

                # Tahrirlash oynasini ochish
                dlg = SlotEditDialog(s, self)
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    data = dlg.get_data()
                    self.db.update_slot_status(s["slot_number"], data["status"], data["plate"])
                    self.reload_slots()
                    # Ota oynani yangilash
                    main_win = self.window()
                    if hasattr(main_win, "refresh_all_data"):
                        main_win.refresh_all_data()
                return


# ==============================================================================
# 3. ASOSIY DASHBOARD (100% Dinamik, Ikonkalar bilan)
# ==============================================================================
class MainDashboard(QMainWindow):
    def __init__(self, db: ParklyDatabase, user_data: dict):
        super().__init__()
        self.db = db
        self.user_data = user_data

        self.setWindowTitle("Parkly.uz — Aqlli Avtoturargoh Boshqaruv Paneli")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 680)

        self.setup_ui()
        self.apply_role_permissions()
        self.refresh_all_data()

    def setup_ui(self):
        central = QWidget(self)
        central.setStyleSheet("background-color: #f1f5f9; font-family: 'Segoe UI', Arial, sans-serif;")
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        # 1. Chap vertikal floating bar (Haqiqiy vektor ikonkalar bilan)
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
            QPushButton { background-color: transparent; border: none; border-radius: 14px; padding: 10px; }
            QPushButton:hover { background-color: #f1f5f9; }
            QPushButton:checked { background-color: #0d9488; }
        """)
        layout = QVBoxLayout(bar)
        layout.setContentsMargins(8, 18, 8, 18)
        layout.setSpacing(14)

        icon_path = os.path.join(ASSETS_DIR, "icon.png")
        pix = QPixmap(icon_path)
        logo_icon = QLabel(bar)
        if not pix.isNull():
            logo_icon.setPixmap(pix.scaledToWidth(40, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_icon.setText("P")
            logo_icon.setStyleSheet("font-size: 20px; font-weight: bold; color: #0d9488;")
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_icon)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        items = [
            (0, "dashboard.svg", "Bosh Sahifa"),
            (1, "map.svg", "2D Xarita"),
            (2, "camera.svg", "Kameralar"),
            (3, "users.svg", "Xodimlar"),
            (4, "wallet.svg", "Moliya"),
            (5, "settings.svg", "Sozlamalar")
        ]
        for idx, icon_name, tip in items:
            btn = QPushButton(bar)
            btn.setIcon(get_icon(icon_name))
            btn.setIconSize(QSize(22, 22))
            btn.setCheckable(True)
            btn.setToolTip(tip)
            btn.setFixedSize(54, 46)
            self.nav_group.addButton(btn, idx)
            layout.addWidget(btn)
            if idx == 0:
                btn.setChecked(True)

        layout.addStretch()

        logout_btn = QPushButton(bar)
        logout_btn.setIcon(get_icon("logout.svg"))
        logout_btn.setIconSize(QSize(22, 22))
        logout_btn.setToolTip("Chiqish")
        logout_btn.setFixedSize(54, 46)
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

        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        pix = QPixmap(logo_path)
        brand_logo = QLabel(hdr)
        if not pix.isNull():
            brand_logo.setPixmap(pix.scaledToHeight(38, Qt.TransformationMode.SmoothTransformation))
        else:
            brand_logo.setText("PARKLY.UZ")
            brand_logo.setStyleSheet("font-size: 18px; color: #0d9488; font-weight: bold;")
        l.addWidget(brand_logo)

        pills = QHBoxLayout()
        pills.setSpacing(6)
        self.pill_group = QButtonGroup(self)

        pill_configs = [
            (0, "dashboard.svg", "Asosiy"),
            (1, "map.svg", "2D Xarita"),
            (2, "camera.svg", "Kameralar"),
            (3, "users.svg", "Xodimlar"),
            (4, "wallet.svg", "Moliya"),
            (5, "settings.svg", "Sozlamalar")
        ]
        for idx, icon_name, name in pill_configs:
            btn = QPushButton(name, hdr)
            btn.setIcon(get_icon(icon_name))
            btn.setIconSize(QSize(16, 16))
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

        # Profil badge
        prof = QLabel(f" {self.user_data['full_name']} ({self.user_data['role']})", hdr)
        prof.setStyleSheet("background-color: #f0fdfa; color: #0d9488; border: 1px solid #ccfbf1; padding: 6px 14px; border-radius: 16px; font-size: 12px; font-weight: 600;")
        l.addWidget(prof)
        return hdr

    def create_dashboard_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(14)

        # Xush kelibsiz banneri
        banner = QFrame(page)
        banner.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 14px;")
        b_layout = QHBoxLayout(banner)
        tl = QVBoxLayout()
        t1 = QLabel(f"Xayrli kun, {self.user_data['full_name']}!", banner)
        t1.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;")
        t2 = QLabel("Parkly.uz — avtoturargoh real-vaqt holati va moliya nazorati.", banner)
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
        self.dash_rev_label = QLabel("0 UZS", card_rev)
        self.dash_rev_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #ffffff; margin-top: 4px;")
        rl.addWidget(self.dash_rev_label)
        rl.addWidget(QLabel("Real tranzaksiyalar asosida dinamik hisoblandi", card_rev))
        grid.addWidget(card_rev, 0, 0, 1, 2)

        def make_stat(title, badge, b_color, v_color):
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
            vl = QLabel("0")
            vl.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {v_color}; margin-top: 4px;")
            cl.addWidget(vl)
            return card, vl

        card_free, self.dash_free_label = make_stat("Bo'sh Joylar", "Erkin", "#10b981", "#10b981")
        card_occ, self.dash_occ_label = make_stat("Band Joylar", "Band", "#ef4444", "#ef4444")
        card_res, self.dash_res_label = make_stat("Faol Bronlar", "Rezerv", "#f59e0b", "#f59e0b")

        grid.addWidget(card_free, 0, 2)
        grid.addWidget(card_occ, 0, 3)
        grid.addWidget(card_res, 0, 4)
        l.addLayout(grid)

        # So'nggi harakatlar
        t_card = QFrame(page)
        t_card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        tl = QVBoxLayout(t_card)

        th = QHBoxLayout()
        th.addWidget(QLabel("<b>So'nggi Kirish-Chiqish va To'lov Harakatlari (Baza)</b>"))
        th.addStretch()
        refresh_btn = QPushButton("Yangilash")
        refresh_btn.setIcon(get_icon("refresh.svg"))
        refresh_btn.clicked.connect(self.refresh_all_data)
        th.addWidget(refresh_btn)
        tl.addLayout(th)

        self.dash_table = QTableWidget(0, 6, t_card)
        self.dash_table.setHorizontalHeaderLabels(["Seans ID", "Avtomobil Raqami", "Slot", "Kirish Vaqti", "Summa", "Holat"])
        self.dash_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.dash_table.setStyleSheet("border: none; font-size: 12px;")
        tl.addWidget(self.dash_table)

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
        combo.currentIndexChanged.connect(lambda idx: self.map_widget.set_floor(idx + 1))
        th.addWidget(combo)

        tip = QLabel("Katak ustiga bosib uning holatini o'zgartirishingiz mumkin.")
        tip.setStyleSheet("color: #0d9488; font-weight: bold; padding-left: 15px;")
        th.addWidget(tip)
        th.addStretch()
        cl.addLayout(th)

        self.map_widget = Parking2DMapWidget(self.db, card)
        cl.addWidget(self.map_widget, 1)

        l.addWidget(card)
        return page

    def create_camera_view(self):
        page = QWidget()
        l = QHBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(14)

        # Video
        v_card = QFrame(page)
        v_card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        vl = QVBoxLayout(v_card)
        vl.addWidget(QLabel("<b>Jonli Kirish Kameralari & ANPR (10 FPS)</b>"))
        cam = QLabel("ANPR Kamera Oqimi Faol\n[RTSP / Web-Kamera / Adaptive Low-Light]", v_card)
        cam.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cam.setStyleSheet("background-color: #0f172a; color: #2dd4bf; font-size: 15px; border-radius: 12px; min-height: 380px; font-weight: bold;")
        vl.addWidget(cam, 1)

        btn = QPushButton("Yangi Mashina Kirishini Simulyatsiya Qilish (DB ga yozish)")
        btn.setIcon(get_icon("car.svg"))
        btn.setStyleSheet("background-color: #0d9488; color: white; padding: 12px; border-radius: 10px; font-weight: bold;")
        btn.clicked.connect(self.sim_detection)
        vl.addWidget(btn)
        l.addWidget(v_card, 1)

        # Log
        l_card = QFrame(page)
        l_card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        ll = QVBoxLayout(l_card)
        ll.addWidget(QLabel("<b>So'nggi O'qilgan Raqamlar (Konsensus)</b>"))
        self.anpr_tbl = QTableWidget(0, 4, l_card)
        self.anpr_tbl.setHorizontalHeaderLabels(["Vaqt", "Davlat Raqami", "Biriktirilgan Slot", "Holat"])
        self.anpr_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.anpr_tbl.setStyleSheet("border: none; font-size: 12px;")
        ll.addWidget(self.anpr_tbl)
        l.addWidget(l_card, 1)
        return page

    def sim_detection(self):
        res = self.db.simulate_car_entry()
        if not res:
            QMessageBox.warning(self, "Parkovka To'la", "Kechirasiz, parkovkada birorta ham bo'sh joy qolmagan!")
            return

        r = self.anpr_tbl.rowCount()
        self.anpr_tbl.insertRow(0)
        self.anpr_tbl.setItem(0, 0, QTableWidgetItem(res["time"]))
        self.anpr_tbl.setItem(0, 1, QTableWidgetItem(res["plate"]))
        self.anpr_tbl.setItem(0, 2, QTableWidgetItem(res["slot"]))
        self.anpr_tbl.setItem(0, 3, QTableWidgetItem("KIRISH GA RUXSAT"))

        self.refresh_all_data()
        QMessageBox.information(self, "Mashina Kirdi", f"Avto: {res['plate']} | Ajratilgan joy: {res['slot']}\nBazaga yozildi!")

    def create_staff_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(14)

        card = QFrame(page)
        card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("<b>Xodimlar va Ruxsatlar Boshqaruvi (Haqiqiy Baza)</b>"))

        self.staff_tbl = QTableWidget(0, 5, card)
        self.staff_tbl.setHorizontalHeaderLabels(["ID", "Login", "F.I.SH", "Roli", "Smenasi"])
        self.staff_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.staff_tbl.setStyleSheet("border: none; font-size: 12px;")
        cl.addWidget(self.staff_tbl, 1)

        # Yangi xodim qo'shish formasi
        box = QGroupBox("Yangi Xodim Qo'shish")
        bl = QHBoxLayout(box)

        self.new_user_edit = QLineEdit()
        self.new_user_edit.setPlaceholderText("Login")
        self.new_name_edit = QLineEdit()
        self.new_name_edit.setPlaceholderText("To'liq Ism")
        self.new_pass_edit = QLineEdit()
        self.new_pass_edit.setPlaceholderText("Parol")

        self.new_role_combo = QComboBox()
        self.new_role_combo.addItems(["OPERATOR", "ADMIN"])

        self.new_shift_combo = QComboBox()
        self.new_shift_combo.addItems(["Smena 1 (08:00 - 16:00)", "Smena 2 (16:00 - 00:00)", "Smena 3 (00:00 - 08:00)", "Zaxira"])

        add_btn = QPushButton("Xodimni Saqlash")
        add_btn.setIcon(get_icon("plus.svg"))
        add_btn.setStyleSheet("background-color: #0d9488; color: white; padding: 8px 16px; border-radius: 8px; font-weight: bold;")
        add_btn.clicked.connect(self.on_add_staff)

        bl.addWidget(self.new_user_edit)
        bl.addWidget(self.new_name_edit)
        bl.addWidget(self.new_pass_edit)
        bl.addWidget(self.new_role_combo)
        bl.addWidget(self.new_shift_combo)
        bl.addWidget(add_btn)

        cl.addWidget(box)
        l.addWidget(card)
        return page

    def on_add_staff(self):
        u = self.new_user_edit.text().strip()
        n = self.new_name_edit.text().strip()
        p = self.new_pass_edit.text().strip() or "123456"
        r = self.new_role_combo.currentText()
        s = self.new_shift_combo.currentText()

        if not u or not n:
            QMessageBox.warning(self, "Diqqat", "Iltimos, login va ismni kiriting!")
            return

        ok = self.db.add_staff(u, p, n, r, s)
        if ok:
            self.new_user_edit.clear()
            self.new_name_edit.clear()
            self.new_pass_edit.clear()
            self.refresh_all_data()
            QMessageBox.information(self, "Muvaffaqiyat", "Yangi xodim bazaga saqlandi!")
        else:
            QMessageBox.warning(self, "Xatolik", "Bu loginli foydalanuvchi allaqachon mavjud!")

    def create_finance_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(14)

        card = QFrame(page)
        card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("<b>Moliya, Kassa va To'lovlar Tahlili (Bazadan)</b>"))

        grid = QGridLayout()
        def fin_box(n, color):
            box = QFrame()
            box.setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 14px;")
            bl = QVBoxLayout(box)
            bl.addWidget(QLabel(n))
            val = QLabel("0 UZS")
            val.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color};")
            bl.addWidget(val)
            return box, val

        box_p, self.payme_val_lbl = fin_box("Payme To'lovlari", "#0ea5e9")
        box_c, self.click_val_lbl = fin_box("Click To'lovlari", "#8b5cf6")
        box_n, self.cash_val_lbl = fin_box("Naqd / Terminal Kassa", "#f59e0b")

        grid.addWidget(box_p, 0, 0)
        grid.addWidget(box_c, 0, 1)
        grid.addWidget(box_n, 0, 2)
        cl.addLayout(grid)

        self.tx_tbl = QTableWidget(0, 5, card)
        self.tx_tbl.setHorizontalHeaderLabels(["Tranzaksiya ID", "To'lovchi", "Provayder", "Summa", "Fiskal Chek"])
        self.tx_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tx_tbl.setStyleSheet("border: none; font-size: 12px; margin-top: 10px;")
        cl.addWidget(self.tx_tbl, 1)

        l.addWidget(card)
        return page

    def create_settings_view(self):
        page = QWidget()
        l = QVBoxLayout(page)
        l.setContentsMargins(0, 0, 0, 0)

        card = QFrame(page)
        card.setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 20px;")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("<b>Tizim va Tarif Sozlamalari (Haqiqiy Baza)</b>"))

        grid = QGridLayout()
        self.day_rate_edit = QLineEdit()
        self.night_rate_edit = QLineEdit()
        self.grace_edit = QLineEdit()
        self.exit_grace_edit = QLineEdit()
        self.daily_cap_edit = QLineEdit()

        grid.addWidget(QLabel("Kunduzgi soatlik stavka (UZS):"), 0, 0)
        grid.addWidget(self.day_rate_edit, 0, 1)

        grid.addWidget(QLabel("Tungi soatlik stavka (UZS):"), 1, 0)
        grid.addWidget(self.night_rate_edit, 1, 1)

        grid.addWidget(QLabel("Dastlabki bepul oraliq (Daqiqa):"), 2, 0)
        grid.addWidget(self.grace_edit, 2, 1)

        grid.addWidget(QLabel("To'lovdan so'ng chiqish oralig'i (Daqiqa):"), 3, 0)
        grid.addWidget(self.exit_grace_edit, 3, 1)

        grid.addWidget(QLabel("Kunlik maksimal to'lov (UZS):"), 4, 0)
        grid.addWidget(self.daily_cap_edit, 4, 1)

        cl.addLayout(grid)

        save_btn = QPushButton("Sozlamalarni Saqlash")
        save_btn.setIcon(get_icon("save.svg"))
        save_btn.setStyleSheet("background-color: #0d9488; color: white; padding: 10px 24px; border-radius: 10px; font-weight: bold; margin-top: 15px;")
        save_btn.clicked.connect(self.on_save_settings)
        cl.addWidget(save_btn, 0, Qt.AlignmentFlag.AlignLeft)
        cl.addStretch()

        l.addWidget(card)
        return page

    def on_save_settings(self):
        settings = {
            "day_rate": self.day_rate_edit.text().strip(),
            "night_rate": self.night_rate_edit.text().strip(),
            "grace_period": self.grace_edit.text().strip(),
            "exit_grace": self.exit_grace_edit.text().strip(),
            "daily_cap": self.daily_cap_edit.text().strip(),
        }
        self.db.save_settings(settings)
        QMessageBox.information(self, "Sozlamalar", "Barcha sozlamalar bazaga muvaffaqiyatli saqlandi!")

    def refresh_all_data(self):
        """Barcha sahifalarni bazadagi oxirgi holat bilan to'liq yangilash"""
        # 1. Bosh sahifa statistikasi
        stats = self.db.get_dashboard_stats()
        self.dash_rev_label.setText(f"{stats['total_revenue']:,} UZS".replace(",", " "))
        self.dash_free_label.setText(f"{stats['free_slots']} ta")
        self.dash_occ_label.setText(f"{stats['occupied_slots']} ta")
        self.dash_res_label.setText(f"{stats['reserved_slots']} ta")

        # 2. So'nggi harakatlar
        activities = self.db.get_recent_activities(10)
        self.dash_table.setRowCount(0)
        for r_idx, a in enumerate(activities):
            self.dash_table.insertRow(r_idx)
            self.dash_table.setItem(r_idx, 0, QTableWidgetItem(a["session_code"]))
            self.dash_table.setItem(r_idx, 1, QTableWidgetItem(a["vehicle_plate"]))
            self.dash_table.setItem(r_idx, 2, QTableWidgetItem(a["slot_number"]))
            self.dash_table.setItem(r_idx, 3, QTableWidgetItem(a["entry_time"]))
            self.dash_table.setItem(r_idx, 4, QTableWidgetItem(f"{a['total_amount']:,} UZS".replace(",", " ")))
            self.dash_table.setItem(r_idx, 5, QTableWidgetItem(a["status"]))

        # 3. 2D xarita
        if hasattr(self, "map_widget"):
            self.map_widget.reload_slots()

        # 4. Xodimlar
        staff = self.db.get_all_staff()
        self.staff_tbl.setRowCount(0)
        for idx, s in enumerate(staff):
            self.staff_tbl.insertRow(idx)
            self.staff_tbl.setItem(idx, 0, QTableWidgetItem(str(s["id"])))
            self.staff_tbl.setItem(idx, 1, QTableWidgetItem(s["username"]))
            self.staff_tbl.setItem(idx, 2, QTableWidgetItem(s["full_name"]))
            self.staff_tbl.setItem(idx, 3, QTableWidgetItem(s["role"]))
            self.staff_tbl.setItem(idx, 4, QTableWidgetItem(s["shift"]))

        # 5. Moliya
        fin = self.db.get_financial_summary()
        self.payme_val_lbl.setText(f"{fin['payme_total']:,} UZS".replace(",", " "))
        self.click_val_lbl.setText(f"{fin['click_total']:,} UZS".replace(",", " "))
        self.cash_val_lbl.setText(f"{fin['cash_total']:,} UZS".replace(",", " "))

        self.tx_tbl.setRowCount(0)
        for idx, t in enumerate(fin["transactions"]):
            self.tx_tbl.insertRow(idx)
            self.tx_tbl.setItem(idx, 0, QTableWidgetItem(t["tx_code"]))
            self.tx_tbl.setItem(idx, 1, QTableWidgetItem(t["vehicle_plate"]))
            self.tx_tbl.setItem(idx, 2, QTableWidgetItem(t["provider"]))
            self.tx_tbl.setItem(idx, 3, QTableWidgetItem(f"{t['amount']:,} UZS".replace(",", " ")))
            self.tx_tbl.setItem(idx, 4, QTableWidgetItem(t["fiscal_sign"] or "-"))

        # 6. Sozlamalar
        st = self.db.get_settings()
        if hasattr(self, "day_rate_edit"):
            self.day_rate_edit.setText(st.get("day_rate", "5000"))
            self.night_rate_edit.setText(st.get("night_rate", "3000"))
            self.grace_edit.setText(st.get("grace_period", "15"))
            self.exit_grace_edit.setText(st.get("exit_grace", "15"))
            self.daily_cap_edit.setText(st.get("daily_cap", "50000"))

    def switch_tab(self, idx):
        self.stack.setCurrentIndex(idx)
        if self.nav_group.button(idx):
            self.nav_group.button(idx).setChecked(True)
        if self.pill_group.button(idx):
            self.pill_group.button(idx).setChecked(True)

    def apply_role_permissions(self):
        role = self.user_data["role"]
        if role == "OPERATOR":
            for i in [3, 4, 5]:  # Xodimlar, Moliya, Sozlamalar
                if self.nav_group.button(i):
                    self.nav_group.button(i).setEnabled(False)
                if self.pill_group.button(i):
                    self.pill_group.button(i).setEnabled(False)


def main():
    app = QApplication(sys.argv)
    db = ParklyDatabase()

    login = LoginDialog(db)
    if login.exec() == QDialog.DialogCode.Accepted:
        win = MainDashboard(db, login.user_data)
        win.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
