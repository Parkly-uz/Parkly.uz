#pragma once

#include <QWidget>
#include "DatabaseManager.h"

class ParkingMapWidget : public QWidget {
    Q_OBJECT
public:
    explicit ParkingMapWidget(QWidget* parent = nullptr);
    void setFloor(int floor);
    void reloadSlots();

signals:
    void slotSelected(const ParkingSlotItem& slot);

protected:
    void paintEvent(QPaintEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;

private:
    int m_currentFloor;
    QVector<ParkingSlotItem> m_slots;
    QString m_selectedSlotNumber;

    QColor getStatusColor(const QString& status) const;
};
