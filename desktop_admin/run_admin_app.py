"""
Parkly.uz — Desktop Admin Panel (PyQt6 / Minimalistic Glassmorphism & 3D Isometric Engine)
100% Dinamik, Real SQLite/PostgreSQL bazasi bilan bog'langan.
Dizayn talablari:
1. Minimalistic Glassmorphism uslubi (yumshoq shaffof kartalar, nozik chegaralar).
2. Yuqori o'ng burchakda Notification (Xabarnomalar markazi) va Admin Profili (Avatar + Super Admin pill).
3. Admin profiliga bosganda Ism, Login va Parolni o'zgartirish modali.
4. Yashirin (Collapsible Drawer) Navigatsiya menyusi va [ ☰ Menyu ] ochish/yopish tugmasi.
5. Dinamik statistika ko'rsatkichlari (Trendlar, bandlik foizi, real vaqt sinxronizatsiyasi).
6. 3D Izometrik xarita (Bosh sahifada mini-preview va to'liq tabda interaktiv 3D avtoturargoh).
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
    QMessageBox, QGroupBox, QSpinBox, QProgressBar, QScrollArea, QToolButton
)
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QPen, QLinearGradient, QPixmap, QIcon, QCursor
)
from PyQt6.QtCore import Qt, QRect, QSize, QTimer, pyqtSignal

from db_manager import ParklyDatabase
from isometric_map import IsometricParkingMapWidget

# Aktivlar va SVG ikonkalari katalogi
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")


def get_icon(name: str) -> QIcon:
    """SVG ikonkani xavfsiz yuklab beruvchi yordamchi funksiya"""
    path = os.path.join(ICONS_DIR, name)
    if os.path.exists(path):
        return QIcon(path)
    return QIcon()


# ==============================================================================
# 1. TIZIMGA KIRISH OYNASI (LOGIN DIALOG)
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
                border-top-left-radius: 14px;
                border-bottom-left-radius: 14px;
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
        sub_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #ccfbf1; margin-top: 15px;")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_layout.addWidget(sub_lbl)

        desc = QLabel(
            "• Minimalistic Glassmorphism interfeys\n"
            "• 3D Izometrik avtoturargoh xaritasi\n"
            "• Real-time ANPR va shlagbaum nazorati\n"
            "• Xavfsiz xodimlar auditi va kassa hisoboti", left_frame
        )
        desc.setStyleSheet("font-size: 11px; color: #99f6e4; line-height: 1.6; margin-top: 15px;")
        l_layout.addWidget(desc)
        l_layout.addStretch()

        footer = QLabel("© 2026 Parkly Ekotizimi v2.0 (Glassmorphism)", left_frame)
        footer.setStyleSheet("font-size: 10px; color: #5eead4;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l_layout.addWidget(footer)

        main_layout.addWidget(left_frame)

        # O'ng qism (Oq minimalist kirish shakli)
        right_frame = QFrame(self)
        right_frame.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-top-right-radius: 14px;
                border-bottom-right-radius: 14px;
            }
        """)
        r_layout = QVBoxLayout(right_frame)
        r_layout.setContentsMargins(45, 40, 45, 40)
        r_layout.setSpacing(14)

        title = QLabel("Admin Panelga Kirish", right_frame)
        title.setStyleSheet("font-size: 22px; font-weight: 800; color: #0f172a;")
        r_layout.addWidget(title)

        subtitle = QLabel("Haqiqiy ma'lumotlar bazasi orqali avtorizatsiya", right_frame)
        subtitle.setStyleSheet("font-size: 12px; color: #64748b; margin-bottom: 8px;")
        r_layout.addWidget(subtitle)

        # Login
        lbl_user = QLabel("Foydalanuvchi nomi (Login):", right_frame)
        lbl_user.setStyleSheet("font-weight: 600; color: #334155; font-size: 12px;")
        r_layout.addWidget(lbl_user)

        self.input_user = QLineEdit(right_frame)
        self.input_user.setPlaceholderText("admin yoki manager")
        self.input_user.setText("admin")
        self.input_user.setStyleSheet("""
            QLineEdit {
                background: #f8fafc;
                border: 1.5px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #0f172a;
            }
            QLineEdit:focus { border: 1.5px solid #0d9488; background: #ffffff; }
        """)
        r_layout.addWidget(self.input_user)

        # Parol
        lbl_pass = QLabel("Maxfiy parol:", right_frame)
        lbl_pass.setStyleSheet("font-weight: 600; color: #334155; font-size: 12px;")
        r_layout.addWidget(lbl_pass)

        self.input_pass = QLineEdit(right_frame)
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setPlaceholderText("Parolni kiriting")
        self.input_pass.setText("admin123")
        self.input_pass.setStyleSheet("""
            QLineEdit {
                background: #f8fafc;
                border: 1.5px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #0f172a;
            }
            QLineEdit:focus { border: 1.5px solid #0d9488; background: #ffffff; }
        """)
        r_layout.addWidget(self.input_pass)

        # Kirish tugmasi
        self.btn_login = QPushButton("Tizimga Kirish", right_frame)
        self.btn_login.setIcon(get_icon("check.svg"))
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
                margin-top: 10px;
            }
            QPushButton:hover { background: #0f766e; }
            QPushButton:pressed { background: #115e59; }
        """)
        self.btn_login.clicked.connect(self.attempt_login)
        r_layout.addWidget(self.btn_login)

        hint = QLabel("Standart: admin / admin123 | manager / manager123", right_frame)
        hint.setStyleSheet("font-size: 11px; color: #94a3b8; margin-top: 6px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_layout.addWidget(hint)
        r_layout.addStretch()

        main_layout.addWidget(right_frame)

    def attempt_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Diqqat", "Iltimos, login va parolni to'ldiring!")
            return

        user = self.db.authenticate(username, password)
        if user:
            self.user_data = user
            self.accept()
        else:
            QMessageBox.critical(self, "Xatolik", "Login yoki parol noto'g'ri! Iltimos, qayta urinib ko'ring.")


# ==============================================================================
# 2. ADMIN PROFILI VA PAROL SOZLAMALARI MODALI (PROFILE DIALOG)
# ==============================================================================
class AdminProfileDialog(QDialog):
    """Admin profili, foydalanuvchi nomi va parolini sozlash oynasi"""
    def __init__(self, db: ParklyDatabase, current_user: dict, parent=None):
        super().__init__(parent)
        self.db = db
        self.current_user = current_user
        self.logout_requested = False
        self.setWindowTitle("Admin Profili va Xavfsizlik Sozlamalari")
        self.setFixedSize(480, 560)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background: #f8fafc;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)

        # Header card (Glassmorphic)
        header_card = QFrame(self)
        header_card.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 12px;
            }
        """)
        h_box = QHBoxLayout(header_card)

        # Avatar doirasi
        avatar = QLabel(self.current_user.get("full_name", "A")[0].upper(), header_card)
        avatar.setFixedSize(54, 54)
        avatar.setStyleSheet("""
            background: #0d9488;
            color: #ffffff;
            font-size: 22px;
            font-weight: 800;
            border-radius: 27px;
        """)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_box.addWidget(avatar)

        user_info = QVBoxLayout()
        name_lbl = QLabel(self.current_user.get("full_name", "Admin"), header_card)
        name_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0f172a;")
        user_info.addWidget(name_lbl)

        role_pill = QLabel(f"Roli: {self.current_user.get('role', 'SUPER_ADMIN')}", header_card)
        role_pill.setStyleSheet("""
            background: #ecfdf5;
            color: #059669;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
        """)
        user_info.addWidget(role_pill)
        h_box.addLayout(user_info)
        h_box.addStretch()
        layout.addWidget(header_card)

        # Form card
        form_card = QFrame(self)
        form_card.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 16px;
            }
            QLabel {
                font-weight: 600;
                color: #334155;
                font-size: 12px;
            }
            QLineEdit {
                background: #f8fafc;
                border: 1.5px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: #0f172a;
            }
            QLineEdit:focus {
                border: 1.5px solid #0d9488;
                background: #ffffff;
            }
        """)
        form_layout = QVBoxLayout(form_card)
        form_layout.setSpacing(10)

        # To'liq ism
        form_layout.addWidget(QLabel("To'liq Ism (F.I.Sh):"))
        self.in_fullname = QLineEdit(form_card)
        self.in_fullname.setText(self.current_user.get("full_name", ""))
        form_layout.addWidget(self.in_fullname)

        # Username
        form_layout.addWidget(QLabel("Foydalanuvchi nomi (Login):"))
        self.in_username = QLineEdit(form_card)
        self.in_username.setText(self.current_user.get("username", ""))
        form_layout.addWidget(self.in_username)

        # Hozirgi parol
        form_layout.addWidget(QLabel("Hozirgi parol (Tasdiqlash uchun):"))
        self.in_curr_pass = QLineEdit(form_card)
        self.in_curr_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.in_curr_pass.setPlaceholderText("Joriy parolni kiriting")
        form_layout.addWidget(self.in_curr_pass)

        # Yangi parol
        form_layout.addWidget(QLabel("Yangi parol (O'zgartirmaslik uchun bo'sh qoldiring):"))
        self.in_new_pass = QLineEdit(form_card)
        self.in_new_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.in_new_pass.setPlaceholderText("Yangi maxfiy parol")
        form_layout.addWidget(self.in_new_pass)

        # Yangi parolni takrorlash
        form_layout.addWidget(QLabel("Yangi parolni takrorlang:"))
        self.in_conf_pass = QLineEdit(form_card)
        self.in_conf_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.in_conf_pass.setPlaceholderText("Takrorlang")
        form_layout.addWidget(self.in_conf_pass)

        layout.addWidget(form_card)

        # Tugmalar
        btn_box = QHBoxLayout()

        self.btn_save = QPushButton("Saqlash", self)
        self.btn_save.setIcon(get_icon("save.svg"))
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background: #0d9488;
                color: white;
                font-weight: 700;
                padding: 10px 18px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background: #0f766e; }
        """)
        self.btn_save.clicked.connect(self.save_profile)
        btn_box.addWidget(self.btn_save)

        self.btn_logout = QPushButton("Tizimdan Chiqish", self)
        self.btn_logout.setIcon(get_icon("logout.svg"))
        self.btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background: #fef2f2;
                color: #ef4444;
                border: 1px solid #fecaca;
                font-weight: 700;
                padding: 10px 16px;
                border-radius: 8px;
            }
            QPushButton:hover { background: #fee2e2; }
        """)
        self.btn_logout.clicked.connect(self.request_logout)
        btn_box.addWidget(self.btn_logout)

        btn_cancel = QPushButton("Bekor qilish", self)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: #e2e8f0;
                color: #334155;
                font-weight: 600;
                padding: 10px 16px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background: #cbd5e1; }
        """)
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_cancel)

        layout.addLayout(btn_box)

    def save_profile(self):
        new_name = self.in_fullname.text().strip()
        new_user = self.in_username.text().strip()
        curr_pass = self.in_curr_pass.text().strip()
        new_p = self.in_new_pass.text().strip()
        conf_p = self.in_conf_pass.text().strip()

        if not new_name or not new_user:
            QMessageBox.warning(self, "Xatolik", "Ism va login bo'sh bo'lishi mumkin emas!")
            return

        if not curr_pass:
            QMessageBox.warning(self, "Diqqat", "O'zgarishlarni tasdiqlash uchun hozirgi parolingizni kiriting!")
            return

        if new_p:
            if new_p != conf_p:
                QMessageBox.warning(self, "Xatolik", "Yangi parol va tasdiqlovchi parol bir-biriga mos kelmadi!")
                return
            if len(new_p) < 4:
                QMessageBox.warning(self, "Xatolik", "Yangi parol kamida 4 ta belgidan iborat bo'lishi kerak!")
                return

        uid = self.current_user["id"]
        success, msg = self.db.update_user_profile(
            uid, new_name, new_user,
            current_password=curr_pass,
            new_password=new_p if new_p else None
        )

        if success:
            self.current_user["full_name"] = new_name
            self.current_user["username"] = new_user
            QMessageBox.information(self, "Muvaffaqiyat", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Rad etildi", msg)

    def request_logout(self):
        confirm = QMessageBox.question(
            self, "Tizimdan chiqish", "Haqiqatan ham hisobdan chiqmoqchimisiz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.logout_requested = True
            self.accept()


# ==============================================================================
# 3. XABARNOMALAR MARKAZI (NOTIFICATIONS DIALOG)
# ==============================================================================
class NotificationDialog(QDialog):
    """Yuqori o'ng burchakdagi bildirishnomalar oynasi"""
    def __init__(self, db: ParklyDatabase, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Tizim Bildirishnomalari (Real-time)")
        self.setFixedSize(480, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("QDialog { background: #f8fafc; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("Xabarnomalar Markazi", self)
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0f172a;")
        header.addWidget(title)
        header.addStretch()

        btn_mark = QPushButton("Barchasini o'qilgan qilish", self)
        btn_mark.setIcon(get_icon("check.svg"))
        btn_mark.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_mark.setStyleSheet("""
            QPushButton {
                background: #ecfdf5;
                color: #059669;
                border: 1px solid #a7f3d0;
                font-weight: 600;
                padding: 5px 10px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover { background: #d1fae5; }
        """)
        btn_mark.clicked.connect(self.mark_all_read)
        header.addWidget(btn_mark)
        layout.addLayout(header)

        # Xabarlar ro'yxati (Scroll Area)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: 1px solid #e2e8f0; border-radius: 10px; background: #ffffff; }")

        content_widget = QWidget()
        self.items_layout = QVBoxLayout(content_widget)
        self.items_layout.setContentsMargins(10, 10, 10, 10)
        self.items_layout.setSpacing(8)

        self.load_notifications()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        btn_close = QPushButton("Yopish", self)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #0d9488;
                color: white;
                font-weight: 700;
                padding: 8px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background: #0f766e; }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def load_notifications(self):
        # Tozalash
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        notifs = self.db.get_notifications(limit=20)
        if not notifs:
            empty_lbl = QLabel("Hozircha hech qanday bildirishnoma yo'q", self)
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet("color: #94a3b8; font-size: 13px; margin: 30px;")
            self.items_layout.addWidget(empty_lbl)
            return

        for n in notifs:
            card = QFrame()
            is_read = n.get("is_read", 0)
            bg = "#ffffff" if is_read else "#f0fdfa"
            border = "#e2e8f0" if is_read else "#99f6e4"
            card.setStyleSheet(f"""
                QFrame {{
                    background: {bg};
                    border: 1px solid {border};
                    border-radius: 8px;
                    padding: 8px;
                }}
            """)
            c_box = QVBoxLayout(card)
            c_box.setSpacing(3)

            top_row = QHBoxLayout()
            t_lbl = QLabel(n.get("title", "Xabarnoma"), card)
            t_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #0f172a;")
            top_row.addWidget(t_lbl)
            top_row.addStretch()

            time_lbl = QLabel(str(n.get("created_at", "")).split()[-1], card)
            time_lbl.setStyleSheet("font-size: 10px; color: #94a3b8;")
            top_row.addWidget(time_lbl)
            c_box.addLayout(top_row)

            m_lbl = QLabel(n.get("message", ""), card)
            m_lbl.setStyleSheet("font-size: 11px; color: #475569;")
            m_lbl.setWordWrap(True)
            c_box.addWidget(m_lbl)

            self.items_layout.addWidget(card)

        self.items_layout.addStretch()

    def mark_all_read(self):
        self.db.mark_all_notifications_read()
        self.load_notifications()


# ==============================================================================
# 4. SLOTNI O'ZGARTIRISH MODALI (SLOT EDIT DIALOG)
# ==============================================================================
class SlotEditDialog(QDialog):
    def __init__(self, slot_data: dict, db: ParklyDatabase, parent=None):
        super().__init__(parent)
        self.slot_data = slot_data
        self.db = db
        self.setWindowTitle(f"Slotni Boshqarish: {slot_data.get('slot_number')}")
        self.setFixedSize(400, 360)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("QDialog { background: #ffffff; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel(f"Slot {self.slot_data.get('slot_number')} ({self.slot_data.get('floor')}-Qavat)", self)
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Holatni tanlang:"))
        self.combo_status = QComboBox(self)
        self.combo_status.addItems(["FREE (Bo'sh)", "OCCUPIED (Band)", "RESERVED (Bron)", "MAINTENANCE (Ta'mirlash)"])
        cur_st = self.slot_data.get("status", "FREE")
        idx_map = {"FREE": 0, "OCCUPIED": 1, "RESERVED": 2, "MAINTENANCE": 3}
        self.combo_status.setCurrentIndex(idx_map.get(cur_st, 0))
        layout.addWidget(self.combo_status)

        layout.addWidget(QLabel("Avtomobil davlat raqami (agar band bo'lsa):"))
        self.input_plate = QLineEdit(self)
        self.input_plate.setText(self.slot_data.get("current_vehicle_plate") or "")
        self.input_plate.setPlaceholderText("01 A 777 AA")
        layout.addWidget(self.input_plate)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Saqlash", self)
        btn_save.setIcon(get_icon("save.svg"))
        btn_save.setStyleSheet("background: #0d9488; color: white; padding: 10px; font-weight: 700; border-radius: 6px;")
        btn_save.clicked.connect(self.save_slot)
        btn_box.addWidget(btn_save)

        btn_cancel = QPushButton("Bekor qilish", self)
        btn_cancel.setStyleSheet("background: #e2e8f0; color: #334155; padding: 10px; border-radius: 6px;")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_cancel)

        layout.addLayout(btn_box)

    def save_slot(self):
        st_text = self.combo_status.currentText().split()[0]
        plate = self.input_plate.text().strip()
        if st_text == "FREE":
            plate = None

        s_num = self.slot_data.get("slot_number")
        self.db.update_slot_status(s_num, st_text, plate)
        QMessageBox.information(self, "Muvaffaqiyat", f"Slot {s_num} holati muvaffaqiyatli yangilandi!")
        self.accept()


# ==============================================================================
# 5. ASOSIY DASTUR OYNASI (MAIN WINDOW — GLASSMORPHISM & COLLAPSIBLE DRAWER)
# ==============================================================================
class MainWindow(QMainWindow):
    def __init__(self, db: ParklyDatabase, user_data: dict):
        super().__init__()
        self.db = db
        self.user_data = user_data

        self.setWindowTitle("Parkly.uz — Aqlli Avtoturargoh Boshqaruv Paneli (Minimalistic Glassmorphism)")
        self.resize(1340, 840)
        self.setMinimumSize(1100, 700)

        self.setup_ui()
        self.init_timers()
        self.refresh_all_data()

    def setup_ui(self):
        # Markaziy vidjet
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Global Glassmorphism Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8fafc, stop:0.5 #f1f5f9, stop:1 #e2e8f0);
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }
            QFrame.glassCard {
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid rgba(255, 255, 255, 0.9);
                border-radius: 16px;
            }
            QLabel {
                color: #0f172a;
            }
            QTableWidget {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                gridline-color: #f1f5f9;
                selection-background-color: #ccfbf1;
                selection-color: #0f766e;
                font-size: 12px;
            }
            QHeaderView::section {
                background: #f8fafc;
                color: #475569;
                font-weight: 700;
                font-size: 11px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                padding: 10px;
            }
        """)

        # Asosiy vertikal tartib
        root_layout = QVBoxLayout(self.central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ----------------------------------------------------------------------
        # A. YUQORI TOP-BAR (LOGO, MENU TUGMASI, NOTIFICATION VA ADMIN PROFILI)
        # ----------------------------------------------------------------------
        self.top_bar = QFrame(self.central_widget)
        self.top_bar.setFixedHeight(68)
        self.top_bar.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.85);
                border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            }
        """)
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(20, 0, 24, 0)
        top_layout.setSpacing(14)

        # 1. Menyu ochish tugmasi (Hamburger Menu)
        self.btn_toggle_menu = QPushButton(self.top_bar)
        self.btn_toggle_menu.setIcon(get_icon("menu.svg"))
        self.btn_toggle_menu.setIconSize(QSize(22, 22))
        self.btn_toggle_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle_menu.setToolTip("Navigatsiya menyusini ochish / yopish")
        self.btn_toggle_menu.setStyleSheet("""
            QPushButton {
                background: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 12px;
            }
            QPushButton:hover { background: #e2e8f0; }
        """)
        self.btn_toggle_menu.clicked.connect(self.toggle_drawer)
        top_layout.addWidget(self.btn_toggle_menu)

        # 2. Logo
        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        pix = QPixmap(logo_path)
        logo_lbl = QLabel(self.top_bar)
        if not pix.isNull():
            logo_lbl.setPixmap(pix.scaledToHeight(36, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_lbl.setText("PARKLY.UZ")
            logo_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #0d9488;")
        top_layout.addWidget(logo_lbl)

        # Joriy sahifa sarlavhasi
        self.page_title_lbl = QLabel("Bosh Sahifa", self.top_bar)
        self.page_title_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #64748b; margin-left: 10px;")
        top_layout.addWidget(self.page_title_lbl)

        top_layout.addStretch()

        # 3. Dinamik soat va sana pilli
        self.clock_pill = QLabel(self.top_bar)
        self.clock_pill.setStyleSheet("""
            background: #f8fafc;
            color: #475569;
            font-size: 11px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
        """)
        top_layout.addWidget(self.clock_pill)

        # 4. Notification Bell tugmasi (Qizil unread badge bilan)
        self.btn_notif = QPushButton(self.top_bar)
        self.btn_notif.setIcon(get_icon("bell.svg"))
        self.btn_notif.setIconSize(QSize(20, 20))
        self.btn_notif.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_notif.setToolTip("Xabarnomalar markazi")
        self.btn_notif.setStyleSheet("""
            QPushButton {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 7px 12px;
                font-weight: 700;
                color: #ef4444;
                font-size: 11px;
            }
            QPushButton:hover { background: #fee2e2; border-color: #fca5a5; }
        """)
        self.btn_notif.clicked.connect(self.open_notifications)
        top_layout.addWidget(self.btn_notif)

        # 5. Admin Profili pilli (Avatar + Ism + Super Admin pill)
        self.btn_profile = QPushButton(self.top_bar)
        self.btn_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_profile.setToolTip("Profil va parolni sozlash uchun bosing")
        self.btn_profile.setStyleSheet("""
            QPushButton {
                background: #f8fafc;
                border: 1.5px solid #e2e8f0;
                border-radius: 20px;
                padding: 4px 14px;
                text-align: left;
            }
            QPushButton:hover {
                background: #ffffff;
                border-color: #0d9488;
            }
        """)
        self.btn_profile.clicked.connect(self.open_admin_profile)
        top_layout.addWidget(self.btn_profile)

        self.update_top_bar_user_ui()
        root_layout.addWidget(self.top_bar)

        # ----------------------------------------------------------------------
        # B. ASOSIY MAYDON (YASHIRIN DRAWER VA SAHIFALAR STACKI)
        # ----------------------------------------------------------------------
        content_box = QHBoxLayout()
        content_box.setContentsMargins(0, 0, 0, 0)
        content_box.setSpacing(0)

        # 1. YASHIRIN COLLAPSIBLE DRAWER (NAVIGATION MENU)
        self.drawer = QFrame(self.central_widget)
        self.drawer.setFixedWidth(240)
        self.drawer.setVisible(False)  # Boshlang'ich holatda yashirilgan!
        self.drawer.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.94);
                border-right: 1px solid rgba(226, 232, 240, 0.9);
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
        d_layout.setSpacing(6)

        # Drawer header (Yopish tugmasi)
        dh_box = QHBoxLayout()
        dh_box.setContentsMargins(16, 0, 12, 10)
        dh_lbl = QLabel("NAVIGATSIYA", self.drawer)
        dh_lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94a3b8; letter-spacing: 1px;")
        dh_box.addWidget(dh_lbl)
        dh_box.addStretch()

        btn_close_drawer = QPushButton(self.drawer)
        btn_close_drawer.setIcon(get_icon("close.svg"))
        btn_close_drawer.setFixedSize(28, 28)
        btn_close_drawer.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close_drawer.setStyleSheet("background: transparent; border-radius: 14px; padding: 2px;")
        btn_close_drawer.clicked.connect(self.toggle_drawer)
        dh_box.addWidget(btn_close_drawer)
        d_layout.addLayout(dh_box)

        # Menyu tugmalari
        self.nav_btns = []
        nav_items = [
            ("Bosh Sahifa", "dashboard.svg", 0),
            ("3D Izometrik Xarita", "map.svg", 1),
            ("Kameralar (ANPR)", "camera.svg", 2),
            ("Xodimlar (RBAC)", "users.svg", 3),
            ("Moliya & Kassa", "wallet.svg", 4),
            ("Tizim Sozlamalari", "settings.svg", 5),
        ]

        for text, icon, idx in nav_items:
            b = QPushButton(f"  {text}", self.drawer)
            b.setIcon(get_icon(icon))
            b.setIconSize(QSize(18, 18))
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda ch, i=idx, t=text: self.navigate_to(i, t))
            self.nav_btns.append(b)
            d_layout.addWidget(b)

        self.nav_btns[0].setChecked(True)
        d_layout.addStretch()

        # Chiqish tugmasi pastda
        btn_drawer_logout = QPushButton("  Tizimdan Chiqish", self.drawer)
        btn_drawer_logout.setIcon(get_icon("logout.svg"))
        btn_drawer_logout.setStyleSheet("color: #ef4444; font-weight: 700;")
        btn_drawer_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_drawer_logout.clicked.connect(self.logout_user)
        d_layout.addWidget(btn_drawer_logout)

        content_box.addWidget(self.drawer)

        # 2. SAHIFALAR STACKI (QStackedWidget)
        self.stack = QStackedWidget(self.central_widget)
        self.stack.addWidget(self.create_dashboard_page())       # 0: Bosh sahifa
        self.stack.addWidget(self.create_isometric_map_page())   # 1: 3D Izometrik xarita
        self.stack.addWidget(self.create_cameras_page())          # 2: Kameralar
        self.stack.addWidget(self.create_staff_page())            # 3: Xodimlar
        self.stack.addWidget(self.create_finance_page())          # 4: Moliya
        self.stack.addWidget(self.create_settings_page())         # 5: Sozlamalar

        content_box.addWidget(self.stack)
        root_layout.addLayout(content_box)

    def toggle_drawer(self):
        """Menyuni ochish yoki yashirish"""
        self.drawer.setVisible(not self.drawer.isVisible())

    def update_top_bar_user_ui(self):
        """Top bar'dagi foydalanuvchi ma'lumotlarini yangilash"""
        name = self.user_data.get("full_name", "Admin")
        role = self.user_data.get("role", "SUPER_ADMIN")
        initial = name[0].upper() if name else "A"

        self.btn_profile.setText(f"  {initial}  |  {name}  ({role})  ▾")
        self.btn_profile.setIcon(get_icon("user.svg"))

        # O'qilmagan xabarnomalar soni
        unread = self.db.get_unread_notifications_count()
        if unread > 0:
            self.btn_notif.setText(f" {unread}")
            self.btn_notif.setStyleSheet("""
                QPushButton {
                    background: #fef2f2;
                    border: 1px solid #fca5a5;
                    border-radius: 18px;
                    padding: 5px 12px;
                    font-weight: 800;
                    color: #ef4444;
                    font-size: 11px;
                }
                QPushButton:hover { background: #fee2e2; }
            """)
        else:
            self.btn_notif.setText("")
            self.btn_notif.setStyleSheet("""
                QPushButton {
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 18px;
                    padding: 5px 10px;
                    color: #64748b;
                }
                QPushButton:hover { background: #f1f5f9; }
            """)

    def open_notifications(self):
        dlg = NotificationDialog(self.db, self)
        dlg.exec()
        self.update_top_bar_user_ui()

    def open_admin_profile(self):
        dlg = AdminProfileDialog(self.db, self.user_data, self)
        if dlg.exec():
            if dlg.logout_requested:
                self.logout_user()
            else:
                self.update_top_bar_user_ui()

    def logout_user(self):
        self.close()
        # Qayta login oynasini ochish
        new_login = LoginDialog(self.db)
        if new_login.exec():
            self.user_data = new_login.user_data
            self.update_top_bar_user_ui()
            self.show()

    def navigate_to(self, index, title):
        for i, b in enumerate(self.nav_btns):
            b.setChecked(i == index)
        self.stack.setCurrentIndex(index)
        self.page_title_lbl.setText(title)

    # --------------------------------------------------------------------------
    # 1. BOSH SAHIFA (DASHBOARD — GLASSMORPHISM & DYNAMIC STATS & MINI 3D PREVIEW)
    # --------------------------------------------------------------------------
    def create_dashboard_page(self):
        page = QWidget()
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(20)

        # 1. Xush kelibsiz banneri (Glassmorphism Banner)
        welcome_card = QFrame(inner)
        welcome_card.setProperty("class", "glassCard")
        welcome_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.95);
                border-radius: 16px;
                padding: 16px 20px;
            }
        """)
        w_box = QHBoxLayout(welcome_card)

        w_left = QVBoxLayout()
        self.w_title = QLabel(f"Xayrli kun, {self.user_data.get('full_name')}!", welcome_card)
        self.w_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        w_left.addWidget(self.w_title)

        w_sub = QLabel("Parkly.uz — Real-vaqt holati, dinamik statistika va 3D avtoturargoh nazorati.", welcome_card)
        w_sub.setStyleSheet("font-size: 12px; color: #64748b; margin-top: 2px;")
        w_left.addWidget(w_sub)
        w_box.addLayout(w_left)
        w_box.addStretch()

        # Tezkor simulyatsiya tugmasi
        btn_sim_car = QPushButton("Avto Kiritish (Simulyatsiya)", welcome_card)
        btn_sim_car.setIcon(get_icon("car.svg"))
        btn_sim_car.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sim_car.setStyleSheet("""
            QPushButton {
                background: #0d9488;
                color: white;
                font-size: 13px;
                font-weight: 700;
                padding: 10px 18px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background: #0f766e; }
        """)
        btn_sim_car.clicked.connect(self.simulate_entry)
        w_box.addWidget(btn_sim_car)
        layout.addWidget(welcome_card)

        # 2. Dinamik KPI Kartalari (4 ta Glassmorphism blok)
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(16)

        self.kpi_rev = self._create_kpi_card("Bugungi Tushum", "0 UZS", "trending_up.svg", "+14.2% bugun", "#0d9488", is_primary=True)
        self.kpi_free = self._create_kpi_card("Bo'sh Joylar", "0 ta", "car.svg", "Ochiq", "#10b981")
        self.kpi_occ = self._create_kpi_card("Band Joylar", "0 ta", "lock.svg", "Band", "#ef4444")
        self.kpi_res = self._create_kpi_card("Faol Bronlar", "0 ta", "star.svg", "Zaxira", "#f59e0b")

        kpi_grid.addWidget(self.kpi_rev, 0, 0)
        kpi_grid.addWidget(self.kpi_free, 0, 1)
        kpi_grid.addWidget(self.kpi_occ, 0, 2)
        kpi_grid.addWidget(self.kpi_res, 0, 3)
        layout.addLayout(kpi_grid)

        # Bandlik foizi progress bar
        occ_bar_card = QFrame(inner)
        occ_bar_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(255, 255, 255, 0.9);
                border-radius: 12px;
                padding: 10px 16px;
            }
        """)
        ob_box = QVBoxLayout(occ_bar_card)
        self.occ_lbl = QLabel("Avtoturargoh bandlik darajasi: Hisoblanmoqda...", occ_bar_card)
        self.occ_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #334155;")
        ob_box.addWidget(self.occ_lbl)

        self.occ_bar = QProgressBar(occ_bar_card)
        self.occ_bar.setFixedHeight(10)
        self.occ_bar.setTextVisible(False)
        self.occ_bar.setStyleSheet("""
            QProgressBar {
                background: #e2e8f0;
                border-radius: 5px;
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:0.7 #f59e0b, stop:1 #ef4444);
                border-radius: 5px;
            }
        """)
        ob_box.addWidget(self.occ_bar)
        layout.addWidget(occ_bar_card)

        # 3. Ikki ustunli qism: Mini 3D Izometrik xarita va So'nggi amallar
        mid_layout = QHBoxLayout()
        mid_layout.setSpacing(16)

        # Chap: Mini 3D Izometrik Xarita (Live Preview)
        iso_card = QFrame(inner)
        iso_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.95);
                border-radius: 16px;
                padding: 14px;
            }
        """)
        iso_box = QVBoxLayout(iso_card)
        iso_head = QHBoxLayout()
        iso_title = QLabel("3D Izometrik Xarita (Real-Vaqt)", iso_card)
        iso_title.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        iso_head.addWidget(iso_title)
        iso_head.addStretch()

        btn_go_map = QPushButton("To'liq Xarita ➔", iso_card)
        btn_go_map.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_go_map.setStyleSheet("color: #0d9488; font-weight: 700; border: none; font-size: 12px;")
        btn_go_map.clicked.connect(lambda: self.navigate_to(1, "3D Izometrik Xarita"))
        iso_head.addWidget(btn_go_map)
        iso_box.addLayout(iso_head)

        self.mini_iso_map = IsometricParkingMapWidget(iso_card, is_mini=True)
        self.mini_iso_map.slot_clicked.connect(self.on_slot_clicked)
        iso_box.addWidget(self.mini_iso_map)
        mid_layout.addWidget(iso_card, stretch=5)

        # O'ng: So'nggi amallar jadvali
        table_card = QFrame(inner)
        table_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.95);
                border-radius: 16px;
                padding: 14px;
            }
        """)
        t_box = QVBoxLayout(table_card)
        th_box = QHBoxLayout()
        t_title = QLabel("So'nggi Harakatlar (Baza)", table_card)
        t_title.setStyleSheet("font-size: 14px; font-weight: 800; color: #0f172a;")
        th_box.addWidget(t_title)
        th_box.addStretch()

        btn_ref = QPushButton("Yangilash", table_card)
        btn_ref.setIcon(get_icon("refresh.svg"))
        btn_ref.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ref.setStyleSheet("color: #0d9488; font-weight: 700; border: none; font-size: 12px;")
        btn_ref.clicked.connect(self.refresh_all_data)
        th_box.addWidget(btn_ref)
        t_box.addLayout(th_box)

        self.table_recent = QTableWidget(table_card)
        self.table_recent.setColumnCount(4)
        self.table_recent.setHorizontalHeaderLabels(["Seans", "Raqam", "Slot", "Holat"])
        self.table_recent.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_recent.verticalHeader().setVisible(False)
        t_box.addWidget(self.table_recent)
        mid_layout.addWidget(table_card, stretch=6)

        layout.addLayout(mid_layout)

        scroll.setWidget(inner)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        return page

    def _create_kpi_card(self, title, val_text, icon_name, trend_text, accent_color, is_primary=False):
        card = QFrame()
        card.setFixedHeight(120)
        if is_primary:
            card.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f766e, stop:1 #115e59);
                    border-radius: 16px;
                    padding: 14px;
                }
            """)
            txt_color = "#ffffff"
            title_color = "#ccfbf1"
        else:
            card.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.85);
                    border: 1px solid rgba(255, 255, 255, 0.95);
                    border-radius: 16px;
                    padding: 14px;
                }
            """)
            txt_color = "#0f172a"
            title_color = "#64748b"

        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(10, 10, 10, 10)

        top = QHBoxLayout()
        t_lbl = QLabel(title, card)
        t_lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {title_color};")
        top.addWidget(t_lbl)
        top.addStretch()

        trend = QLabel(trend_text, card)
        trend.setStyleSheet(f"""
            font-size: 10px; font-weight: 700;
            color: {accent_color if not is_primary else '#5eead4'};
            background: {'rgba(255,255,255,0.15)' if is_primary else '#f1f5f9'};
            padding: 3px 8px; border-radius: 8px;
        """)
        top.addWidget(trend)
        c_layout.addLayout(top)

        val_lbl = QLabel(val_text, card)
        val_lbl.setObjectName("val")
        val_lbl.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {txt_color}; margin-top: 4px;")
        c_layout.addWidget(val_lbl)

        return card

    # --------------------------------------------------------------------------
    # 2. 3D IZOMETRIK XARITA SAHIFASI (ISOMETRIC 3D MAP TAB)
    # --------------------------------------------------------------------------
    def create_isometric_map_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(14)

        # Yuqori boshqaruv paneli
        top_bar = QFrame(page)
        top_bar.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.95);
                border-radius: 14px;
                padding: 10px 16px;
            }
        """)
        tb_box = QHBoxLayout(top_bar)

        # Qavatni almashtirish tugmalari
        self.btn_fl1 = QPushButton("1-Qavat (Asosiy Maydon)", top_bar)
        self.btn_fl1.setCheckable(True)
        self.btn_fl1.setChecked(True)
        self.btn_fl1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fl1.setStyleSheet("""
            QPushButton {
                background: #f1f5f9; color: #334155; font-weight: 700; padding: 8px 16px; border-radius: 8px; border: none;
            }
            QPushButton:checked { background: #0d9488; color: white; }
        """)
        self.btn_fl1.clicked.connect(lambda: self.switch_floor(1))
        tb_box.addWidget(self.btn_fl1)

        self.btn_fl2 = QPushButton("2-Qavat (Yuqori / Zaxira)", top_bar)
        self.btn_fl2.setCheckable(True)
        self.btn_fl2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fl2.setStyleSheet("""
            QPushButton {
                background: #f1f5f9; color: #334155; font-weight: 700; padding: 8px 16px; border-radius: 8px; border: none;
            }
            QPushButton:checked { background: #0d9488; color: white; }
        """)
        self.btn_fl2.clicked.connect(lambda: self.switch_floor(2))
        tb_box.addWidget(self.btn_fl2)

        tb_box.addStretch()

        btn_sim = QPushButton("Avto Kiritish", top_bar)
        btn_sim.setIcon(get_icon("car.svg"))
        btn_sim.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sim.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 8px 14px; border-radius: 8px;")
        btn_sim.clicked.connect(self.simulate_entry)
        tb_box.addWidget(btn_sim)

        btn_ref = QPushButton("Yangilash", top_bar)
        btn_ref.setIcon(get_icon("refresh.svg"))
        btn_ref.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ref.setStyleSheet("background: #f1f5f9; color: #334155; font-weight: 600; padding: 8px 14px; border-radius: 8px;")
        btn_ref.clicked.connect(self.refresh_all_data)
        tb_box.addWidget(btn_ref)

        layout.addWidget(top_bar)

        # Asosiy 3D Izometrik xarita vidjeti
        self.full_iso_map = IsometricParkingMapWidget(page, is_mini=False)
        self.full_iso_map.slot_clicked.connect(self.on_slot_clicked)
        layout.addWidget(self.full_iso_map, stretch=1)

        return page

    def switch_floor(self, floor):
        self.btn_fl1.setChecked(floor == 1)
        self.btn_fl2.setChecked(floor == 2)
        slots = self.db.get_slots(floor=floor)
        self.full_iso_map.set_slots(slots, floor=floor)

    def on_slot_clicked(self, slot_data):
        dlg = SlotEditDialog(slot_data, self.db, self)
        if dlg.exec():
            self.refresh_all_data()

    # --------------------------------------------------------------------------
    # 3. KAMERALAR (ANPR) SAHIFASI
    # --------------------------------------------------------------------------
    def create_cameras_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(16)

        title = QLabel("Universal Kameralar Oqimi & ANPR Nazorati", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(16)

        # Kamera 1: Kirish
        cam1 = self._create_cam_card("Kamera #1 — Kirish Darvozasi (ANPR Faol)", "01 A 777 AA", "99.4%", "Avtomatik ochildi")
        grid.addWidget(cam1, 0, 0)

        # Kamera 2: Chiqish
        cam2 = self._create_cam_card("Kamera #2 — Chiqish Shlagbaumi (Kassa)", "10 123 BBA", "98.7%", "To'lov kutilyapti")
        grid.addWidget(cam2, 0, 1)

        layout.addLayout(grid)

        # Shlagbaumni qo'lda ochish kartasi
        override_card = QFrame(page)
        override_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.95);
                border-radius: 14px;
                padding: 16px;
            }
        """)
        ob_box = QHBoxLayout(override_card)
        ob_info = QVBoxLayout()
        ob_title = QLabel("Favqulodda Shlagbaumni Qo'lda Ochish (Operator Auditi)", override_card)
        ob_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #0f172a;")
        ob_info.addWidget(ob_title)
        ob_sub = QLabel("Barcha qo'lda ochish holatlari operator ismi va sababi bilan bazada saqlanadi.", override_card)
        ob_sub.setStyleSheet("font-size: 11px; color: #64748b;")
        ob_info.addWidget(ob_sub)
        ob_box.addLayout(ob_info)
        ob_box.addStretch()

        btn_open_barrier = QPushButton("Shlagbaumni Ochish", override_card)
        btn_open_barrier.setIcon(get_icon("barrier.svg"))
        btn_open_barrier.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open_barrier.setStyleSheet("background: #ef4444; color: white; font-weight: 700; padding: 10px 18px; border-radius: 8px;")
        btn_open_barrier.clicked.connect(self.manual_barrier_override)
        ob_box.addWidget(btn_open_barrier)

        layout.addWidget(override_card)
        layout.addStretch()
        return page

    def _create_cam_card(self, title, plate, conf, status):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #0f172a;
                border-radius: 14px;
                padding: 14px;
            }
        """)
        box = QVBoxLayout(card)

        head = QHBoxLayout()
        t_lbl = QLabel(title, card)
        t_lbl.setStyleSheet("color: white; font-size: 13px; font-weight: 700;")
        head.addWidget(t_lbl)
        head.addStretch()

        rec_dot = QLabel("● REC 30 FPS", card)
        rec_dot.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 11px;")
        head.addWidget(rec_dot)
        box.addLayout(head)

        # Video simulyatsiya ekrani
        screen = QLabel(card)
        screen.setFixedHeight(220)
        screen.setStyleSheet("""
            background: #1e293b;
            border: 1px dashed #334155;
            border-radius: 10px;
        """)
        screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        screen.setText(f"[ ANPR KADR: {plate} ]\nCLAHE Kontrast: Faol | Homography: To'g'rilangan")
        box.addWidget(screen)

        footer = QHBoxLayout()
        f_lbl = QLabel(f"Oxirgi o'qilgan raqam: <b>{plate}</b> (Aniqlik: {conf})", card)
        f_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        footer.addWidget(f_lbl)
        footer.addStretch()

        st_lbl = QLabel(status, card)
        st_lbl.setStyleSheet("color: #10b981; font-weight: bold; font-size: 11px;")
        footer.addWidget(st_lbl)
        box.addLayout(footer)

        return card

    def manual_barrier_override(self):
        uname = self.user_data.get("username", "admin")
        name = self.user_data.get("full_name", "Operator")
        self.db.log_barrier_override(uname, name, "Operator paneli orqali qo'lda ochildi")
        QMessageBox.information(self, "Shlagbaum", "Shlagbaum muvaffaqiyatli ochildi va audit bazasiga qayd etildi!")
        self.update_top_bar_user_ui()

    # --------------------------------------------------------------------------
    # 4. XODIMLAR (RBAC) SAHIFASI
    # --------------------------------------------------------------------------
    def create_staff_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(14)

        top = QHBoxLayout()
        title = QLabel("Xodimlar va Huquqlar Boshqaruvi (RBAC)", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        top.addWidget(title)
        top.addStretch()

        btn_add = QPushButton("Yangi Xodim Qo'shish", page)
        btn_add.setIcon(get_icon("plus.svg"))
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 8px 16px; border-radius: 8px;")
        btn_add.clicked.connect(self.add_staff_dialog)
        top.addWidget(btn_add)
        layout.addLayout(top)

        self.table_staff = QTableWidget(page)
        self.table_staff.setColumnCount(5)
        self.table_staff.setHorizontalHeaderLabels(["ID", "F.I.Sh", "Login", "Roli", "Smena"])
        self.table_staff.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_staff.verticalHeader().setVisible(False)
        layout.addWidget(self.table_staff)

        return page

    def add_staff_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Yangi Xodim Qo'shish")
        dlg.setFixedSize(380, 400)
        l = QVBoxLayout(dlg)
        l.setContentsMargins(20, 20, 20, 20)

        in_name = QLineEdit(dlg)
        in_name.setPlaceholderText("To'liq Ism (F.I.Sh)")
        l.addWidget(in_name)

        in_user = QLineEdit(dlg)
        in_user.setPlaceholderText("Login (username)")
        l.addWidget(in_user)

        in_pass = QLineEdit(dlg)
        in_pass.setEchoMode(QLineEdit.EchoMode.Password)
        in_pass.setPlaceholderText("Parol")
        l.addWidget(in_pass)

        cb_role = QComboBox(dlg)
        cb_role.addItems(["OPERATOR", "ADMIN", "SUPER_ADMIN"])
        l.addWidget(cb_role)

        in_shift = QLineEdit(dlg)
        in_shift.setPlaceholderText("Smena (masalan: Smena 1 (08:00 - 16:00))")
        in_shift.setText("Smena 1")
        l.addWidget(in_shift)

        btn_save = QPushButton("Qo'shish", dlg)
        btn_save.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 10px; border-radius: 6px;")

        def save():
            name = in_name.text().strip()
            user = in_user.text().strip()
            pw = in_pass.text().strip()
            role = cb_role.currentText()
            shift = in_shift.text().strip()

            if not name or not user or not pw:
                QMessageBox.warning(dlg, "Xatolik", "Barcha maydonlarni to'ldiring!")
                return

            res = self.db.add_staff(user, pw, name, role, shift)
            if res:
                QMessageBox.information(dlg, "Muvaffaqiyat", "Yangi xodim muvaffaqiyatli qo'shildi!")
                dlg.accept()
                self.load_staff_table()
            else:
                QMessageBox.critical(dlg, "Xatolik", "Bunday loginli xodim allaqachon mavjud!")

        btn_save.clicked.connect(save)
        l.addWidget(btn_save)
        dlg.exec()

    # --------------------------------------------------------------------------
    # 5. MOLIYA & KASSA SAHIFASI
    # --------------------------------------------------------------------------
    def create_finance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(14)

        title = QLabel("Moliya va To'lovlar Nazorati (Real-time Tranzaksiyalar)", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        grid = QGridLayout()
        self.kpi_payme = self._create_kpi_card("Payme Tushumi", "0 UZS", "wallet.svg", "Elektron", "#0d9488")
        self.kpi_click = self._create_kpi_card("Click Tushumi", "0 UZS", "wallet.svg", "Elektron", "#0284c7")
        self.kpi_cash = self._create_kpi_card("Naqd To'lovlar", "0 UZS", "wallet.svg", "Kassa", "#10b981")
        grid.addWidget(self.kpi_payme, 0, 0)
        grid.addWidget(self.kpi_click, 0, 1)
        grid.addWidget(self.kpi_cash, 0, 2)
        layout.addLayout(grid)

        # Tranzaksiyalar jadvali
        self.table_tx = QTableWidget(page)
        self.table_tx.setColumnCount(6)
        self.table_tx.setHorizontalHeaderLabels(["Kod", "Seans", "Raqam", "To'lov Turi", "Summa", "Fiskal Belgi"])
        self.table_tx.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_tx.verticalHeader().setVisible(False)
        layout.addWidget(self.table_tx)

        return page

    # --------------------------------------------------------------------------
    # 6. SOZLAMALAR SAHIFASI
    # --------------------------------------------------------------------------
    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 20, 28, 24)
        layout.setSpacing(16)

        title = QLabel("Avtoturargoh Tizim Sozlamalari (Tariflar va Qoidalar)", page)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0f172a;")
        layout.addWidget(title)

        card = QFrame(page)
        card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.95);
                border-radius: 14px;
                padding: 20px;
            }
            QLabel { font-weight: 600; color: #334155; }
            QLineEdit {
                background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 8px 12px;
            }
        """)
        f_layout = QVBoxLayout(card)
        f_layout.setSpacing(12)

        f_layout.addWidget(QLabel("Kunduzgi soatlik tarif (08:00 - 20:00, so'm):"))
        self.set_day = QLineEdit(card)
        f_layout.addWidget(self.set_day)

        f_layout.addWidget(QLabel("Tungi soatlik tarif (20:00 - 08:00, so'm):"))
        self.set_night = QLineEdit(card)
        f_layout.addWidget(self.set_night)

        f_layout.addWidget(QLabel("Dastlabki bepul oraliq (daqiqa):"))
        self.set_grace = QLineEdit(card)
        f_layout.addWidget(self.set_grace)

        f_layout.addWidget(QLabel("Kunlik maksimal to'lov (so'm):"))
        self.set_cap = QLineEdit(card)
        f_layout.addWidget(self.set_cap)

        btn_save = QPushButton("Sozlamalarni Saqlash", card)
        btn_save.setIcon(get_icon("save.svg"))
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("background: #0d9488; color: white; font-weight: 700; padding: 10px 20px; border-radius: 8px; margin-top: 10px;")
        btn_save.clicked.connect(self.save_settings_data)
        f_layout.addWidget(btn_save)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def save_settings_data(self):
        settings_dict = {
            "day_rate": self.set_day.text().strip(),
            "night_rate": self.set_night.text().strip(),
            "grace_period": self.set_grace.text().strip(),
            "daily_cap": self.set_cap.text().strip(),
        }
        self.db.save_settings(settings_dict)
        QMessageBox.information(self, "Muvaffaqiyat", "Barcha tarif va sozlamalar bazada saqlandi!")

    # --------------------------------------------------------------------------
    # DINAMIK YANGILASH VA REAL-TIME SINXRONIZATSIYA
    # --------------------------------------------------------------------------
    def init_timers(self):
        # 1 soniyalik soat taymeri
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

        # 5 soniyalik ma'lumotlar yangilanish taymeri
        self.data_timer = QTimer(self)
        self.data_timer.timeout.connect(self.refresh_all_data)
        self.data_timer.start(5000)

    def update_clock(self):
        now = datetime.now()
        uz_months = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
        m_name = uz_months[now.month - 1]
        self.clock_pill.setText(f"⏱ {now.strftime('%H:%M:%S')}  |  {now.day}-{m_name}, {now.year}")

    def refresh_all_data(self):
        """Barcha ma'lumotlarni bazadan olib dinamik yangilash"""
        stats = self.db.get_dashboard_stats()

        # KPI qiymatlarini yangilash
        rev = stats.get("total_revenue", 0)
        free = stats.get("free_slots", 0)
        occ = stats.get("occupied_slots", 0)
        res = stats.get("reserved_slots", 0)
        total = free + occ + res or 1

        self.kpi_rev.findChild(QLabel, "val").setText(f"{rev:,} UZS".replace(",", " "))
        self.kpi_free.findChild(QLabel, "val").setText(f"{free} ta")
        self.kpi_occ.findChild(QLabel, "val").setText(f"{occ} ta")
        self.kpi_res.findChild(QLabel, "val").setText(f"{res} ta")

        # Bandlik foizi
        pct = int((occ / total) * 100)
        self.occ_bar.setValue(pct)
        self.occ_lbl.setText(f"Avtoturargoh bandlik darajasi: {pct}% ({occ} / {total} ta joy band)")

        # 3D Izometrik xaritalarni yangilash
        slots_fl1 = self.db.get_slots(floor=1)
        self.mini_iso_map.set_slots(slots_fl1, floor=1)
        self.full_iso_map.set_slots(slots_fl1, floor=self.full_iso_map.floor)

        # Jadval ma'lumotlarini yuklash
        self.load_recent_activities()
        self.load_staff_table()
        self.load_finance_data()
        self.load_settings_into_inputs()
        self.update_top_bar_user_ui()

    def load_recent_activities(self):
        acts = self.db.get_recent_activities(limit=6)
        self.table_recent.setRowCount(len(acts))
        for r, a in enumerate(acts):
            self.table_recent.setItem(r, 0, QTableWidgetItem(a.get("session_code", "")))
            self.table_recent.setItem(r, 1, QTableWidgetItem(a.get("vehicle_plate", "")))
            self.table_recent.setItem(r, 2, QTableWidgetItem(a.get("slot_number", "")))
            self.table_recent.setItem(r, 3, QTableWidgetItem(a.get("status", "")))

    def load_staff_table(self):
        staff = self.db.get_all_staff()
        self.table_staff.setRowCount(len(staff))
        for r, s in enumerate(staff):
            self.table_staff.setItem(r, 0, QTableWidgetItem(str(s.get("id"))))
            self.table_staff.setItem(r, 1, QTableWidgetItem(s.get("full_name", "")))
            self.table_staff.setItem(r, 2, QTableWidgetItem(s.get("username", "")))
            self.table_staff.setItem(r, 3, QTableWidgetItem(s.get("role", "")))
            self.table_staff.setItem(r, 4, QTableWidgetItem(s.get("shift", "")))

    def load_finance_data(self):
        fin = self.db.get_financial_summary()
        self.kpi_payme.findChild(QLabel, "val").setText(f"{fin.get('payme_total', 0):,} UZS".replace(",", " "))
        self.kpi_click.findChild(QLabel, "val").setText(f"{fin.get('click_total', 0):,} UZS".replace(",", " "))
        self.kpi_cash.findChild(QLabel, "val").setText(f"{fin.get('cash_total', 0):,} UZS".replace(",", " "))

        txs = fin.get("transactions", [])
        self.table_tx.setRowCount(len(txs))
        for r, t in enumerate(txs):
            self.table_tx.setItem(r, 0, QTableWidgetItem(t.get("tx_code", "")))
            self.table_tx.setItem(r, 1, QTableWidgetItem(t.get("session_code", "")))
            self.table_tx.setItem(r, 2, QTableWidgetItem(t.get("vehicle_plate", "")))
            self.table_tx.setItem(r, 3, QTableWidgetItem(t.get("provider", "")))
            self.table_tx.setItem(r, 4, QTableWidgetItem(f"{t.get('amount', 0):,} UZS".replace(",", " ")))
            self.table_tx.setItem(r, 5, QTableWidgetItem(t.get("fiscal_sign", "")))

    def load_settings_into_inputs(self):
        s = self.db.get_settings()
        if hasattr(self, 'set_day'):
            if not self.set_day.text():
                self.set_day.setText(s.get("day_rate", "5000"))
            if not self.set_night.text():
                self.set_night.setText(s.get("night_rate", "3000"))
            if not self.set_grace.text():
                self.set_grace.setText(s.get("grace_period", "15"))
            if not self.set_cap.text():
                self.set_cap.setText(s.get("daily_cap", "50000"))

    def simulate_entry(self):
        res = self.db.simulate_car_entry()
        if res:
            QMessageBox.information(
                self, "Yangi Avto Kirdi",
                f"Avtomobil: <b>{res['plate']}</b><br>Biriktirilgan joy: <b>{res['slot']}</b><br>Vaqt: {res['time']}"
            )
            self.refresh_all_data()
        else:
            QMessageBox.warning(self, "Bo'sh joy yo'q", "Barcha avtoturargoh joylari band!")


# ==============================================================================
# 6. ASOSIY ISHGA TUSHIRISH (MAIN ENTRY POINT)
# ==============================================================================
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # DB obyektini ishga tushirish
    db = ParklyDatabase()

    # Login dialogini ochish
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
