#include "LoginDialog.h"
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QFrame>
#include <QGraphicsDropShadowEffect>

LoginDialog::LoginDialog(QWidget *parent)
    : QDialog(parent), m_username(""), m_fullName(""), m_role("") {
    setWindowTitle("Parkly.uz — Tizimga Kirish");
    setFixedSize(760, 480);
    setWindowFlags(windowFlags() & ~Qt::WindowContextHelpButtonHint);
    setupUI();
}

void LoginDialog::setupUI() {
    QHBoxLayout *mainLayout = new QHBoxLayout(this);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);

    // ==========================================
    // 1. CHAP TOMON (BRANDING & ILLUSTRATION - Image 3 dagi kabi)
    // ==========================================
    QFrame *leftFrame = new QFrame(this);
    leftFrame->setFixedWidth(320);
    leftFrame->setStyleSheet(R"(
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f766e, stop:1 #115e59);
            border-top-left-radius: 12px;
            border-bottom-left-radius: 12px;
            color: white;
        }
    )");

    QVBoxLayout *leftLayout = new QVBoxLayout(leftFrame);
    leftLayout->setContentsMargins(35, 45, 35, 45);

    QPixmap logoPix("desktop_admin/assets/logo.png");
    if (logoPix.isNull()) {
        logoPix.load("assets/logo.png");
    }

    if (!logoPix.isNull()) {
        QLabel *logoImg = new QLabel(leftFrame);
        logoImg->setPixmap(logoPix.scaledToWidth(240, Qt::SmoothTransformation));
        logoImg->setAlignment(Qt::AlignCenter);
        leftLayout->addWidget(logoImg);
    } else {
        QLabel *logoLabel = new QLabel("🚗 <b>Parkly.uz</b>", leftFrame);
        logoLabel->setStyleSheet("font-size: 26px; color: #ffffff; font-weight: bold;");
        leftLayout->addWidget(logoLabel);
    }

    QLabel *subTitle = new QLabel("Aqlli Avtoturargoh Boshqaruv Tizimi", leftFrame);
    subTitle->setStyleSheet("font-size: 15px; font-weight: bold; color: #ccfbf1; margin-top: 15px;");
    subTitle->setAlignment(Qt::AlignCenter);

    QLabel *descLabel = new QLabel(
        "• Real-time ANPR kamera oqimi\n"
        "• 2D interaktiv slotlar xaritasi\n"
        "• Avtomatlashgan to'lov va shlagbaum\n"
        "• Super-Admin va 5 ta operator nazorati", leftFrame);
    descLabel->setStyleSheet("font-size: 11px; color: #99f6e4; line-height: 1.5; margin-top: 15px;");
    descLabel->setWordWrap(true);

    leftLayout->addWidget(logoLabel);
    leftLayout->addWidget(iconLabel);
    leftLayout->addWidget(subTitle);
    leftLayout->addWidget(descLabel);
    leftLayout->addStretch();

    QLabel *footerLeft = new QLabel("© 2026 Parkly Ekotizimi v1.0", leftFrame);
    footerLeft->setStyleSheet("font-size: 10px; color: #5eead4;");
    leftLayout->addWidget(footerLeft);

    // ==========================================
    // 2. O'NG TOMON (LOGIN FORMASI - Image 3 dagi kabi)
    // ==========================================
    QFrame *rightFrame = new QFrame(this);
    rightFrame->setStyleSheet("background-color: #ffffff; border-top-right-radius: 12px; border-bottom-right-radius: 12px;");

    QVBoxLayout *rightLayout = new QVBoxLayout(rightFrame);
    rightLayout->setContentsMargins(45, 45, 45, 45);
    rightLayout->setSpacing(14);

    QLabel *formTitle = new QLabel("PARKLY ADMIN", rightFrame);
    formTitle->setStyleSheet("font-size: 24px; font-weight: bold; color: #0d9488; letter-spacing: 1px;");

    QLabel *formSub = new QLabel("Tizimga kirish (Foydalanuvchi hisobi)", rightFrame);
    formSub->setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 10px;");

    QLabel *uLabel = new QLabel("Foydalanuvchi nomi yoki Email:", rightFrame);
    uLabel->setStyleSheet("font-size: 12px; font-weight: 600; color: #334155;");

    m_usernameEdit = new QLineEdit(rightFrame);
    m_usernameEdit->setPlaceholderText("admin yoki operator1");
    m_usernameEdit->setText("admin"); // Sinov uchun qulaylik
    m_usernameEdit->setStyleSheet(R"(
        QLineEdit {
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 13px;
            background-color: #f8fafc;
            color: #0f172a;
        }
        QLineEdit:focus {
            border: 2px solid #0d9488;
            background-color: #ffffff;
        }
    )");

    QLabel *pLabel = new QLabel("Maxfiy parol:", rightFrame);
    pLabel->setStyleSheet("font-size: 12px; font-weight: 600; color: #334155;");

    m_passwordEdit = new QLineEdit(rightFrame);
    m_passwordEdit->setEchoMode(QLineEdit::Password);
    m_passwordEdit->setPlaceholderText("••••••••");
    m_passwordEdit->setText("admin123"); // Sinov uchun qulaylik
    m_passwordEdit->setStyleSheet(R"(
        QLineEdit {
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 13px;
            background-color: #f8fafc;
            color: #0f172a;
        }
        QLineEdit:focus {
            border: 2px solid #0d9488;
            background-color: #ffffff;
        }
    )");

    m_rememberCheck = new QCheckBox("Meni tizimda eslab qol", rightFrame);
    m_rememberCheck->setChecked(true);
    m_rememberCheck->setStyleSheet("font-size: 12px; color: #64748b;");

    m_errorLabel = new QLabel("", rightFrame);
    m_errorLabel->setStyleSheet("color: #ef4444; font-size: 12px; font-weight: bold;");

    m_loginButton = new QPushButton("Tizimga Kirish", rightFrame);
    m_loginButton->setCursor(Qt::PointingHandCursor);
    m_loginButton->setStyleSheet(R"(
        QPushButton {
            background-color: #0d9488;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px;
            border: none;
        }
        QPushButton:hover {
            background-color: #0f766e;
        }
        QPushButton:pressed {
            background-color: #115e59;
        }
    )");
    connect(m_loginButton, &QPushButton::clicked, this, &LoginDialog::onLoginClicked);

    QLabel *hintLabel = new QLabel("🔑 Sinov: Super-Admin: <b>admin</b> / <b>admin123</b> | Operator: <b>operator1</b> / <b>operator123</b>", rightFrame);
    hintLabel->setStyleSheet("font-size: 10px; color: #94a3b8;");
    hintLabel->setWordWrap(true);

    rightLayout->addWidget(formTitle);
    rightLayout->addWidget(formSub);
    rightLayout->addWidget(uLabel);
    rightLayout->addWidget(m_usernameEdit);
    rightLayout->addWidget(pLabel);
    rightLayout->addWidget(m_passwordEdit);
    rightLayout->addWidget(m_rememberCheck);
    rightLayout->addWidget(m_errorLabel);
    rightLayout->addWidget(m_loginButton);
    rightLayout->addWidget(hintLabel);
    rightLayout->addStretch();

    mainLayout->addWidget(leftFrame);
    mainLayout->addWidget(rightFrame);
}

void LoginDialog::onLoginClicked() {
    QString u = m_usernameEdit->text().trimmed();
    QString p = m_passwordEdit->text().trimmed();

    if (u.isEmpty() || p.isEmpty()) {
        m_errorLabel->setText("⚠️ Foydalanuvchi nomi va parolni kiriting!");
        return;
    }

    // Rollar bo'yicha autentifikatsiya tekshiruvi:
    if (u == "admin" && p == "admin123") {
        m_username = "erjigitvv5";
        m_fullName = "Erjigit (Bosh Rahbar)";
        m_role = "SUPER_ADMIN";
        accept();
    } else if (u == "manager" && p == "manager123") {
        m_username = "sherzod_ali";
        m_fullName = "Sherzod Aliyev (Filial Admini)";
        m_role = "ADMIN";
        accept();
    } else if ((u == "operator1" || u == "operator") && p == "operator123") {
        m_username = "aziz_rustamov";
        m_fullName = "Aziz Rustamov (Smena 1)";
        m_role = "OPERATOR";
        accept();
    } else {
        m_errorLabel->setText("❌ Noto'g'ri login yoki parol kiritildi!");
    }
}
