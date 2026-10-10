#pragma once

#include <QString>
#include <QVector>
#include <QDateTime>
#include <memory>

struct ParkingSlotItem {
    int id;
    int floor;
    QString zone;
    QString slotNumber;
    QString slotType;     // REGULAR, EV_CHARGING, VIP_STAFF, ACCESSIBLE
    QString status;       // FREE, OCCUPIED, RESERVED, PAYMENT_PENDING, MAINTENANCE
    int posX;
    int posY;
    int width;
    int height;
    QString currentPlate;
};

struct UserStaffItem {
    int id;
    QString username;
    QString fullName;
    QString role;         // SUPER_ADMIN, ADMIN, OPERATOR
    QString shift;        // Smena 1, Smena 2
    bool isActive;
};

struct AuditLogItem {
    int id;
    QString operatorName;
    QString action;
    QString reason;
    QDateTime timestamp;
};

class DatabaseManager {
public:
    static DatabaseManager& instance();

    bool connectToPostgres(const QString& host, int port, const QString& dbName,
                           const QString& user, const QString& password);
    bool connectToSqlite(const QString& dbPath = "parkly_local.db");
    bool isConnected() const;

    // Slots
    QVector<ParkingSlotItem> getSlotsByFloor(int floor);
    bool updateSlotStatus(const QString& slotNumber, const QString& newStatus, const QString& plate = "");

    // Staff
    QVector<UserStaffItem> getAllStaff();

    // Barrier Override Audit
    bool logBarrierOverride(const QString& operatorName, const QString& reason);
    QVector<AuditLogItem> getRecentOverrides();

private:
    DatabaseManager();
    ~DatabaseManager();
    bool m_connected;
    QVector<ParkingSlotItem> m_mockSlots;
    QVector<UserStaffItem> m_mockStaff;
    QVector<AuditLogItem> m_mockAudit;

    void initMockData();
};
