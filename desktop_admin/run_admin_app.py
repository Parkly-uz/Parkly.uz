"""
Parkly.uz — Mukammal Desktop Admin Paneli (PyQt6)
Dizayn va Funksional talablari (To'liq amalga oshirilgan):
1. Card Style: Oq bloklar border-radius: 16px, mayin chegara (1px solid rgba(226, 232, 240, 0.8)) va QGraphicsDropShadowEffect (0 4px 20px rgba(0,0,0,0.03)).
2. Statistika Bloki: "Bugungi Jami Tushum" kartochkasi Deep Cyan / Dark Slate Gradient (linear-gradient(135deg, #0F172A, #0066FF)).
3. Mini Vektor Ikonkalar: "Bo'sh joylar", "Band joylar", "Bronlar" kartochkalarida "Erkin", "Band", "Rezerv" badge-lari bilan.
4. Status Badges: ACTIVE matni #DCFCE7 fonda #166534 matnli yumaloq badge (border-radius: 20px).
5. Jadval Vizualizatsiyasi: UPPERCASE alohida Header qatori (ID | AVTO RAQAM | SLOT | KIRISH VAQTI | SUMMA | STATUS), qator ustiga sichqoncha borganda #F8FAFC hover effekti, Avto raqamlari monospace stiker/ramka ichida.
6. Navigatsiya Bo'limlari (6 ta to'liq modul):
   - 📊 Dashboard (Asosiy Boshqaruv & Live logs)
   - 🗺️ 2D Interactive Map (3D Izometrik xarita, slot management, zonalarni filtrlash)
   - 📷 Camera Monitoring & ANPR (Live stream, OCR confidence, override)
   - 🚗 Vehicles & Sessions (Faol seanslar jonli taymerlar bilan, Whitelist/Blacklist, qidiruv)
   - 💳 Billing & Finance (Tariflar, Click/Payme hisoboti, vaucher va chegirmalar)
   - ⚙️ System Settings (Hardware integratsiya, MQTT/Relay, RBAC huquqlar, tizim salomatligi)
7. Mukammal Login Paneli: Rasmdagi dizayn (chapda yashil/teal brending, o'ngda oq kartochka, sinov hisoblari bir klikda to'ldirish bilan).
"""

import sys
import os
import random
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QLabel, QPushButton, QLineEdit, QComboBox,
    QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget,
    QMessageBox, QProgressBar, QScrollArea, QGraphicsDropShadowEffect,
    QTabWidget
)
from PyQt6.QtGui import (
    QColor, QFont, QLinearGradient, QPixmap, QIcon, QCursor
)
from PyQt6.QtCore import Qt, QSize, QTimer

from db_manager import ParklyDatabase
from isometric_map import IsometricParkingMapWidget

ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")


def get_icon(name: str) -> QIcon:
    """SVG ikonkani xavfsiz yuklab beruvchi yordamchi funksiya"""
    path = os.path.join(ICONS_DIR, name)
    if os.path.exists(path):
        return QIcon(path)
    return QIcon()


def apply_card_shadow(widget, blur=18, y=4, alpha=15):
    """Figma/Dribbble uslubidagi yengil va yumshoq box-shadow qo'shish"""
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setOffset(0, y)
    shadow.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(shadow)


def create_plate_badge(plate_text: str) -> QLabel:
    """Avtomobil davlat raqamini chiroyli stiker/ramka ko'rinishida chiqarish"""
    lbl = QLabel(f" {plate_text} ")
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setStyleSheet("""
        QLabel {
            background-color: #f1f5f9;
            color: #0f172a;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 11.5px;
            font-weight: 700;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 3px 8px;
        }
    """)
    return lbl


def create_status_badge(status_text: str) -> QLabel:
    """Statusni yumaloq burchakli rangli badge ko'rinishida chiqarish"""
    st = status_text.upper()
    bg, fg = "#F1F5F9", "#475569"
    display = status_text

    if "ACTIVE" in st or "ERKIN" in st or "FREE" in st or "MUVAFFAQ" in st:
        bg, fg = "#DCFCE7", "#166534"
        display = "ACTIVE"
    elif "OCCUPIED" in st or "BAND" in st or "XATOLIK" in st:
        bg, fg = "#FEE2E2", "#991B1B"
        display = "BAND"
    elif "RESERVED" in st or "REZERV" in st or "PENDING" in st or "KUTILMOQDA" in st:
        bg, fg = "#FEF3C7", "#92400E"
        display = "REZERV"
    elif "WHITELIST" in st or "VIP" in st:
        bg, fg = "#E0E7FF", "#3730A3"
        display = "WHITELIST"
    elif "BLACKLIST" in st or "BLOK" in st:
        bg, fg = "#FFE4E6", "#9F1239"
        display = "BLACKLIST"

    lbl = QLabel(f"  {display}  ")
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setStyleSheet(f"""
        QLabel {{
            background-color: {bg};
            color: {fg};
            font-size: 10.5px;
            font-weight: 700;
            border-radius: 12px;
            padding: 4px 10px;
        }}
    """)
    return lbl


# ==============================================================================
# 1. MUKAMMAL TIZIMGA KIRISH OYNASI (LOGIN PANEL — RASMDAGI DIZAYN)
# ==============================================================================
class LoginDialog(QDialog):
    """
    Foydalanuvchi taqdim etgan rasmga (media_1791450488192.png) to'liq mos keluvchi
    professional ikki ustunli kirish oynasi.
    """
    def __init__(self, db: ParklyDatabase, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Parkly.uz — Tizimga Kirish")
        self.setFixedSize(780, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.user_data = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Chap qism (Deep Teal Hero Banner)
        left_frame = QFrame(self)
        left_frame.setFixedWidth(330)
        left_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #086b59, stop:1 #064e42);
                color: white;
            }
        """)
        l_layout = QVBoxLayout(left_frame)
        l_layout.setContentsMargins(32, 40, 32, 35)

        # Logotip
        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        pix = QPixmap(logo_path)
        logo_widget = QLabel(left_frame)
        if not pix.isNull():
            logo_widget.setPixmap(pix.scaledToWidth(250, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_widget.setText("PARKLY.UZ")
            logo_widget.setStyleSheet("font-size: 26px; font-weight: 900; color: white;")
        logo_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_layout.addWidget(logo_widget)

        sub_lbl = QLabel("Aqlli Avtoturargoh Boshqaruv Tizimi", left_frame)
        sub_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #ffffff; margin-top: 18px;")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_layout.addWidget(sub_lbl)

        desc = QLabel(
            "• Real-time ANPR kamera oqimi\n"
            "• 2D/3D interaktiv slotlar xaritasi\n"
            "• Avtomatlashgan to'lov va shlagbaum\n"
            "• Super-Admin va 5 ta operator nazorati", left_frame
        )
        desc.setStyleSheet("font-size: 11.5px; color: #ccfbf1; line-height: 1.7; margin-top: 18px;")
        l_layout.addWidget(desc)
        l_layout.addStretch()

        footer = QLabel("© 2026 Parkly Ekotizimi v1.0", left_frame)
        footer.setStyleSheet("font-size: 10px; color: #5eead4;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_layout.addWidget(footer)

        main_layout.addWidget(left_frame)

        # 2. O'ng qism (Oq minimalist karta — Rasmdagi kabi)
        right_frame = QFrame(self)
        right_frame.setStyleSheet("""
            QFrame {
                background: #ffffff;
            }
        """)
        r_layout = QVBoxLayout(right_frame)
        r_layout.setContentsMargins(45, 38, 45, 30)
        r_layout.setSpacing(12)

        title = QLabel("PARKLY ADMIN", right_frame)
        title.setStyleSheet("font-size: 24px; font-weight: 900; color: #0d9488; letter-spacing: 0.5px;")
        r_layout.addWidget(title)

        subtitle = QLabel("Tizimga kirish (Foydalanuvchi hisobi)", right_frame)
        subtitle.setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 8px;")
        r_layout.addWidget(subtitle)

        # Foydalanuvchi nomi
        lbl_user = QLabel("Foydalanuvchi nomi yoki Email:", right_frame)
        lbl_user.setStyleSheet("font-weight: 600; color: #1e293b; font-size: 12px;")
        r_layout.addWidget(lbl_user)

        self.input_user = QLineEdit(right_frame)
        self.input_user.setPlaceholderText("admin")
        self.input_user.setText("admin")
        self.input_user.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                border: 1.5px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #0f172a;
            }
            QLineEdit:focus { border: 1.5px solid #0d9488; }
        """)
        r_layout.addWidget(self.input_user)

        # Maxfiy parol
        lbl_pass = QLabel("Maxfiy parol:", right_frame)
        lbl_pass.setStyleSheet("font-weight: 600; color: #1e293b; font-size: 12px;")
        r_layout.addWidget(lbl_pass)

        self.input_pass = QLineEdit(right_frame)
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setPlaceholderText("••••••••")
        self.input_pass.setText("admin123")
        self.input_pass.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                border: 1.5px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #0f172a;
            }
            QLineEdit:focus { border: 1.5px solid #0d9488; }
        """)
        r_layout.addWidget(self.input_pass)

        # "Meni tizimda eslab qol"
        self.chk_remember = QCheckBox("Meni tizimda eslab qol", right_frame)
        self.chk_remember.setChecked(True)
        self.chk_remember.setStyleSheet("font-size: 12px; color: #475569;")
        r_layout.addWidget(self.chk_remember)

        # Kirish tugmasi
        self.btn_login = QPushButton("Tizimga Kirish", right_frame)
        self.btn_login.setIcon(get_icon("lock.svg"))
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background: #0d9488;
                color: white;
                font-size: 14px;
                font-weight: 700;
                padding: 12px;
                border-radius: 8px;
                border: none;
                margin-top: 6px;
            }
            QPushButton:hover { background: #0f766e; }
            QPushButton:pressed { background: #115e59; }
        """)
        self.btn_login.clicked.connect(self.attempt_login)
        r_layout.addWidget(self.btn_login)

        # 3. Sinov hisoblari paneli (Rasmdagi qizil ramkali qism — bir klikda to'ldiriladi)
        test_box = QFrame(right_frame)
        test_box.setStyleSheet("""
            QFrame {
                background: #f8fafc;
                border: 1px dashed #cbd5e1;
                border-radius: 8px;
                padding: 8px;
                margin-top: 8px;
            }
        """)
        tb_layout = QHBoxLayout(test_box)
        tb_layout.setContentsMargins(6, 4, 6, 4)

        tb_lbl = QLabel("Sinov:", test_box)
        tb_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #64748b;")
        tb_layout.addWidget(tb_lbl)

        btn_fill_admin = QPushButton("Super-Admin: admin", test_box)
        btn_fill_admin.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_fill_admin.setStyleSheet("color: #0d9488; font-weight: 700; font-size: 11px; border: none; background: transparent;")
        btn_fill_admin.clicked.connect(lambda: self.fill_credentials("admin", "admin123"))
        tb_layout.addWidget(btn_fill_admin)

        tb_div = QLabel("|", test_box)
        tb_div.setStyleSheet("color: #cbd5e1;")
        tb_layout.addWidget(tb_div)

        btn_fill_op = QPushButton("Operator: operator1", test_box)
        btn_fill_op.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_fill_op.setStyleSheet("color: #0d9488; font-weight: 700; font-size: 11px; border: none; background: transparent;")
        btn_fill_op.clicked.connect(lambda: self.fill_credentials("operator1", "operator123"))
        tb_layout.addWidget(btn_fill_op)

        r_layout.addWidget(test_box)
        r_layout.addStretch()

        main_layout.addWidget(right_frame)

    def fill_credentials(self, u, p):
        self.input_user.setText(u)
        self.input_pass.setText(p)

    def attempt_login(self):
        u = self.input_user.text().strip()
        p = self.input_pass.text().strip()
        if not u or not p:
            QMessageBox.warning(self, "Diqqat", "Iltimos, login va parolni kiriting!")
            return

        user = self.db.authenticate(u, p)
        if user:
            self.user_data = user
            self.accept()
        else:
            QMessageBox.critical(self, "Xatolik", "Login yoki maxfiy parol noto'g'ri!")


# ==============================================================================
# 2. ADMIN PROFILI VA PAROLNI SOZLASH DIALOGI
# ==============================================================================
class AdminProfileDialog(QDialog):
    def __init__(self, db: ParklyDatabase, user_data: dict, parent=None):
        super().__init__(parent)
        self.db = db
        self.user_data = user_data
        self.logout_requested = False
        self.setWindowTitle("Admin Profili va Xavfsizlik Sozlamalari")
        self.setFixedSize(460, 540)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("QDialog { background: #f8fafc; font-family: 'Segoe UI', sans-serif; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)

        card = QFrame(self)
        card.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px;")
        apply_card_shadow(card)
        c_layout = QVBoxLayout(card)

        # Avatar
        avatar = QLabel(self.user_data.get("full_name", "A")[0].upper(), card)
        avatar.setFixedSize(54, 54)
        avatar.setStyleSheet("background: #0d9488; color: white; font-size: 22px; font-weight: 800; border-radius: 27px;")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c_layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignCenter)

        t_lbl = QLabel(self.user_data.get("full_name", "Admin"), card)
        t_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 4px;")
        t_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c_layout.addWidget(t_lbl)

        role_lbl = QLabel(f"Roli: {self.user_data.get('role', 'SUPER_ADMIN')}", card)
        role_lbl.setStyleSheet("background: #dcfce7; color: #166534; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 10px;")
        role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c_layout.addWidget(role_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        c_layout.addWidget(QLabel("To'liq Ism (F.I.Sh):"))
        self.in_name = QLineEdit(card)
        self.in_name.setText(self.user_data.get("full_name", ""))
        c_layout.addWidget(self.in_name)

        c_layout.addWidget(QLabel("Foydalanuvchi nomi (Login):"))
        self.in_user = QLineEdit(card)
        self.in_user.setText(self.user_data.get("username", ""))
        c_layout.addWidget(self.in_user)

        c_layout.addWidget(QLabel("Hozirgi parol (Tasdiqlash uchun):"))
        self.in_curr = QLineEdit(card)
        self.in_curr.setEchoMode(QLineEdit.EchoMode.Password)
        c_layout.addWidget(self.in_curr)

        c_layout.addWidget(QLabel("Yangi parol (Ixtiyoriy):"))
        self.in_new = QLineEdit(card)
        self.in_new.setEchoMode(QLineEdit.EchoMode.Password)
        c_layout.addWidget(self.in_new)

        layout.addWidget(card)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Saqlash", self)
        btn_save.setIcon(get_icon("save.svg"))
        btn_save.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 10px 18px; border-radius: 8px;")
        btn_save.clicked.connect(self.save)
        btn_box.addWidget(btn_save)

        btn_logout = QPushButton("Tizimdan Chiqish", self)
        btn_logout.setIcon(get_icon("logout.svg"))
        btn_logout.setStyleSheet("background: #fee2e2; color: #991b1b; font-weight: 700; padding: 10px 14px; border-radius: 8px;")
        btn_logout.clicked.connect(self.logout)
        btn_box.addWidget(btn_logout)

        layout.addLayout(btn_box)

    def save(self):
        new_name = self.in_name.text().strip()
        new_user = self.in_user.text().strip()
        curr_p = self.in_curr.text().strip()
        new_p = self.in_new.text().strip()

        if not curr_p:
            QMessageBox.warning(self, "Diqqat", "O'zgarishlarni tasdiqlash uchun hozirgi parolingizni kiriting!")
            return

        ok, msg = self.db.update_user_profile(
            self.user_data["id"], new_name, new_user,
            current_password=curr_p, new_password=new_p if new_p else None
        )
        if ok:
            self.user_data["full_name"] = new_name
            self.user_data["username"] = new_user
            QMessageBox.information(self, "Muvaffaqiyat", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Rad etildi", msg)

    def logout(self):
        self.logout_requested = True
        self.accept()


# ==============================================================================
# 3. ASOSIY DASTUR OYNASI (MAIN WINDOW — 6 TA TO'LIQ MODUL)
# ==============================================================================
class MainWindow(QMainWindow):
    def __init__(self, db: ParklyDatabase, user_data: dict):
        super().__init__()
        self.db = db
        self.user_data = user_data

        self.setWindowTitle("Parkly.uz — Aqlli Avtoturargoh Boshqaruv Tizimi")
        self.resize(1360, 860)
        self.setMinimumSize(1100, 700)

        self.setup_ui()
        self.init_timers()
        self.refresh_all_data()

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Global Dribbble/Figma Card Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }
            QFrame.whiteCard {
                background-color: #ffffff;
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 16px;
            }
            /* Jadval (Table) Stilining Mukammalligi */
            QTableWidget {
                background-color: #ffffff;
                border: none;
                gridline-color: transparent;
                selection-background-color: #f1f5f9;
                selection-color: #0f172a;
                font-size: 12px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #f1f5f9;
                padding-top: 10px;
                padding-bottom: 10px;
            }
            QTableWidget::item:hover {
                background-color: #f8fafc;
            }
            QHeaderView::section {
                background-color: #ffffff;
                color: #64748b;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                padding: 10px 14px;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff;
                border: 1.5px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12.5px;
                color: #0f172a;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1.5px solid #0d9488;
            }
        """)

        root_layout = QVBoxLayout(self.central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ----------------------------------------------------------------------
        # TOP NAVIGATION BAR (LOGO, MENYU TUGMASI, SOAT, NOTIFIKATSIYA, PROFIL)
        # ----------------------------------------------------------------------
        top_bar = QFrame(self.central_widget)
        top_bar.setFixedHeight(68)
        top_bar.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 24, 0)
        top_layout.setSpacing(14)

        # 1. Menyu tugmasi (Drawer toggle)
        self.btn_menu = QPushButton(top_bar)
        self.btn_menu.setIcon(get_icon("menu.svg"))
        self.btn_menu.setIconSize(QSize(20, 20))
        self.btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_menu.setToolTip("Navigatsiya menyusini ochish / yopish")
        self.btn_menu.setStyleSheet("""
            QPushButton {
                background: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 7px 10px;
            }
            QPushButton:hover { background: #e2e8f0; }
        """)
        self.btn_menu.clicked.connect(self.toggle_drawer)
        top_layout.addWidget(self.btn_menu)

        # 2. Logo
        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        pix = QPixmap(logo_path)
        logo_lbl = QLabel(top_bar)
        if not pix.isNull():
            logo_lbl.setPixmap(pix.scaledToHeight(36, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_lbl.setText("PARKLY.UZ")
            logo_lbl.setStyleSheet("font-size: 19px; font-weight: 900; color: #0d9488;")
        top_layout.addWidget(logo_lbl)

        # Joriy modul sarlavhasi
        self.lbl_module_title = QLabel("Dashboard (Asosiy Boshqaruv)", top_bar)
        self.lbl_module_title.setStyleSheet("font-size: 14.5px; font-weight: 700; color: #475569; margin-left: 10px;")
        top_layout.addWidget(self.lbl_module_title)

        top_layout.addStretch()

        # Soat va sana pilli
        self.lbl_clock = QLabel(top_bar)
        self.lbl_clock.setStyleSheet("""
            background: #f1f5f9;
            color: #475569;
            font-size: 11.5px;
            font-weight: 600;
            padding: 5px 14px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
        """)
        top_layout.addWidget(self.lbl_clock)

        # Notification Bell
        self.btn_notif = QPushButton(top_bar)
        self.btn_notif.setIcon(get_icon("bell.svg"))
        self.btn_notif.setIconSize(QSize(18, 18))
        self.btn_notif.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_notif.setStyleSheet("""
            QPushButton {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 6px 12px;
                font-weight: 800;
                font-size: 11px;
                color: #ef4444;
            }
            QPushButton:hover { background: #fee2e2; }
        """)
        self.btn_notif.clicked.connect(self.show_notifications)
        top_layout.addWidget(self.btn_notif)

        # Admin Profile Pill
        self.btn_profile = QPushButton(top_bar)
        self.btn_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_profile.setStyleSheet("""
            QPushButton {
                background: #f8fafc;
                border: 1.5px solid #e2e8f0;
                border-radius: 20px;
                padding: 4px 14px;
            }
            QPushButton:hover { background: #ffffff; border-color: #0d9488; }
        """)
        self.btn_profile.clicked.connect(self.open_profile_dialog)
        top_layout.addWidget(self.btn_profile)
        self.update_user_topbar()

        root_layout.addWidget(top_bar)

        # ----------------------------------------------------------------------
        # ASOSIY MAYDON (YASHIRIN DRAWER VA 6 TA MODUL STACKI)
        # ----------------------------------------------------------------------
        body_box = QHBoxLayout()
        body_box.setContentsMargins(0, 0, 0, 0)
        body_box.setSpacing(0)

        # Collapsible Drawer (Navigatsiya Menyusi)
        self.drawer = QFrame(self.central_widget)
        self.drawer.setFixedWidth(240)
        self.drawer.setVisible(False)  # Boshlang'ich holatda yashirilgan!
        self.drawer.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-right: 1px solid #e2e8f0;
            }
            QPushButton {
                text-align: left;
                padding: 12px 18px;
                font-size: 13px;
                font-weight: 600;
                color: #334155;
                border-radius: 10px;
                border: none;
                margin: 2px 10px;
            }
            QPushButton:hover {
                background: #f1f5f9;
                color: #0d9488;
            }
            QPushButton:checked {
                background: #ccfbf1;
                color: #0f766e;
                font-weight: 700;
            }
        """)
        d_layout = QVBoxLayout(self.drawer)
        d_layout.setContentsMargins(0, 16, 0, 16)
        d_layout.setSpacing(4)

        # Drawer Title & Close Button
        dh = QHBoxLayout()
        dh.setContentsMargins(16, 0, 12, 10)
        dh_lbl = QLabel("NAVIGATSIYA BO'LIMLARI", self.drawer)
        dh_lbl.setStyleSheet("font-size: 10.5px; font-weight: 800; color: #94a3b8; letter-spacing: 0.5px;")
        dh.addWidget(dh_lbl)
        dh.addStretch()

        btn_c = QPushButton(self.drawer)
        btn_c.setIcon(get_icon("close.svg"))
        btn_c.setFixedSize(26, 26)
        btn_c.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c.setStyleSheet("background: transparent; border: none; padding: 2px;")
        btn_c.clicked.connect(self.toggle_drawer)
        dh.addWidget(btn_c)
        d_layout.addLayout(dh)

        self.nav_btns = []
        modules = [
            ("1. Dashboard", "dashboard.svg", 0),
            ("2. 2D Interactive Map", "map.svg", 1),
            ("3. Camera Monitoring", "camera.svg", 2),
            ("4. Vehicles & Sessions", "car.svg", 3),
            ("5. Billing & Finance", "wallet.svg", 4),
            ("6. System Settings", "settings.svg", 5),
        ]

        for title, icon, idx in modules:
            b = QPushButton(f"  {title}", self.drawer)
            b.setIcon(get_icon(icon))
            b.setIconSize(QSize(18, 18))
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda ch, i=idx, t=title: self.navigate_module(i, t))
            self.nav_btns.append(b)
            d_layout.addWidget(b)

        self.nav_btns[0].setChecked(True)
        d_layout.addStretch()

        btn_d_logout = QPushButton("  Tizimdan Chiqish", self.drawer)
        btn_d_logout.setIcon(get_icon("logout.svg"))
        btn_d_logout.setStyleSheet("color: #ef4444; font-weight: 700;")
        btn_d_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_d_logout.clicked.connect(self.logout_user)
        d_layout.addWidget(btn_d_logout)

        body_box.addWidget(self.drawer)

        # 6 Ta Modul Sahifasi (QStackedWidget)
        self.stack = QStackedWidget(self.central_widget)
        self.stack.addWidget(self.build_dashboard_page())    # Modul 1
        self.stack.addWidget(self.build_map_page())          # Modul 2
        self.stack.addWidget(self.build_cameras_page())      # Modul 3
        self.stack.addWidget(self.build_sessions_page())     # Modul 4
        self.stack.addWidget(self.build_finance_page())      # Modul 5
        self.stack.addWidget(self.build_settings_page())     # Modul 6

        body_box.addWidget(self.stack)
        root_layout.addLayout(body_box)

    def toggle_drawer(self):
        self.drawer.setVisible(not self.drawer.isVisible())

    def navigate_module(self, idx, title):
        for i, b in enumerate(self.nav_btns):
            b.setChecked(i == idx)
        self.stack.setCurrentIndex(idx)
        self.lbl_module_title.setText(title)

    def update_user_topbar(self):
        name = self.user_data.get("full_name", "Admin")
        role = self.user_data.get("role", "SUPER_ADMIN")
        initial = name[0].upper() if name else "A"
        self.btn_profile.setText(f" {initial}  |  {name}  ({role})  ▾")
        self.btn_profile.setIcon(get_icon("user.svg"))

        unread = self.db.get_unread_notifications_count()
        self.btn_notif.setText(f" {unread}" if unread > 0 else "")

    def open_profile_dialog(self):
        dlg = AdminProfileDialog(self.db, self.user_data, self)
        if dlg.exec():
            if dlg.logout_requested:
                self.logout_user()
            else:
                self.update_user_topbar()

    def show_notifications(self):
        notifs = self.db.get_notifications(limit=10)
        msg = "\n\n".join([f"• [{n['type']}] {n['title']}: {n['message']}" for n in notifs]) or "Xabarnomalar yo'q."
        QMessageBox.information(self, "Tizim Bildirishnomalari", msg)
        self.db.mark_all_notifications_read()
        self.update_user_topbar()

    def logout_user(self):
        self.close()
        login = LoginDialog(self.db)
        if login.exec():
            self.user_data = login.user_data
            self.update_user_topbar()
            self.show()

    # --------------------------------------------------------------------------
    # MODUL 1: DASHBOARD (ASOSIY BOSHQARUV & LIVE FEED)
    # --------------------------------------------------------------------------
    def build_dashboard_page(self):
        page = QWidget()
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(20)

        # 1. Welcome Card
        wel_card = QFrame(inner)
        wel_card.setProperty("class", "whiteCard")
        wel_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 16px 22px;")
        apply_card_shadow(wel_card)
        w_box = QHBoxLayout(wel_card)

        wl_text = QVBoxLayout()
        wl_t = QLabel(f"Xayrli kun, {self.user_data.get('full_name')}!", wel_card)
        wl_t.setStyleSheet("font-size: 21px; font-weight: 800; color: #0f172a;")
        wl_text.addWidget(wl_t)

        wl_sub = QLabel("Parkly.uz — Avtoturargoh real-vaqt holati, moliyaviy oqim va ANPR monitoringi.", wel_card)
        wl_sub.setStyleSheet("font-size: 12px; color: #64748b; margin-top: 2px;")
        wl_text.addWidget(wl_sub)
        w_box.addLayout(wl_text)
        w_box.addStretch()

        btn_sim = QPushButton("Avto Kiritish (Simulyatsiya)", wel_card)
        btn_sim.setIcon(get_icon("car.svg"))
        btn_sim.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sim.setStyleSheet("""
            QPushButton {
                background: #0d9488; color: white; font-size: 13px; font-weight: 700;
                padding: 10px 18px; border-radius: 10px; border: none;
            }
            QPushButton:hover { background: #0f766e; }
        """)
        btn_sim.clicked.connect(self.simulate_car_entry)
        w_box.addWidget(btn_sim)
        layout.addWidget(wel_card)

        # 2. Statistika Bloki (Deep Cyan / Dark Slate Gradient va Mini Vektor Ikonkalar)
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(16)

        # Kartochka 1: Bugungi Jami Tushum (Deep Cyan / Dark Slate Gradient)
        self.card_rev = QFrame(inner)
        self.card_rev.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0F172A, stop:0.6 #0b2559, stop:1 #0066FF);
                border-radius: 16px;
                padding: 16px;
            }
        """)
        apply_card_shadow(self.card_rev)
        cr_box = QVBoxLayout(self.card_rev)

        cr_top = QHBoxLayout()
        cr_title = QLabel("Bugungi Jami Tushum", self.card_rev)
        cr_title.setStyleSheet("font-size: 12px; font-weight: 600; color: #93c5fd;")
        cr_top.addWidget(cr_title)
        cr_top.addStretch()

        cr_trend = QLabel("📈 +14.2% bugun", self.card_rev)
        cr_trend.setStyleSheet("font-size: 10.5px; font-weight: 700; color: #67e8f9; background: rgba(255,255,255,0.12); padding: 3px 8px; border-radius: 10px;")
        cr_top.addWidget(cr_trend)
        cr_box.addLayout(cr_top)

        self.lbl_rev_val = QLabel("0 UZS", self.card_rev)
        self.lbl_rev_val.setStyleSheet("font-size: 24px; font-weight: 900; color: #ffffff; margin-top: 6px;")
        cr_box.addWidget(self.lbl_rev_val)
        kpi_grid.addWidget(self.card_rev, 0, 0)

        # Kartochka 2: Bo'sh Joylar ("Erkin" mini badge bilan)
        self.card_free, self.lbl_free_val = self._create_stat_card("Bo'sh Joylar", "0 ta", "car.svg", "Erkin", "#DCFCE7", "#166534")
        kpi_grid.addWidget(self.card_free, 0, 1)

        # Kartochka 3: Band Joylar ("Band" mini badge bilan)
        self.card_occ, self.lbl_occ_val = self._create_stat_card("Band Joylar", "0 ta", "lock.svg", "Band", "#FEE2E2", "#991B1B")
        kpi_grid.addWidget(self.card_occ, 0, 2)

        # Kartochka 4: Faol Bronlar ("Rezerv" mini badge bilan)
        self.card_res, self.lbl_res_val = self._create_stat_card("Faol Bronlar", "0 ta", "star.svg", "Rezerv", "#FEF3C7", "#92400E")
        kpi_grid.addWidget(self.card_res, 0, 3)

        layout.addLayout(kpi_grid)

        # Bandlik progress-bari
        p_card = QFrame(inner)
        p_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 14px; padding: 12px 18px;")
        apply_card_shadow(p_card)
        pb_box = QVBoxLayout(p_card)
        self.lbl_occ_pct = QLabel("Avtoturargoh bandlik darajasi: Hisoblanmoqda...", p_card)
        self.lbl_occ_pct.setStyleSheet("font-size: 12px; font-weight: 700; color: #334155;")
        pb_box.addWidget(self.lbl_occ_pct)

        self.bar_occ = QProgressBar(p_card)
        self.bar_occ.setFixedHeight(8)
        self.bar_occ.setTextVisible(False)
        self.bar_occ.setStyleSheet("""
            QProgressBar { background: #e2e8f0; border-radius: 4px; border: none; }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:0.7 #f59e0b, stop:1 #ef4444);
                border-radius: 4px;
            }
        """)
        pb_box.addWidget(self.bar_occ)
        layout.addWidget(p_card)

        # 3. Ikki ustunli qism: Mini 3D Izometrik Preview va Pastki Mukammal Jadval
        mid_row = QHBoxLayout()
        mid_row.setSpacing(16)

        # Chap: Mini 3D Izometrik Xarita
        iso_box = QFrame(inner)
        iso_box.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 14px;")
        apply_card_shadow(iso_box)
        ib_layout = QVBoxLayout(iso_box)

        ibh = QHBoxLayout()
        ibh_t = QLabel("3D Izometrik Xarita (Live Preview)", iso_box)
        ibh_t.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        ibh.addWidget(ibh_t)
        ibh.addStretch()

        btn_to_map = QPushButton("To'liq Xarita ➔", iso_box)
        btn_to_map.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_to_map.setStyleSheet("color: #0d9488; font-weight: 700; border: none; font-size: 12px;")
        btn_to_map.clicked.connect(lambda: self.navigate_module(1, "2. 2D Interactive Map"))
        ibh.addWidget(btn_to_map)
        ib_layout.addLayout(ibh)

        self.dash_iso_map = IsometricParkingMapWidget(iso_box, is_mini=True)
        self.dash_iso_map.slot_clicked.connect(self.on_slot_clicked)
        ib_layout.addWidget(self.dash_iso_map)
        mid_row.addWidget(iso_box, stretch=5)

        # O'ng: Live Activity Feed & Alert Box
        feed_box = QFrame(inner)
        feed_box.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 14px;")
        apply_card_shadow(feed_box)
        fb_layout = QVBoxLayout(feed_box)

        fbh = QHBoxLayout()
        fbh_t = QLabel("Live Activity Feed (Real-vaqt Xronologiyasi)", feed_box)
        fbh_t.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        fbh.addWidget(fbh_t)
        fbh.addStretch()

        btn_r = QPushButton("Yangilash", feed_box)
        btn_r.setIcon(get_icon("refresh.svg"))
        btn_r.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_r.setStyleSheet("color: #0d9488; font-weight: 700; border: none; font-size: 12px;")
        btn_r.clicked.connect(self.refresh_all_data)
        fbh.addWidget(btn_r)
        fb_layout.addLayout(fbh)

        self.table_feed = QTableWidget(feed_box)
        self.table_feed.setColumnCount(4)
        self.table_feed.setHorizontalHeaderLabels(["SEANS", "AVTO RAQAM", "SLOT", "STATUS"])
        self.table_feed.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_feed.verticalHeader().setVisible(False)
        fb_layout.addWidget(self.table_feed)

        mid_row.addWidget(feed_box, stretch=6)
        layout.addLayout(mid_row)

        # 4. Pastki Asosiy Jadval (UPPERCASE Headers, Stiker raqamlar, Status badge)
        tbl_card = QFrame(inner)
        tbl_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 18px;")
        apply_card_shadow(tbl_card)
        tc_layout = QVBoxLayout(tbl_card)

        tch = QHBoxLayout()
        tch_t = QLabel("So'nggi Kirish-Chiqish va To'lov Harakatlari (Baza)", tbl_card)
        tch_t.setStyleSheet("font-size: 15px; font-weight: 800; color: #0f172a;")
        tch.addWidget(tch_t)
        tch.addStretch()
        tc_layout.addLayout(tch)

        # Mukammal Data Table: ID | AVTO RAQAM | SLOT | KIRISH VAQTI | SUMMA | STATUS
        self.table_recent = QTableWidget(tbl_card)
        self.table_recent.setColumnCount(6)
        self.table_recent.setHorizontalHeaderLabels([
            "ID", "AVTO RAQAM", "SLOT", "KIRISH VAQTI", "SUMMA", "STATUS"
        ])
        self.table_recent.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_recent.verticalHeader().setVisible(False)
        tc_layout.addWidget(self.table_recent)

        layout.addWidget(tbl_card)

        scroll.setWidget(inner)
        p_box = QVBoxLayout(page)
        p_box.setContentsMargins(0, 0, 0, 0)
        p_box.addWidget(scroll)
        return page

    def _create_stat_card(self, title, val, icon_name, badge_text, badge_bg, badge_fg):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 16px;
                padding: 16px;
            }
        """)
        apply_card_shadow(card)
        box = QVBoxLayout(card)

        top = QHBoxLayout()
        t_lbl = QLabel(title, card)
        t_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #64748b;")
        top.addWidget(t_lbl)
        top.addStretch()

        # Mini vektor ikonkali badge
        b_lbl = QLabel(f" {badge_text} ", card)
        b_lbl.setStyleSheet(f"background: {badge_bg}; color: {badge_fg}; font-size: 10.5px; font-weight: 700; padding: 3px 8px; border-radius: 10px;")
        top.addWidget(b_lbl)
        box.addLayout(top)

        v_lbl = QLabel(val, card)
        v_lbl.setStyleSheet("font-size: 24px; font-weight: 900; color: #0f172a; margin-top: 6px;")
        box.addWidget(v_lbl)
        return card, v_lbl

    # --------------------------------------------------------------------------
    # MODUL 2: 2D/3D INTERACTIVE MAP (SLOT MANAGEMENT & FILTERS)
    # --------------------------------------------------------------------------
    def build_map_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(14)

        top_bar = QFrame(page)
        top_bar.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 14px; padding: 10px 16px;")
        apply_card_shadow(top_bar)
        tb_box = QHBoxLayout(top_bar)

        self.btn_f1 = QPushButton("1-Qavat (Asosiy / A-Zona)", top_bar)
        self.btn_f1.setCheckable(True)
        self.btn_f1.setChecked(True)
        self.btn_f1.setStyleSheet("QPushButton { background: #f1f5f9; font-weight: 700; padding: 8px 16px; border-radius: 8px; } QPushButton:checked { background: #0d9488; color: white; }")
        self.btn_f1.clicked.connect(lambda: self.switch_floor(1))
        tb_box.addWidget(self.btn_f1)

        self.btn_f2 = QPushButton("2-Qavat (B-Zona & EV)", top_bar)
        self.btn_f2.setCheckable(True)
        self.btn_f2.setStyleSheet("QPushButton { background: #f1f5f9; font-weight: 700; padding: 8px 16px; border-radius: 8px; } QPushButton:checked { background: #0d9488; color: white; }")
        self.btn_f2.clicked.connect(lambda: self.switch_floor(2))
        tb_box.addWidget(self.btn_f2)

        tb_box.addStretch()

        tb_lbl = QLabel("Zonalar: A-Zona (Standart) | EV (Zaryadlash) | VIP (Xodim)", top_bar)
        tb_lbl.setStyleSheet("font-size: 11.5px; color: #64748b; font-weight: 600;")
        tb_box.addWidget(tb_lbl)

        btn_sim = QPushButton("Avto Kiritish", top_bar)
        btn_sim.setIcon(get_icon("car.svg"))
        btn_sim.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 8px 14px; border-radius: 8px;")
        btn_sim.clicked.connect(self.simulate_car_entry)
        tb_box.addWidget(btn_sim)

        layout.addWidget(top_bar)

        self.full_iso_map = IsometricParkingMapWidget(page, is_mini=False)
        self.full_iso_map.slot_clicked.connect(self.on_slot_clicked)
        layout.addWidget(self.full_iso_map, stretch=1)
        return page

    def switch_floor(self, fl):
        self.btn_f1.setChecked(fl == 1)
        self.btn_f2.setChecked(fl == 2)
        slots = self.db.get_slots(floor=fl)
        self.full_iso_map.set_slots(slots, floor=fl)

    def on_slot_clicked(self, sdata):
        from run_admin_app import SlotEditDialog
        dlg = SlotEditDialog(sdata, self.db, self)
        if dlg.exec():
            self.refresh_all_data()

    # --------------------------------------------------------------------------
    # MODUL 3: CAMERA MONITORING & ANPR (LIVE STREAM & OVERRIDE)
    # --------------------------------------------------------------------------
    def build_cameras_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(16)

        title = QLabel("Universal Kameralar Oqimi & ANPR Nazorati (Kirish / Chiqish)", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(16)

        cam1 = self._build_cam_widget("Kamera #1 — Kirish Darvozasi (ANPR Faol)", "01 A 777 AA", "99.4%", "Avtomatik ochildi")
        cam2 = self._build_cam_widget("Kamera #2 — Chiqish Shlagbaumi (Kassa)", "10 123 BBA", "98.7%", "To'lov kutilyapti")
        grid.addWidget(cam1, 0, 0)
        grid.addWidget(cam2, 0, 1)
        layout.addLayout(grid)

        # Manual Correction & Barrier Override Card
        ov_card = QFrame(page)
        ov_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 18px;")
        apply_card_shadow(ov_card)
        ov_box = QHBoxLayout(ov_card)

        ov_l = QVBoxLayout()
        ov_t = QLabel("Operator tomonidan qo'lda tahrirlash & Shlagbaumni ochish (Audit)", ov_card)
        ov_t.setStyleSheet("font-size: 14px; font-weight: 700; color: #0f172a;")
        ov_l.addWidget(ov_t)

        ov_s = QLabel("Kamera xato o'qigan holatda raqamni to'g'rilash va shlagbaumni majburiy ochish bazaga qayd etiladi.", ov_card)
        ov_s.setStyleSheet("font-size: 11.5px; color: #64748b;")
        ov_l.addWidget(ov_s)
        ov_box.addLayout(ov_l)
        ov_box.addStretch()

        btn_ov = QPushButton("Shlagbaumni Majburiy Ochish", ov_card)
        btn_ov.setIcon(get_icon("barrier.svg"))
        btn_ov.setStyleSheet("background: #ef4444; color: white; font-weight: 700; padding: 10px 18px; border-radius: 8px;")
        btn_ov.clicked.connect(self.manual_barrier_open)
        ov_box.addWidget(btn_ov)

        layout.addWidget(ov_card)
        layout.addStretch()
        return page

    def _build_cam_widget(self, title, plate, conf, status):
        card = QFrame()
        card.setStyleSheet("background: #0f172a; border-radius: 14px; padding: 14px;")
        apply_card_shadow(card)
        box = QVBoxLayout(card)

        head = QHBoxLayout()
        t_lbl = QLabel(title, card)
        t_lbl.setStyleSheet("color: white; font-size: 13px; font-weight: 700;")
        head.addWidget(t_lbl)
        head.addStretch()

        rec = QLabel("● LIVE 30 FPS", card)
        rec.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 11px;")
        head.addWidget(rec)
        box.addLayout(head)

        screen = QLabel(card)
        screen.setFixedHeight(220)
        screen.setStyleSheet("background: #1e293b; border: 1px dashed #334155; border-radius: 10px; color: #38bdf8; font-family: monospace; font-size: 12px;")
        screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        screen.setText(f"[ ANPR REAL-TIME STREAM ]\nAniqlangan avto: {plate}\nConfidence: {conf} | CLAHE: On | Homography: OK")
        box.addWidget(screen)

        foot = QHBoxLayout()
        f_lbl = QLabel(f"Oxirgi o'qilgan: <b>{plate}</b>", card)
        f_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        foot.addWidget(f_lbl)
        foot.addStretch()

        st_lbl = QLabel(status, card)
        st_lbl.setStyleSheet("color: #10b981; font-weight: bold; font-size: 11px;")
        foot.addWidget(st_lbl)
        box.addLayout(foot)
        return card

    def manual_barrier_open(self):
        u = self.user_data.get("username", "admin")
        n = self.user_data.get("full_name", "Operator")
        self.db.log_barrier_override(u, n, "Operator paneli orqali qo'lda ochildi")
        QMessageBox.information(self, "Shlagbaum", "Shlagbaum ochildi va audit jurnali yangilandi!")
        self.update_user_topbar()

    # --------------------------------------------------------------------------
    # MODUL 4: VEHICLES & SESSIONS (FAOL SEANSLAR & WHITELIST / BLACKLIST)
    # --------------------------------------------------------------------------
    def build_sessions_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(14)

        title = QLabel("Avtomobillar va Sessiyalar Boshqaruvi", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        tabs = QTabWidget(page)
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid rgba(226, 232, 240, 0.8); background: #ffffff; border-radius: 14px; }
            QTabBar::tab { background: #f1f5f9; color: #475569; font-weight: 700; padding: 10px 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px; }
            QTabBar::tab:selected { background: #0d9488; color: white; }
        """)

        # Tab 1: Faol Sessiyalar (Live Timers)
        tab_active = QWidget()
        ta_box = QVBoxLayout(tab_active)
        ta_box.setContentsMargins(16, 16, 16, 16)

        tah = QHBoxLayout()
        tah_lbl = QLabel("Hozirda turargohda turgan avtomobillar ro'yxati va seans taymerlari", tab_active)
        tah_lbl.setStyleSheet("font-weight: 600; color: #64748b; font-size: 12px;")
        tah.addWidget(tah_lbl)
        tah.addStretch()

        self.in_search_session = QLineEdit(tab_active)
        self.in_search_session.setPlaceholderText("Raqam yoki seans bo'yicha qidirish...")
        self.in_search_session.setFixedWidth(260)
        self.in_search_session.textChanged.connect(self.filter_sessions)
        tah.addWidget(self.in_search_session)
        ta_box.addLayout(tah)

        self.table_sessions = QTableWidget(tab_active)
        self.table_sessions.setColumnCount(6)
        self.table_sessions.setHorizontalHeaderLabels(["SEANS", "AVTO RAQAM", "SLOT", "KIRISH VAQTI", "DAVOMIYLIK", "STATUS"])
        self.table_sessions.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_sessions.verticalHeader().setVisible(False)
        ta_box.addWidget(self.table_sessions)
        tabs.addTab(tab_active, "Faol Seanslar")

        # Tab 2: Whitelist & Blacklist
        tab_list = QWidget()
        tl_box = QVBoxLayout(tab_list)
        tl_box.setContentsMargins(16, 16, 16, 16)

        tlh = QHBoxLayout()
        tlh_lbl = QLabel("Ruxsat berilgan (VIP) va taqiqlangan avtomobillar bazasi", tab_list)
        tlh_lbl.setStyleSheet("font-weight: 600; color: #64748b; font-size: 12px;")
        tlh.addWidget(tlh_lbl)
        tlh.addStretch()

        btn_add_access = QPushButton("Raqam Qo'shish", tab_list)
        btn_add_access.setIcon(get_icon("plus.svg"))
        btn_add_access.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px;")
        btn_add_access.clicked.connect(self.add_access_dialog)
        tlh.addWidget(btn_add_access)
        tl_box.addLayout(tlh)

        self.table_access = QTableWidget(tab_list)
        self.table_access.setColumnCount(5)
        self.table_access.setHorizontalHeaderLabels(["ID", "AVTO RAQAM", "RO'YXAT TURI", "IZOH", "AMAL"])
        self.table_access.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_access.verticalHeader().setVisible(False)
        tl_box.addWidget(self.table_access)
        tabs.addTab(tab_list, "Whitelist / Blacklist")

        layout.addWidget(tabs)
        return page

    def filter_sessions(self, text):
        query = text.strip()
        if not query:
            self.load_active_sessions()
            return
        res = self.db.search_sessions_history(query)
        self._populate_sessions_table(res)

    def add_access_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Ro'yxatga avto raqam kiritish")
        dlg.setFixedSize(360, 260)
        l = QVBoxLayout(dlg)
        l.setSpacing(10)

        in_p = QLineEdit(dlg)
        in_p.setPlaceholderText("Avto raqam (01 A 777 AA)")
        l.addWidget(in_p)

        cb_t = QComboBox(dlg)
        cb_t.addItems(["WHITELIST", "BLACKLIST"])
        l.addWidget(cb_t)

        in_n = QLineEdit(dlg)
        in_n.setPlaceholderText("Izoh (masalan: VIP Rahbariyat)")
        l.addWidget(in_n)

        btn = QPushButton("Saqlash", dlg)
        btn.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 8px;")

        def save():
            p = in_p.text().strip()
            t = cb_t.currentText()
            n = in_n.text().strip()
            if p:
                self.db.add_to_access_list(p, t, n)
                dlg.accept()
                self.load_access_list()

        btn.clicked.connect(save)
        l.addWidget(btn)
        dlg.exec()

    # --------------------------------------------------------------------------
    # MODUL 5: BILLING & FINANCE (TARIFLAR, TUSHUMLAR VA VAUCHERLAR)
    # --------------------------------------------------------------------------
    def build_finance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(14)

        title = QLabel("Moliya, Tariflar va To'lovlar Nazorati", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(16)

        c_pay, self.lbl_pay_val = self._create_stat_card("Payme Tushumi", "0 UZS", "wallet.svg", "Elektron", "#DCFCE7", "#166534")
        c_clk, self.lbl_clk_val = self._create_stat_card("Click Tushumi", "0 UZS", "wallet.svg", "Elektron", "#E0F2FE", "#0369A1")
        c_csh, self.lbl_csh_val = self._create_stat_card("Naqd To'lovlar", "0 UZS", "wallet.svg", "Kassa", "#FEF3C7", "#92400E")
        grid.addWidget(c_pay, 0, 0)
        grid.addWidget(c_clk, 0, 1)
        grid.addWidget(c_csh, 0, 2)
        layout.addLayout(grid)

        # Chegirmalar va Vaucherlar (Coupons) bo'limi
        coup_card = QFrame(page)
        coup_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 16px;")
        apply_card_shadow(coup_card)
        cp_box = QVBoxLayout(coup_card)

        cph = QHBoxLayout()
        cph_t = QLabel("Vaucherlar va Chegirma Promokodlari", coup_card)
        cph_t.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        cph.addWidget(cph_t)
        cph.addStretch()

        btn_add_coup = QPushButton("Yangi Vaucher Yaratish", coup_card)
        btn_add_coup.setIcon(get_icon("plus.svg"))
        btn_add_coup.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 6px 12px; border-radius: 6px;")
        btn_add_coup.clicked.connect(self.add_coupon_dialog)
        cph.addWidget(btn_add_coup)
        cp_box.addLayout(cph)

        self.table_coupons = QTableWidget(coup_card)
        self.table_coupons.setColumnCount(4)
        self.table_coupons.setHorizontalHeaderLabels(["KOD", "CHEGIRMA (%)", "AMAL QILISH MUDDATI", "HOLAT"])
        self.table_coupons.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_coupons.verticalHeader().setVisible(False)
        cp_box.addWidget(self.table_coupons)

        layout.addWidget(coup_card)
        return page

    def add_coupon_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Yangi Vaucher / Promokod")
        dlg.setFixedSize(320, 220)
        l = QVBoxLayout(dlg)

        in_c = QLineEdit(dlg)
        in_c.setPlaceholderText("Promokod (masalan: GUEST20)")
        l.addWidget(in_c)

        in_p = QLineEdit(dlg)
        in_p.setPlaceholderText("Chegirma foizi (masalan: 20)")
        l.addWidget(in_p)

        btn = QPushButton("Yaratish", dlg)
        btn.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 8px;")

        def save():
            c = in_c.text().strip()
            p = int(in_p.text().strip() or "10")
            if c:
                self.db.add_coupon(c, p)
                dlg.accept()
                self.load_coupons()

        btn.clicked.connect(save)
        l.addWidget(btn)
        dlg.exec()

    # --------------------------------------------------------------------------
    # MODUL 6: SYSTEM SETTINGS (HARDWARE, RBAC & HEALTH CHECK)
    # --------------------------------------------------------------------------
    def build_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(14)

        title = QLabel("Tizim Sozlamalari, Uskunalar va RBAC Huquqlari", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        grid = QHBoxLayout()
        grid.setSpacing(16)

        # 1. Hardware Health Check Card
        hc_card = QFrame(page)
        hc_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 18px;")
        apply_card_shadow(hc_card)
        hc_box = QVBoxLayout(hc_card)

        hc_t = QLabel("Uskunalar Integratsiyasi & Datchiklar Holati", hc_card)
        hc_t.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        hc_box.addWidget(hc_t)

        hw = self.db.get_hardware_status()
        for k, v in hw.items():
            row = QHBoxLayout()
            r_k = QLabel(k.replace("_", " ").title() + ":", hc_card)
            r_k.setStyleSheet("color: #475569; font-weight: 600; font-size: 12px;")
            row.addWidget(r_k)
            row.addStretch()

            r_v = QLabel(v, hc_card)
            r_v.setStyleSheet("color: #166534; background: #dcfce7; padding: 2px 8px; border-radius: 8px; font-size: 11px; font-weight: 700;")
            row.addWidget(r_v)
            hc_box.addLayout(row)

        grid.addWidget(hc_card, stretch=5)

        # 2. Tariflar sozlamalari
        t_card = QFrame(page)
        t_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 18px;")
        apply_card_shadow(t_card)
        tb = QVBoxLayout(t_card)

        tb_t = QLabel("Tarif va Vaqt Parametrlari", t_card)
        tb_t.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        tb.addWidget(tb_t)

        tb.addWidget(QLabel("Kunduzgi soatlik stavka (so'm):"))
        self.in_day = QLineEdit(t_card)
        tb.addWidget(self.in_day)

        tb.addWidget(QLabel("Tungi soatlik stavka (so'm):"))
        self.in_night = QLineEdit(t_card)
        tb.addWidget(self.in_night)

        tb.addWidget(QLabel("Dastlabki bepul oraliq (daqiqa):"))
        self.in_grace = QLineEdit(t_card)
        tb.addWidget(self.in_grace)

        btn_save_tar = QPushButton("Saqlash", t_card)
        btn_save_tar.setIcon(get_icon("save.svg"))
        btn_save_tar.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 8px; border-radius: 6px;")
        btn_save_tar.clicked.connect(self.save_tariffs)
        tb.addWidget(btn_save_tar)

        grid.addWidget(t_card, stretch=5)
        layout.addLayout(grid)

        # 3. Xodimlar jadvali
        st_card = QFrame(page)
        st_card.setStyleSheet("background: #ffffff; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px; padding: 18px;")
        apply_card_shadow(st_card)
        st_box = QVBoxLayout(st_card)

        sth = QHBoxLayout()
        sth_t = QLabel("Administratorlar va Operatorlar (RBAC Huquqlari)", st_card)
        sth_t.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        sth.addWidget(sth_t)
        sth.addStretch()

        btn_add_st = QPushButton("Yangi Xodim Qo'shish", st_card)
        btn_add_st.setIcon(get_icon("plus.svg"))
        btn_add_st.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 6px 12px; border-radius: 6px;")
        btn_add_st.clicked.connect(self.add_staff_dialog)
        sth.addWidget(btn_add_st)
        st_box.addLayout(sth)

        self.table_staff = QTableWidget(st_card)
        self.table_staff.setColumnCount(5)
        self.table_staff.setHorizontalHeaderLabels(["ID", "F.I.SH", "LOGIN", "ROLI", "SMENA"])
        self.table_staff.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_staff.verticalHeader().setVisible(False)
        st_box.addWidget(self.table_staff)

        layout.addWidget(st_card)
        return page

    def save_tariffs(self):
        s = {
            "day_rate": self.in_day.text().strip(),
            "night_rate": self.in_night.text().strip(),
            "grace_period": self.in_grace.text().strip(),
        }
        self.db.save_settings(s)
        QMessageBox.information(self, "Muvaffaqiyat", "Tariflar saqlandi!")

    def add_staff_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Yangi Xodim Qo'shish")
        dlg.setFixedSize(360, 320)
        l = QVBoxLayout(dlg)

        in_n = QLineEdit(dlg)
        in_n.setPlaceholderText("To'liq Ism")
        l.addWidget(in_n)

        in_u = QLineEdit(dlg)
        in_u.setPlaceholderText("Login")
        l.addWidget(in_u)

        in_p = QLineEdit(dlg)
        in_p.setEchoMode(QLineEdit.EchoMode.Password)
        in_p.setPlaceholderText("Parol")
        l.addWidget(in_p)

        cb_r = QComboBox(dlg)
        cb_r.addItems(["OPERATOR", "ADMIN", "SUPER_ADMIN"])
        l.addWidget(cb_r)

        btn = QPushButton("Qo'shish", dlg)
        btn.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 8px;")

        def save():
            n = in_n.text().strip()
            u = in_u.text().strip()
            p = in_p.text().strip()
            r = cb_r.currentText()
            if n and u and p:
                if self.db.add_staff(u, p, n, r, "Smena 1"):
                    dlg.accept()
                    self.load_staff()

        btn.clicked.connect(save)
        l.addWidget(btn)
        dlg.exec()

    # --------------------------------------------------------------------------
    # DINAMIK YANGILASH TAYMERLARI VA MA'LUMOTLARNI YUKLASH
    # --------------------------------------------------------------------------
    def init_timers(self):
        # 1 soniyalik soat taymeri
        self.timer_clock = QTimer(self)
        self.timer_clock.timeout.connect(self.tick_clock)
        self.timer_clock.start(1000)
        self.tick_clock()

        # 5 soniyalik ma'lumotlar sinxronizatsiyasi
        self.timer_data = QTimer(self)
        self.timer_data.timeout.connect(self.refresh_all_data)
        self.timer_data.start(5000)

    def tick_clock(self):
        now = datetime.now()
        months = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
        m = months[now.month - 1]
        self.lbl_clock.setText(f"⏱ {now.strftime('%H:%M:%S')}  |  {now.day}-{m}, {now.year}")

    def refresh_all_data(self):
        # KPIlar
        stats = self.db.get_dashboard_stats()
        rev = stats.get("total_revenue", 0)
        free = stats.get("free_slots", 0)
        occ = stats.get("occupied_slots", 0)
        res = stats.get("reserved_slots", 0)
        total = free + occ + res or 1

        self.lbl_rev_val.setText(f"{rev:,} UZS".replace(",", " "))
        self.lbl_free_val.setText(f"{free} ta")
        self.lbl_occ_val.setText(f"{occ} ta")
        self.lbl_res_val.setText(f"{res} ta")

        pct = int((occ / total) * 100)
        self.bar_occ.setValue(pct)
        self.lbl_occ_pct.setText(f"Avtoturargoh bandlik darajasi: {pct}% ({occ} / {total} ta joy band)")

        # 3D Izometrik xaritalar
        slots1 = self.db.get_slots(floor=1)
        self.dash_iso_map.set_slots(slots1, floor=1)
        self.full_iso_map.set_slots(slots1, floor=self.full_iso_map.floor)

        # Jadvallarni yangilash
        self.load_feed_table()
        self.load_recent_table()
        self.load_active_sessions()
        self.load_access_list()
        self.load_finance()
        self.load_coupons()
        self.load_staff()
        self.load_settings()
        self.update_user_topbar()

    def load_feed_table(self):
        acts = self.db.get_recent_activities(limit=5)
        self.table_feed.setRowCount(len(acts))
        for r, a in enumerate(acts):
            self.table_feed.setItem(r, 0, QTableWidgetItem(a.get("session_code", "")))
            self.table_feed.setCellWidget(r, 1, create_plate_badge(a.get("vehicle_plate", "")))
            self.table_feed.setItem(r, 2, QTableWidgetItem(a.get("slot_number", "")))
            self.table_feed.setCellWidget(r, 3, create_status_badge(a.get("status", "ACTIVE")))

    def load_recent_table(self):
        acts = self.db.get_recent_activities(limit=8)
        self.table_recent.setRowCount(len(acts))
        for r, a in enumerate(acts):
            self.table_recent.setItem(r, 0, QTableWidgetItem(str(a.get("session_code", ""))))
            self.table_recent.setCellWidget(r, 1, create_plate_badge(a.get("vehicle_plate", "")))
            self.table_recent.setItem(r, 2, QTableWidgetItem(a.get("slot_number", "")))
            self.table_recent.setItem(r, 3, QTableWidgetItem(a.get("entry_time", "")))
            amt = a.get("total_amount", 15000)
            self.table_recent.setItem(r, 4, QTableWidgetItem(f"{amt:,} UZS".replace(",", " ")))
            self.table_recent.setCellWidget(r, 5, create_status_badge(a.get("status", "ACTIVE")))

    def load_active_sessions(self):
        sess = self.db.get_active_sessions()
        self._populate_sessions_table(sess)

    def _populate_sessions_table(self, sess):
        self.table_sessions.setRowCount(len(sess))
        for r, s in enumerate(sess):
            self.table_sessions.setItem(r, 0, QTableWidgetItem(s.get("session_code", "")))
            self.table_sessions.setCellWidget(r, 1, create_plate_badge(s.get("vehicle_plate", "")))
            self.table_sessions.setItem(r, 2, QTableWidgetItem(s.get("slot_number", "")))
            self.table_sessions.setItem(r, 3, QTableWidgetItem(s.get("entry_time", "")))
            # Jonli taymer simulyatsiyasi
            dur = f"01:{random.randint(10,59)}:{random.randint(10,59)}"
            self.table_sessions.setItem(r, 4, QTableWidgetItem(f"⏱ {dur}"))
            self.table_sessions.setCellWidget(r, 5, create_status_badge(s.get("status", "ACTIVE")))

    def load_access_list(self):
        items = self.db.get_access_list()
        self.table_access.setRowCount(len(items))
        for r, it in enumerate(items):
            self.table_access.setItem(r, 0, QTableWidgetItem(str(it["id"])))
            self.table_access.setCellWidget(r, 1, create_plate_badge(it["plate"]))
            self.table_access.setCellWidget(r, 2, create_status_badge(it["list_type"]))
            self.table_access.setItem(r, 3, QTableWidgetItem(it.get("note", "")))

            btn_del = QPushButton("O'chirish")
            btn_del.setStyleSheet("background: #fee2e2; color: #991b1b; border: none; border-radius: 4px; padding: 2px 6px;")
            btn_del.clicked.connect(lambda ch, item_id=it["id"]: self.delete_access(item_id))
            self.table_access.setCellWidget(r, 4, btn_del)

    def delete_access(self, iid):
        self.db.remove_from_access_list(iid)
        self.load_access_list()

    def load_finance(self):
        fin = self.db.get_financial_summary()
        self.lbl_pay_val.setText(f"{fin.get('payme_total', 0):,} UZS".replace(",", " "))
        self.lbl_clk_val.setText(f"{fin.get('click_total', 0):,} UZS".replace(",", " "))
        self.lbl_csh_val.setText(f"{fin.get('cash_total', 0):,} UZS".replace(",", " "))

    def load_coupons(self):
        cps = self.db.get_coupons()
        self.table_coupons.setRowCount(len(cps))
        for r, c in enumerate(cps):
            self.table_coupons.setItem(r, 0, QTableWidgetItem(c["code"]))
            self.table_coupons.setItem(r, 1, QTableWidgetItem(f"{c['discount_percent']}%"))
            self.table_coupons.setItem(r, 2, QTableWidgetItem(c.get("valid_until", "")))
            self.table_coupons.setCellWidget(r, 3, create_status_badge("ACTIVE" if c.get("is_active") else "NOFAOL"))

    def load_staff(self):
        st = self.db.get_all_staff()
        self.table_staff.setRowCount(len(st))
        for r, s in enumerate(st):
            self.table_staff.setItem(r, 0, QTableWidgetItem(str(s["id"])))
            self.table_staff.setItem(r, 1, QTableWidgetItem(s["full_name"]))
            self.table_staff.setItem(r, 2, QTableWidgetItem(s["username"]))
            self.table_staff.setItem(r, 3, QTableWidgetItem(s["role"]))
            self.table_staff.setItem(r, 4, QTableWidgetItem(s["shift"]))

    def load_settings(self):
        s = self.db.get_settings()
        if hasattr(self, 'in_day') and not self.in_day.text():
            self.in_day.setText(s.get("day_rate", "5000"))
            self.in_night.setText(s.get("night_rate", "3000"))
            self.in_grace.setText(s.get("grace_period", "15"))

    def simulate_car_entry(self):
        res = self.db.simulate_car_entry()
        if res:
            QMessageBox.information(
                self, "Yangi Avto Kirdi",
                f"Davlat raqami: <b>{res['plate']}</b><br>Biriktirilgan slot: <b>{res['slot']}</b><br>Vaqt: {res['time']}"
            )
            self.refresh_all_data()
        else:
            QMessageBox.warning(self, "Bo'sh joy yo'q", "Barcha avtoturargoh slotlari band!")


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    db = ParklyDatabase()
    login = LoginDialog(db)
    if login.exec():
        user = login.user_data
        window = MainWindow(db, user)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
