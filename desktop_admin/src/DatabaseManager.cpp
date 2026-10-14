#include "DatabaseManager.h"
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>
#include <QDebug>

DatabaseManager& DatabaseManager::instance() {
    static DatabaseManager inst;
    return inst;
}

DatabaseManager::DatabaseManager() : m_connected(false) {
    initMockData();
}

DatabaseManager::~DatabaseManager() {}

void DatabaseManager::initMockData() {
    // 1-qavat boshlang'ich slotlari
    m_mockSlots = {
        {1, 1, "A", "A-101", "REGULAR", "FREE", 50, 50, 80, 140, ""},
        {2, 1, "A", "A-102", "REGULAR", "OCCUPIED", 150, 50, 80, 140, "01 A 777 AA"},
        {3, 1, "A", "A-103", "REGULAR", "FREE", 250, 50, 80, 140, ""},
        {4, 1, "A", "A-104", "REGULAR", "RESERVED", 350, 50, 80, 140, ""},
        {5, 1, "A", "A-105", "REGULAR", "PAYMENT_PENDING", 450, 50, 80, 140, "10 123 BBA"},
        {6, 1, "A", "A-106", "REGULAR", "MAINTENANCE", 550, 50, 80, 140, ""},

        {7, 1, "EV", "EV-01", "EV_CHARGING", "FREE", 50, 240, 80, 140, ""},
        {8, 1, "EV", "EV-02", "EV_CHARGING", "OCCUPIED", 150, 240, 80, 140, "01 888 ZZZ"},
        {9, 1, "EV", "EV-03", "EV_CHARGING", "FREE", 250, 240, 80, 140, ""},

        {10, 1, "VIP", "VIP-01", "VIP_STAFF", "FREE", 350, 240, 80, 140, ""},
        {11, 1, "VIP", "VIP-02", "VIP_STAFF", "OCCUPIED", 450, 240, 80, 140, "01 001 PPP"},
        {12, 1, "VIP", "VIP-03", "VIP_STAFF", "RESERVED", 550, 240, 80, 140, ""}
    };

    // Huquqlar Matritsasi: 2 ta Super-Admin, 4 ta Oddiy Admin va 2 ta Smena Operatorlari
    m_mockStaff = {
        {1, "admin", "Erjigit (Bosh Rahbar)", "SUPER_ADMIN", "Asosiy Boshqaruv", true},
        {2, "superadmin2", "Sherzod Aliyev", "SUPER_ADMIN", "Tizim Arxitekturasi", true},
        {3, "admin_yunusobod", "Jahongir Qodirov", "ADMIN", "Yunusobod Filiali", true},
        {4, "admin_chilonzor", "Aziz Rustamov", "ADMIN", "Chilonzor Filiali", true},
        {5, "admin_mirobod", "Bobur Mirzayev", "ADMIN", "Mirobod Filiali", true},
        {6, "admin_sergeli", "Dilshod Karimov", "ADMIN", "Sergeli Filiali", true},
        {7, "operator1", "Farrux Yusupov", "OPERATOR", "Smena 1 (08:00 - 20:00)", true},
        {8, "operator2", "G'ayrat Xoliqov", "OPERATOR", "Smena 2 (20:00 - 08:00)", true}
    };
}

bool DatabaseManager::connectToPostgres(const QString& host, int port, const QString& dbName,
                                        const QString& user, const QString& password) {
    QSqlDatabase db = QSqlDatabase::addDatabase("QPSQL");
    db.setHostName(host);
    db.setPort(port);
    db.setDatabaseName(dbName);
    db.setUserName(user);
    db.setPassword(password);

    if (db.open()) {
        m_connected = true;
        qDebug() << "PostgreSQL bazasiga muvaffaqiyatli ulandi!";
        return true;
    } else {
        qDebug() << "PostgreSQL ulanish xatosi:" << db.lastError().text();
        m_connected = false;
        return false;
    }
}

bool DatabaseManager::connectToSqlite(const QString& dbPath) {
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(dbPath);

    if (db.open()) {
        m_connected = true;
        qDebug() << "Lokal SQLite bazasiga (" << dbPath << ") muvaffaqiyatli ulandi!";
        return true;
    } else {
        qDebug() << "SQLite ulanish xatosi:" << db.lastError().text();
        m_connected = false;
        return false;
    }
}

bool DatabaseManager::isConnected() const {
    return m_connected;
}

QVector<ParkingSlotItem> DatabaseManager::getSlotsByFloor(int floor) {
    if (m_connected) {
        QSqlQuery query;
        query.prepare("SELECT id, floor, zone, slot_number, slot_type, status, pos_x, pos_y, width, height, current_vehicle_plate "
                      "FROM parking_slots WHERE floor = :floor ORDER BY slot_number ASC");
        query.bindValue(":floor", floor);

        if (query.exec()) {
            QVector<ParkingSlotItem> dbSlots;
            while (query.next()) {
                ParkingSlotItem item;
                item.id = query.value(0).toInt();
                item.floor = query.value(1).toInt();
                item.zone = query.value(2).toString();
                item.slotNumber = query.value(3).toString();
                item.slotType = query.value(4).toString();
                item.status = query.value(5).toString();
                item.posX = query.value(6).toInt();
                item.posY = query.value(7).toInt();
                item.width = query.value(8).toInt();
                item.height = query.value(9).toInt();
                item.currentPlate = query.value(10).toString();
                dbSlots.append(item);
            }
            if (!dbSlots.isEmpty()) {
                return dbSlots;
            }
        } else {
            qDebug() << "SQL xatolik (getSlotsByFloor):" << query.lastError().text();
        }
    }

    // Offline / Zaxira xotiradan olish
    QVector<ParkingSlotItem> result;
    for (const auto& s : m_mockSlots) {
        if (s.floor == floor) {
            result.append(s);
        }
    }
    return result;
}

bool DatabaseManager::updateSlotStatus(const QString& slotNumber, const QString& newStatus, const QString& plate) {
    if (m_connected) {
        QSqlQuery query;
        query.prepare("UPDATE parking_slots SET status = :status, current_vehicle_plate = :plate, last_status_change = CURRENT_TIMESTAMP "
                      "WHERE slot_number = :slot");
        query.bindValue(":status", newStatus);
        query.bindValue(":plate", plate.isEmpty() ? QVariant(QMetaType(QMetaType::QString)) : plate);
        query.bindValue(":slot", slotNumber);

        if (query.exec()) {
            qDebug() << "Bazada slot muvaffaqiyatli yangilandi:" << slotNumber;
        } else {
            qDebug() << "SQL xatolik (updateSlotStatus):" << query.lastError().text();
        }
    }

    // Lokal xotirani ham sinxron yangilash
    for (auto& s : m_mockSlots) {
        if (s.slotNumber == slotNumber) {
            s.status = newStatus;
            s.currentPlate = plate;
            return true;
        }
    }
    return false;
}

QVector<UserStaffItem> DatabaseManager::getAllStaff() {
    return m_mockStaff;
}

bool DatabaseManager::logBarrierOverride(const QString& operatorName, const QString& reason) {
    AuditLogItem log;
    log.id = m_mockAudit.size() + 1;
    log.operatorName = operatorName;
    log.action = "MANUAL_OPEN_BARRIER";
    log.reason = reason;
    log.timestamp = QDateTime::currentDateTime();
    m_mockAudit.prepend(log);
    return true;
}

QVector<AuditLogItem> DatabaseManager::getRecentOverrides() {
    return m_mockAudit;
}
