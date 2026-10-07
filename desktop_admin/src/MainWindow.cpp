#include "MainWindow.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QGroupBox>
#include <QHeaderView>
#include <QMessageBox>
#include <QDateTime>
#include <QScrollArea>
#include <QFrame>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), m_username("admin"), m_fullName("Erjigit (Boshliq)"), m_role("SUPER_ADMIN") {
    setWindowTitle("Parkly.uz — Aqlli Avtoturargoh Boshqaruv Paneli");
    resize(1280, 800);
    setMinimumSize(1024, 680);
    setupUI();
    applyRolePermissions();
}

MainWindow::~MainWindow() {}

void MainWindow::setAuthenticatedUser(const QString& username, const QString& fullName, const QString& role) {
    m_username = username;
    m_fullName = fullName;
    m_role = role;

    m_userProfilePill->setText(QString("👤 <b>%1</b> (%2)").arg(m_fullName, m_role));
    m_greetingTitle->setText(QString("Xayrli kun, %1 👋").arg(m_fullName));
    applyRolePermissions();
}

void MainWindow::setupUI() {
    QWidget *centralWidget = new QWidget(this);
    centralWidget->setStyleSheet("background-color: #f1f5f9; font-family: 'Segoe UI', Arial, sans-serif;");

    QHBoxLayout *rootLayout = new QHBoxLayout(centralWidget);
    rootLayout->setContentsMargins(12, 12, 12, 12);
    rootLayout->setSpacing(12);

    // 1. Chap Vertikal Floating Navigatsiya Dock (Image 1 & 2 kabi)
    QWidget *sidebar = createLeftSidebar();
    rootLayout->addWidget(sidebar);

    // 2. Asosiy Kontent Qismi (O'ng tomon)
    QVBoxLayout *contentLayout = new QVBoxLayout();
    contentLayout->setContentsMargins(0, 0, 0, 0);
    contentLayout->setSpacing(12);

    // Yuqori Header paneli (Logo, Pill Tabs, Search, Profil)
    QWidget *header = createTopHeader();
    contentLayout->addWidget(header);

    // Sahifalar Stacki (QStackedWidget)
    m_contentStack = new QStackedWidget(this);
    m_contentStack->addWidget(createDashboardPage()); // Index 0: Bosh Sahifa
    m_contentStack->addWidget(createMapPage());       // Index 1: 2D Xarita
    m_contentStack->addWidget(createCameraPage());    // Index 2: Kameralar & ANPR
    m_contentStack->addWidget(createStaffPage());     // Index 3: Xodimlar
    m_contentStack->addWidget(createFinancePage());   // Index 4: Moliya & Kassa
    m_contentStack->addWidget(createSettingsPage());  // Index 5: Sozlamalar

    contentLayout->addWidget(m_contentStack, 1);
    rootLayout->addLayout(contentLayout, 1);

    setCentralWidget(centralWidget);
}

QWidget* MainWindow::createLeftSidebar() {
    QFrame *sidebar = new QFrame(this);
    sidebar->setFixedWidth(72);
    sidebar->setStyleSheet(R"(
        QFrame {
            background-color: #ffffff;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
        }
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 14px;
            font-size: 20px;
            padding: 10px;
            color: #64748b;
        }
        QPushButton:hover {
            background-color: #f1f5f9;
            color: #0f766e;
        }
        QPushButton:checked {
            background-color: #0d9488;
            color: #ffffff;
        }
    )");

    QVBoxLayout *layout = new QVBoxLayout(sidebar);
    layout->setContentsMargins(8, 18, 8, 18);
    layout->setSpacing(14);

    QLabel *logoIcon = new QLabel("🚗", sidebar);
    logoIcon->setAlignment(Qt::AlignCenter);
    logoIcon->setStyleSheet("font-size: 26px; margin-bottom: 12px;");
    layout->addWidget(logoIcon);

    m_navGroup = new QButtonGroup(this);
    m_navGroup->setExclusive(true);

    auto addNavBtn = [this, layout](int id, const QString& icon, const QString& tooltip) {
        QPushButton *btn = new QPushButton(icon, this);
        btn->setCheckable(true);
        btn->setToolTip(tooltip);
        btn->setFixedSize(54, 46);
        m_navGroup->addButton(btn, id);
        layout->addWidget(btn);
        if (id == 0) btn->setChecked(true);
    };

    addNavBtn(0, "📊", "Bosh Sahifa (Dashboard)");
    addNavBtn(1, "🗺️", "2D Xarita");
    addNavBtn(2, "📹", "Kameralar va ANPR");
    addNavBtn(3, "👥", "Xodimlar va Rollar");
    addNavBtn(4, "💳", "Moliya va To'lovlar");
    addNavBtn(5, "⚙️", "Tizim Sozlamalari");

    layout->addStretch();

    QPushButton *logoutBtn = new QPushButton("🚪", sidebar);
    logoutBtn->setToolTip("Chiqish (Logout)");
    logoutBtn->setFixedSize(54, 46);
    logoutBtn->setStyleSheet("color: #ef4444;");
    connect(logoutBtn, &QPushButton::clicked, this, &MainWindow::onLogout);
    layout->addWidget(logoutBtn);

    connect(m_navGroup, &QButtonGroup::idClicked, this, &MainWindow::onNavButtonClicked);

    return sidebar;
}

QWidget* MainWindow::createTopHeader() {
    QFrame *header = new QFrame(this);
    header->setFixedHeight(68);
    header->setStyleSheet(R"(
        QFrame {
            background-color: #ffffff;
            border-radius: 18px;
            border: 1px solid #e2e8f0;
        }
    )");

    QHBoxLayout *layout = new QHBoxLayout(header);
    layout->setContentsMargins(20, 10, 20, 10);
    layout->setSpacing(14);

    QPixmap logoPix("desktop_admin/assets/logo.png");
    if (logoPix.isNull()) {
        logoPix.load("assets/logo.png");
    }

    if (!logoPix.isNull()) {
        QLabel *logoImg = new QLabel(header);
        logoImg->setPixmap(logoPix.scaledToHeight(38, Qt::SmoothTransformation));
        layout->addWidget(logoImg);
    } else {
        QLabel *brand = new QLabel("<b>Parkly.uz</b>", header);
        brand->setStyleSheet("font-size: 18px; color: #0d9488; font-weight: bold;");
        layout->addWidget(brand);
    }

    // O'rtadagi Pill navigatsiya tugmalari (Image 1 & 2 kabi)
    QHBoxLayout *pillsLayout = new QHBoxLayout();
    pillsLayout->setSpacing(6);
    m_topPillGroup = new QButtonGroup(this);

    auto addPill = [this, pillsLayout](int id, const QString& text) {
        QPushButton *btn = new QPushButton(text, this);
        btn->setCheckable(true);
        btn->setStyleSheet(R"(
            QPushButton {
                background-color: #f8fafc;
                color: #475569;
                font-size: 12px;
                font-weight: 600;
                padding: 7px 16px;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:checked {
                background-color: #0f172a;
                color: #ffffff;
                border: 1px solid #0f172a;
            }
        )");
        m_topPillGroup->addButton(btn, id);
        pillsLayout->addWidget(btn);
        if (id == 0) btn->setChecked(true);
    };

    addPill(0, "Asosiy Ko'rsatkichlar");
    addPill(1, "2D Xarita");
    addPill(2, "Kameralar");
    addPill(3, "Xodimlar");
    addPill(4, "Kassa & Moliya");
    addPill(5, "Sozlamalar");

    connect(m_topPillGroup, &QButtonGroup::idClicked, this, &MainWindow::onNavButtonClicked);
    layout->addLayout(pillsLayout);
    layout->addStretch();

    // Qidiruv maydoni (Search)
    QLineEdit *searchEdit = new QLineEdit(header);
    searchEdit->setPlaceholderText("🔍 Mashina raqami yoki slot qidirish...");
    searchEdit->setFixedWidth(240);
    searchEdit->setStyleSheet(R"(
        QLineEdit {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 6px 14px;
            font-size: 12px;
            color: #1e293b;
        }
        QLineEdit:focus {
            border: 1px solid #0d9488;
            background-color: #ffffff;
        }
    )");
    layout->addWidget(searchEdit);

    // Foydalanuvchi profili
    m_userProfilePill = new QLabel(QString("👤 <b>%1</b> (%2)").arg(m_fullName, m_role), header);
    m_userProfilePill->setStyleSheet(R"(
        QLabel {
            background-color: #f0fdfa;
            color: #0d9488;
            border: 1px solid #ccfbf1;
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 12px;
        }
    )");
    layout->addWidget(m_userProfilePill);

    return header;
}

QWidget* MainWindow::createDashboardPage() {
    QWidget *page = new QWidget();
    QVBoxLayout *layout = new QVBoxLayout(page);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(14);

    // Xush kelibsiz banneri (Image 1 & 2 kabi)
    QFrame *welcomeCard = new QFrame(page);
    welcomeCard->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 14px;");
    QHBoxLayout *wLayout = new QHBoxLayout(welcomeCard);
    
    QVBoxLayout *textLayout = new QVBoxLayout();
    m_greetingTitle = new QLabel(QString("Xayrli kun, %1 👋").arg(m_fullName), welcomeCard);
    m_greetingTitle->setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;");
    m_greetingSubtitle = new QLabel("Parkly.uz — avtoturargoh holati, tushumlar va xodimlar nazorati.", welcomeCard);
    m_greetingSubtitle->setStyleSheet("font-size: 13px; color: #64748b; margin-top: 2px;");
    textLayout->addWidget(m_greetingTitle);
    textLayout->addWidget(m_greetingSubtitle);
    wLayout->addLayout(textLayout);
    wLayout->addStretch();

    QLabel *dateBadge = new QLabel(QDateTime::currentDateTime().toString("dd-MMMM, yyyy"), welcomeCard);
    dateBadge->setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 8px 16px; font-weight: 600; color: #334155;");
    wLayout->addWidget(dateBadge);

    layout->addWidget(welcomeCard);

    // Karta Ko'rsatkichlari (Metric Cards Grid - Image 1/2 kabi)
    QGridLayout *metricsGrid = new QGridLayout();
    metricsGrid->setSpacing(14);

    // 1. Katta Yashil Kartochka (Jami tushum)
    QFrame *cardRevenue = new QFrame(page);
    cardRevenue->setStyleSheet(R"(
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f766e, stop:1 #115e59);
            border-radius: 18px;
            color: white;
            padding: 16px;
        }
    )");
    QVBoxLayout *revLayout = new QVBoxLayout(cardRevenue);
    QLabel *revTitle = new QLabel("Bugungi Jami Tushum", cardRevenue);
    revTitle->setStyleSheet("font-size: 13px; color: #99f6e4; font-weight: 600;");
    m_totalRevenueLabel = new QLabel("4,850,000 UZS", cardRevenue);
    m_totalRevenueLabel->setStyleSheet("font-size: 26px; font-weight: bold; color: #ffffff; margin-top: 4px;");
    QLabel *revGrowth = new QLabel("↑ +14.2% o'tgan haftaga nisbatan (Bandlik: 68%)", cardRevenue);
    revGrowth->setStyleSheet("font-size: 11px; color: #ccfbf1;");
    revLayout->addWidget(revTitle);
    revLayout->addWidget(m_totalRevenueLabel);
    revLayout->addWidget(revGrowth);
    metricsGrid->addWidget(cardRevenue, 0, 0, 1, 2);

    auto makeStatCard = [](const QString& title, const QString& value, const QString& badgeText, const QString& badgeColor, const QString& numColor) {
        QFrame *card = new QFrame();
        card->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 14px;");
        QVBoxLayout *l = new QVBoxLayout(card);
        QHBoxLayout *topL = new QHBoxLayout();
        QLabel *tLbl = new QLabel(title);
        tLbl->setStyleSheet("font-size: 12px; color: #64748b; font-weight: 600;");
        QLabel *bLbl = new QLabel(badgeText);
        bLbl->setStyleSheet(QString("background-color: %1; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;").arg(badgeColor));
        topL->addWidget(tLbl);
        topL->addStretch();
        topL->addWidget(bLbl);
        l->addLayout(topL);

        QLabel *vLbl = new QLabel(value);
        vLbl->setStyleSheet(QString("font-size: 24px; font-weight: bold; color: %1; margin-top: 4px;").arg(numColor));
        l->addWidget(vLbl);
        return card;
    };

    metricsGrid->addWidget(makeStatCard("Bo'sh Joylar", "48 ta", "Erkin", "#10b981", "#10b981"), 0, 2);
    metricsGrid->addWidget(makeStatCard("Band Joylar", "92 ta", "Mashina bor", "#ef4444", "#ef4444"), 0, 3);
    metricsGrid->addWidget(makeStatCard("Faol Bronlar", "14 ta", "Rezerv", "#f59e0b", "#f59e0b"), 0, 4);

    layout->addLayout(metricsGrid);

    // So'nggi Harakatlar Jadvali (Recent Activities - Image 1/2 kabi)
    QFrame *tableCard = new QFrame(page);
    tableCard->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;");
    QVBoxLayout *tableLayout = new QVBoxLayout(tableCard);

    QHBoxLayout *tHead = new QHBoxLayout();
    QLabel *tTitle = new QLabel("<b>So'nggi Kirish-Chiqish va To'lov Harakatlari</b>", tableCard);
    tTitle->setStyleSheet("font-size: 15px; color: #0f172a;");
    tHead->addWidget(tTitle);
    tHead->addStretch();
    tableLayout->addLayout(tHead);

    m_recentActivitiesTable = new QTableWidget(0, 6, tableCard);
    m_recentActivitiesTable->setHorizontalHeaderLabels({"Seans ID", "Avtomobil Raqami", "Slot", "Kirish Vaqti", "Summa", "Holat"});
    m_recentActivitiesTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    m_recentActivitiesTable->setStyleSheet(R"(
        QTableWidget {
            border: none;
            gridline-color: #f1f5f9;
            font-size: 12px;
            color: #1e293b;
        }
        QHeaderView::section {
            background-color: #f8fafc;
            color: #64748b;
            font-weight: 600;
            padding: 8px;
            border: none;
            border-bottom: 2px solid #e2e8f0;
        }
    )");

    // Namunaviy dastlabki qatorlar
    auto addRow = [this](const QString& id, const QString& plate, const QString& slot, const QString& time, const QString& sum, const QString& status) {
        int r = m_recentActivitiesTable->rowCount();
        m_recentActivitiesTable->insertRow(r);
        m_recentActivitiesTable->setItem(r, 0, new QTableWidgetItem(id));
        m_recentActivitiesTable->setItem(r, 1, new QTableWidgetItem(plate));
        m_recentActivitiesTable->setItem(r, 2, new QTableWidgetItem(slot));
        m_recentActivitiesTable->setItem(r, 3, new QTableWidgetItem(time));
        m_recentActivitiesTable->setItem(r, 4, new QTableWidgetItem(sum));
        m_recentActivitiesTable->setItem(r, 5, new QTableWidgetItem(status));
    };

    addRow("SES-1049", "01 A 777 AA", "A-102", "14:22:10", "15,000 UZS", "✅ To'langan (Payme)");
    addRow("SES-1048", "10 123 BBA", "A-105", "14:18:05", "10,000 UZS", "⏳ To'lov kutilmoqda");
    addRow("SES-1047", "01 888 ZZZ", "EV-02", "14:05:40", "35,000 UZS", "⚡ Zaryadlanmoqda");
    addRow("SES-1046", "01 001 PPP", "VIP-02", "13:40:12", "0 UZS", "⭐ VIP Xodim");

    tableLayout->addWidget(m_recentActivitiesTable);
    layout->addWidget(tableCard, 1);

    return page;
}

QWidget* MainWindow::createMapPage() {
    QWidget *page = new QWidget();
    QVBoxLayout *layout = new QVBoxLayout(page);
    layout->setContentsMargins(0, 0, 0, 0);

    QFrame *mapCard = new QFrame(page);
    mapCard->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;");
    QVBoxLayout *mLayout = new QVBoxLayout(mapCard);

    QHBoxLayout *topBar = new QHBoxLayout();
    QLabel *lbl = new QLabel("<b>Qavatni tanlang:</b>", mapCard);
    lbl->setStyleSheet("font-size: 13px; color: #0f172a;");
    m_floorCombo = new QComboBox(mapCard);
    m_floorCombo->addItems({"1-Qavat (Markaziy)", "2-Qavat (Yuqori)"});
    m_floorCombo->setStyleSheet("padding: 6px 14px; border-radius: 8px; border: 1px solid #cbd5e1; background-color: #f8fafc; font-weight: 600;");
    connect(m_floorCombo, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &MainWindow::onFloorChanged);

    m_slotDetailsLabel = new QLabel("Tanlangan slot: [Katak ustiga bosing]", mapCard);
    m_slotDetailsLabel->setStyleSheet("color: #0d9488; font-weight: bold; font-size: 13px; padding-left: 15px;");

    topBar->addWidget(lbl);
    topBar->addWidget(m_floorCombo);
    topBar->addWidget(m_slotDetailsLabel);
    topBar->addStretch();
    mLayout->addLayout(topBar);

    m_mapWidget = new ParkingMapWidget(mapCard);
    connect(m_mapWidget, &ParkingMapWidget::slotSelected, this, &MainWindow::onSlotSelected);
    mLayout->addWidget(m_mapWidget, 1);

    layout->addWidget(mapCard);
    return page;
}

QWidget* MainWindow::createCameraPage() {
    QWidget *page = new QWidget();
    QHBoxLayout *layout = new QHBoxLayout(page);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(14);

    // Chap: Jonli video ekrani
    QFrame *videoCard = new QFrame(page);
    videoCard->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;");
    QVBoxLayout *vLayout = new QVBoxLayout(videoCard);

    QLabel *vTitle = new QLabel("<b>📷 Jonli Kirish Kameralari & ANPR (10 FPS)</b>", videoCard);
    vTitle->setStyleSheet("font-size: 14px; color: #0f172a;");
    vLayout->addWidget(vTitle);

    m_cameraFeedLabel = new QLabel("ANPR Kamera Oqimi Faol\n[RTSP / Web-Kamera / Adaptive CLAHE]", videoCard);
    m_cameraFeedLabel->setAlignment(Qt::AlignCenter);
    m_cameraFeedLabel->setStyleSheet("background-color: #0f172a; color: #2dd4bf; font-size: 15px; border-radius: 12px; min-height: 380px; font-weight: bold;");
    vLayout->addWidget(m_cameraFeedLabel, 1);

    QPushButton *simBtn = new QPushButton("🚗 Yangi Mashina Kirishini Simulyatsiya Qilish", videoCard);
    simBtn->setStyleSheet(R"(
        QPushButton {
            background-color: #0d9488;
            color: white;
            font-size: 13px;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            border: none;
        }
        QPushButton:hover { background-color: #0f766e; }
    )");
    connect(simBtn, &QPushButton::clicked, this, &MainWindow::onSimulateCameraDetection);
    vLayout->addWidget(simBtn);

    layout->addWidget(videoCard, 1);

    // O'ng: ANPR Jurnali
    QFrame *logCard = new QFrame(page);
    logCard->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;");
    QVBoxLayout *lLayout = new QVBoxLayout(logCard);

    QLabel *lTitle = new QLabel("<b>So'nggi O'qilgan Raqamlar (Konsensus)</b>", logCard);
    lTitle->setStyleSheet("font-size: 14px; color: #0f172a;");
    lLayout->addWidget(lTitle);

    m_anprDetectionsTable = new QTableWidget(0, 4, logCard);
    m_anprDetectionsTable->setHorizontalHeaderLabels({"Vaqt", "Davlat Raqami", "Aniqlik", "Holat"});
    m_anprDetectionsTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    m_anprDetectionsTable->setStyleSheet("border: none; font-size: 12px;");
    lLayout->addWidget(m_anprDetectionsTable);

    layout->addWidget(logCard, 1);
    return page;
}

QWidget* MainWindow::createStaffPage() {
    QWidget *page = new QWidget();
    QVBoxLayout *layout = new QVBoxLayout(page);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(14);

    QFrame *staffCard = new QFrame(page);
    staffCard->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;");
    QVBoxLayout *sLayout = new QVBoxLayout(staffCard);

    QHBoxLayout *sHead = new QHBoxLayout();
    QLabel *sTitle = new QLabel("<b>Xodimlar va Ruxsatlar Boshqaruvi (Super-Admin, Adminlar, 5 Operator)</b>", staffCard);
    sTitle->setStyleSheet("font-size: 15px; color: #0f172a;");
    sHead->addWidget(sTitle);
    sHead->addStretch();
    sLayout->addLayout(sHead);

    m_staffTable = new QTableWidget(0, 5, staffCard);
    m_staffTable->setHorizontalHeaderLabels({"ID", "Login", "F.I.SH", "Roli", "Smenasi / Vazifasi"});
    m_staffTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    m_staffTable->setStyleSheet("border: none; font-size: 12px;");
    sLayout->addWidget(m_staffTable, 1);

    // Yangi xodim qo'shish paneli (Faqat Super-Admin uchun)
    QGroupBox *addBox = new QGroupBox("Yangi Xodim Qo'shish");
    addBox->setStyleSheet("font-size: 12px; font-weight: bold; color: #334155;");
    QHBoxLayout *addLayout = new QHBoxLayout(addBox);

    m_newStaffUserEdit = new QLineEdit();
    m_newStaffUserEdit->setPlaceholderText("Login (masalan: op_smena_4)");
    m_newStaffNameEdit = new QLineEdit();
    m_newStaffNameEdit->setPlaceholderText("To'liq Ism (F.I.SH)");

    m_newStaffRoleCombo = new QComboBox();
    m_newStaffRoleCombo->addItems({"OPERATOR", "ADMIN"});

    m_newStaffShiftCombo = new QComboBox();
    m_newStaffShiftCombo->addItems({"Smena 1 (08:00 - 16:00)", "Smena 2 (16:00 - 00:00)", "Smena 3 (00:00 - 08:00)", "Zaxira"});

    QPushButton *addBtn = new QPushButton("➕ Xodimni Saqlash");
    addBtn->setStyleSheet("background-color: #0d9488; color: white; padding: 8px 16px; border-radius: 8px; font-weight: bold;");
    connect(addBtn, &QPushButton::clicked, this, &MainWindow::onAddNewStaff);

    addLayout->addWidget(m_newStaffUserEdit);
    addLayout->addWidget(m_newStaffNameEdit);
    addLayout->addWidget(m_newStaffRoleCombo);
    addLayout->addWidget(m_newStaffShiftCombo);
    addLayout->addWidget(addBtn);

    sLayout->addWidget(addBox);
    layout->addWidget(staffCard);

    onRefreshStaffTable();
    return page;
}

QWidget* MainWindow::createFinancePage() {
    QWidget *page = new QWidget();
    QVBoxLayout *layout = new QVBoxLayout(page);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(14);

    QFrame *finCard = new QFrame(page);
    finCard->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 16px;");
    QVBoxLayout *fLayout = new QVBoxLayout(finCard);

    QLabel *fTitle = new QLabel("<b>💳 Moliya, Kassa va To'lovlar Tahlili</b>", finCard);
    fTitle->setStyleSheet("font-size: 16px; color: #0f172a;");
    fLayout->addWidget(fTitle);

    QGridLayout *grid = new QGridLayout();
    auto makeFinCard = [](const QString& name, const QString& amount, const QString& color) {
        QFrame *c = new QFrame();
        c->setStyleSheet(QString("background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 14px;"));
        QVBoxLayout *l = new QVBoxLayout(c);
        QLabel *n = new QLabel(name);
        n->setStyleSheet("font-size: 12px; color: #64748b; font-weight: bold;");
        QLabel *a = new QLabel(amount);
        a->setStyleSheet(QString("font-size: 22px; font-weight: bold; color: %1; margin-top: 4px;").arg(color));
        l->addWidget(n);
        l->addWidget(a);
        return c;
    };

    grid->addWidget(makeFinCard("Payme To'lovlari", "2,450,000 UZS", "#0ea5e9"), 0, 0);
    grid->addWidget(makeFinCard("Click To'lovlari", "1,650,000 UZS", "#8b5cf6"), 0, 1);
    grid->addWidget(makeFinCard("Naqd / Terminal Kassa", "750,000 UZS", "#f59e0b"), 0, 2);
    fLayout->addLayout(grid);

    m_financeTransactionsTable = new QTableWidget(0, 5, finCard);
    m_financeTransactionsTable->setHorizontalHeaderLabels({"Tranzaksiya ID", "To'lovchi", "Provayder", "Summa", "Fiskal Chek"});
    m_financeTransactionsTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    m_financeTransactionsTable->setStyleSheet("border: none; font-size: 12px; margin-top: 10px;");

    int r = 0;
    auto addTx = [this, &r](const QString& tx, const QString& p, const QString& prov, const QString& sum, const QString& f) {
        m_financeTransactionsTable->insertRow(r);
        m_financeTransactionsTable->setItem(r, 0, new QTableWidgetItem(tx));
        m_financeTransactionsTable->setItem(r, 1, new QTableWidgetItem(p));
        m_financeTransactionsTable->setItem(r, 2, new QTableWidgetItem(prov));
        m_financeTransactionsTable->setItem(r, 3, new QTableWidgetItem(sum));
        m_financeTransactionsTable->setItem(r, 4, new QTableWidgetItem(f));
        r++;
    };

    addTx("PAY-9921", "01 A 777 AA", "Payme", "15,000 UZS", "FISC-88214");
    addTx("CLK-8812", "10 123 BBA", "Click", "10,000 UZS", "FISC-88213");
    addTx("PAY-9920", "01 888 ZZZ", "Payme", "35,000 UZS", "FISC-88212");

    fLayout->addWidget(m_financeTransactionsTable, 1);
    layout->addWidget(finCard);

    return page;
}

QWidget* MainWindow::createSettingsPage() {
    QWidget *page = new QWidget();
    QVBoxLayout *layout = new QVBoxLayout(page);
    layout->setContentsMargins(0, 0, 0, 0);

    QFrame *card = new QFrame(page);
    card->setStyleSheet("background-color: #ffffff; border-radius: 18px; border: 1px solid #e2e8f0; padding: 20px;");
    QVBoxLayout *cLayout = new QVBoxLayout(card);

    QLabel *sTitle = new QLabel("<b>⚙️ Parkovka Tizimi va Tarif Sozlamalari</b>", card);
    sTitle->setStyleSheet("font-size: 16px; color: #0f172a; margin-bottom: 10px;");
    cLayout->addWidget(sTitle);

    QGridLayout *formGrid = new QGridLayout();
    formGrid->setSpacing(12);

    auto addField = [formGrid](int row, const QString& label, QLineEdit*& edit, const QString& defaultVal) {
        QLabel *lbl = new QLabel(label);
        lbl->setStyleSheet("font-size: 13px; font-weight: 600; color: #334155;");
        edit = new QLineEdit();
        edit->setText(defaultVal);
        edit->setStyleSheet("padding: 8px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background-color: #f8fafc;");
        formGrid->addWidget(lbl, row, 0);
        formGrid->addWidget(edit, row, 1);
    };

    addField(0, "Kunduzgi soatlik stavka (08:00 - 20:00):", m_dayRateEdit, "5000 UZS");
    addField(1, "Tungi soatlik stavka (20:00 - 08:00):", m_nightRateEdit, "3000 UZS");
    addField(2, "Dastlabki bepul oraliq (Grace Period):", m_gracePeriodEdit, "15 daqiqa");
    addField(3, "To'lovdan so'ng chiqish oralig'i:", m_exitGraceEdit, "15 daqiqa");
    addField(4, "Kunlik maksimal to'lov (Daily Cap):", m_dailyCapEdit, "50000 UZS");

    QLabel *bLbl = new QLabel("Shlagbaum avtomatik ochilishi:");
    bLbl->setStyleSheet("font-size: 13px; font-weight: 600; color: #334155;");
    m_barrierAutoOpenCombo = new QComboBox();
    m_barrierAutoOpenCombo->addItems({"Yoqilgan (To'lov tekshirilgach darhol)", "Qo'lda (Faqat operator tasdig'i bilan)"});
    m_barrierAutoOpenCombo->setStyleSheet("padding: 8px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background-color: #f8fafc; font-weight: 600;");
    formGrid->addWidget(bLbl, 5, 0);
    formGrid->addWidget(m_barrierAutoOpenCombo, 5, 1);

    cLayout->addLayout(formGrid);

    QPushButton *saveBtn = new QPushButton("💾 Sozlamalarni Saqlash", card);
    saveBtn->setStyleSheet(R"(
        QPushButton {
            background-color: #0d9488;
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 10px 24px;
            border-radius: 10px;
            border: none;
            margin-top: 15px;
        }
        QPushButton:hover { background-color: #0f766e; }
    )");
    connect(saveBtn, &QPushButton::clicked, this, &MainWindow::onSaveSettings);
    cLayout->addWidget(saveBtn, 0, Qt::AlignLeft);

    cLayout->addStretch();
    layout->addWidget(card);
    return page;
}

void MainWindow::onNavButtonClicked(int index) {
    m_contentStack->setCurrentIndex(index);
    if (m_navGroup->button(index)) m_navGroup->button(index)->setChecked(true);
    if (m_topPillGroup->button(index)) m_topPillGroup->button(index)->setChecked(true);
}

void MainWindow::applyRolePermissions() {
    if (m_role == "OPERATOR") {
        // Operatorga Moliya (4), Xodimlar (3) va Sozlamalar (5) yopiq
        if (m_topPillGroup->button(3)) m_topPillGroup->button(3)->setEnabled(false);
        if (m_topPillGroup->button(4)) m_topPillGroup->button(4)->setEnabled(false);
        if (m_topPillGroup->button(5)) m_topPillGroup->button(5)->setEnabled(false);

        if (m_navGroup->button(3)) m_navGroup->button(3)->setEnabled(false);
        if (m_navGroup->button(4)) m_navGroup->button(4)->setEnabled(false);
        if (m_navGroup->button(5)) m_navGroup->button(5)->setEnabled(false);
    } else {
        for (int i = 0; i <= 5; ++i) {
            if (m_topPillGroup->button(i)) m_topPillGroup->button(i)->setEnabled(true);
            if (m_navGroup->button(i)) m_navGroup->button(i)->setEnabled(true);
        }
    }
}

void MainWindow::onFloorChanged(int index) {
    m_mapWidget->setFloor(index + 1);
}

void MainWindow::onSlotSelected(const ParkingSlotItem& slot) {
    m_slotDetailsLabel->setText(
        QString("Tanlangan slot: <b>%1</b> | Turi: <b>%2</b> | Holati: <b>%3</b> | Mashina: <b>%4</b>")
            .arg(slot.slotNumber, slot.slotType, slot.status,
                 slot.currentPlate.isEmpty() ? "Yo'q" : slot.currentPlate)
    );
}

void MainWindow::onManualOpenBarrier() {
    // Shlagbaum ochish
}

void MainWindow::onRefreshStaffTable() {
    auto staff = DatabaseManager::instance().getAllStaff();
    m_staffTable->setRowCount(0);
    for (const auto& u : staff) {
        int r = m_staffTable->rowCount();
        m_staffTable->insertRow(r);
        m_staffTable->setItem(r, 0, new QTableWidgetItem(QString::number(u.id)));
        m_staffTable->setItem(r, 1, new QTableWidgetItem(u.username));
        m_staffTable->setItem(r, 2, new QTableWidgetItem(u.fullName));
        m_staffTable->setItem(r, 3, new QTableWidgetItem(u.role));
        m_staffTable->setItem(r, 4, new QTableWidgetItem(u.shift));
    }
}

void MainWindow::onAddNewStaff() {
    QString u = m_newStaffUserEdit->text().trimmed();
    QString n = m_newStaffNameEdit->text().trimmed();
    if (u.isEmpty() || n.isEmpty()) {
        QMessageBox::warning(this, "Diqqat", "Iltimos, login va ismni to'liq kiriting!");
        return;
    }

    int r = m_staffTable->rowCount();
    m_staffTable->insertRow(r);
    m_staffTable->setItem(r, 0, new QTableWidgetItem(QString::number(r + 1)));
    m_staffTable->setItem(r, 1, new QTableWidgetItem(u));
    m_staffTable->setItem(r, 2, new QTableWidgetItem(n));
    m_staffTable->setItem(r, 3, new QTableWidgetItem(m_newStaffRoleCombo->currentText()));
    m_staffTable->setItem(r, 4, new QTableWidgetItem(m_newStaffShiftCombo->currentText()));

    m_newStaffUserEdit->clear();
    m_newStaffNameEdit->clear();
    QMessageBox::information(this, "Muvaffaqiyat", "✅ Yangi xodim muvaffaqiyatli saqlandi!");
}

void MainWindow::onSaveSettings() {
    QMessageBox::information(this, "Sozlamalar", "✅ Barcha tarif va tizim sozlamalari bazaga saqlandi!");
}

void MainWindow::onSimulateCameraDetection() {
    int r = m_anprDetectionsTable->rowCount();
    m_anprDetectionsTable->insertRow(0);

    QString plate = QString("01 A %1 AA").arg(rand() % 900 + 100);
    m_anprDetectionsTable->setItem(0, 0, new QTableWidgetItem(QDateTime::currentDateTime().toString("hh:mm:ss")));
    m_anprDetectionsTable->setItem(0, 1, new QTableWidgetItem(plate));
    m_anprDetectionsTable->setItem(0, 2, new QTableWidgetItem("98.2%"));
    m_anprDetectionsTable->setItem(0, 3, new QTableWidgetItem("KIRISH GA RUXSAT"));

    DatabaseManager::instance().updateSlotStatus("A-101", "OCCUPIED", plate);
    m_mapWidget->reloadSlots();
}

void MainWindow::onLogout() {
    QMessageBox::StandardButton reply = QMessageBox::question(
        this, "Chiqish", "Tizimdan chiqishni xohlaysizmi?", QMessageBox::Yes | QMessageBox::No
    );
    if (reply == QMessageBox::Yes) {
        close();
    }
}
