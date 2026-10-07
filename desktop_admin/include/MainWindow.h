#pragma once

#include <QMainWindow>
#include <QStackedWidget>
#include <QTableWidget>
#include <QLabel>
#include <QPushButton>
#include <QLineEdit>
#include <QComboBox>
#include <QButtonGroup>
#include "ParkingMapWidget.h"
#include "DatabaseManager.h"

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void setAuthenticatedUser(const QString& username, const QString& fullName, const QString& role);

private slots:
    void onNavButtonClicked(int index);
    void onFloorChanged(int index);
    void onSlotSelected(const ParkingSlotItem& slot);
    void onManualOpenBarrier();
    void onRefreshStaffTable();
    void onAddNewStaff();
    void onSaveSettings();
    void onSimulateCameraDetection();
    void onLogout();

private:
    QString m_username;
    QString m_fullName;
    QString m_role; // "SUPER_ADMIN", "ADMIN", "OPERATOR"

    // UI Elementlari
    QStackedWidget *m_contentStack;
    QButtonGroup *m_navGroup;
    QButtonGroup *m_topPillGroup;

    QLabel *m_userProfilePill;
    QLabel *m_greetingTitle;
    QLabel *m_greetingSubtitle;

    // View 0: Dashboard (Bosh Sahifa)
    QLabel *m_totalRevenueLabel;
    QLabel *m_freeSlotsCountLabel;
    QLabel *m_occupiedSlotsCountLabel;
    QLabel *m_reservedSlotsCountLabel;
    QTableWidget *m_recentActivitiesTable;

    // View 1: 2D Parking Xarita
    ParkingMapWidget *m_mapWidget;
    QComboBox *m_floorCombo;
    QLabel *m_slotDetailsLabel;

    // View 2: Kameralar & ANPR
    QLabel *m_cameraFeedLabel;
    QTableWidget *m_anprDetectionsTable;

    // View 3: Xodimlar va Rollar
    QTableWidget *m_staffTable;
    QLineEdit *m_newStaffUserEdit;
    QLineEdit *m_newStaffNameEdit;
    QComboBox *m_newStaffRoleCombo;
    QComboBox *m_newStaffShiftCombo;

    // View 4: Kassa va Moliya
    QLabel *m_paymeTotalLabel;
    QLabel *m_clickTotalLabel;
    QLabel *m_cashTotalLabel;
    QTableWidget *m_financeTransactionsTable;

    // View 5: Sozlamalar (Settings)
    QLineEdit *m_dayRateEdit;
    QLineEdit *m_nightRateEdit;
    QLineEdit *m_gracePeriodEdit;
    QLineEdit *m_exitGraceEdit;
    QLineEdit *m_dailyCapEdit;
    QComboBox *m_barrierAutoOpenCombo;

    // Shlagbaum boshqaruvi
    QLineEdit *m_overrideReasonEdit;
    QTableWidget *m_auditTable;

    void setupUI();
    QWidget* createLeftSidebar();
    QWidget* createTopHeader();
    
    // Sahifalar
    QWidget* createDashboardPage();
    QWidget* createMapPage();
    QWidget* createCameraPage();
    QWidget* createStaffPage();
    QWidget* createFinancePage();
    QWidget* createSettingsPage();

    void applyRolePermissions();
};
