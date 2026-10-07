#include "ParkingMapWidget.h"
#include <QPainter>
#include <QMouseEvent>
#include <QLinearGradient>

ParkingMapWidget::ParkingMapWidget(QWidget* parent)
    : QWidget(parent), m_currentFloor(1) {
    setMinimumSize(700, 450);
    reloadSlots();
}

void ParkingMapWidget::setFloor(int floor) {
    m_currentFloor = floor;
    reloadSlots();
    update();
}

void ParkingMapWidget::reloadSlots() {
    m_slots = DatabaseManager::instance().getSlotsByFloor(m_currentFloor);
    update();
}

QColor ParkingMapWidget::getStatusColor(const QString& status) const {
    if (status == "FREE") return QColor(46, 204, 113);            // Yashil
    if (status == "OCCUPIED") return QColor(231, 76, 60);         // Qizil
    if (status == "RESERVED") return QColor(241, 196, 15);        // Sariq
    if (status == "PAYMENT_PENDING") return QColor(230, 126, 34); // To'q sariq
    if (status == "MAINTENANCE") return QColor(149, 165, 166);    // Kulrang
    return QColor(127, 140, 141);
}

void ParkingMapWidget::paintEvent(QPaintEvent* /*event*/) {
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    // Fon: Zamonaviy qorong'i asfalt
    painter.fillRect(rect(), QColor(26, 28, 35));

    // Yo'l chiziqlari (Har bir qator o'rtasidagi yo'lak)
    QPen roadPen(QColor(60, 64, 75), 2, Qt::DashLine);
    painter.setPen(roadPen);
    painter.drawLine(30, 200, width() - 30, 200);
    painter.drawLine(30, 390, width() - 30, 390);

    // Zonalarning sarlavhasi
    painter.setPen(QColor(180, 190, 205));
    QFont headerFont("Segoe UI", 11, QFont::Bold);
    painter.setFont(headerFont);
    painter.drawText(50, 35, "ZONA A — STANDART");
    painter.drawText(50, 225, "ZONA EV — ELEKTROMOBILLAR (CHARGING)");
    painter.drawText(350, 225, "ZONA VIP & XODIMLAR");

    // Slotlarni chizish
    QFont slotFont("Segoe UI", 9, QFont::Bold);
    QFont plateFont("Segoe UI", 7);

    for (const auto& slot : m_slots) {
        QRect slotRect(slot.posX, slot.posY, slot.width, slot.height);
        QColor statusColor = getStatusColor(slot.status);

        // Slot fonini gradient bilan to'ldirish
        QLinearGradient grad(slotRect.topLeft(), slotRect.bottomLeft());
        grad.setColorAt(0, statusColor.darker(110));
        grad.setColorAt(1, statusColor);

        painter.setBrush(grad);
        QPen borderPen(slot.slotNumber == m_selectedSlotNumber ? Qt::white : QColor(30, 30, 30),
                       slot.slotNumber == m_selectedSlotNumber ? 3 : 1);
        painter.setPen(borderPen);
        painter.drawRoundedRect(slotRect, 6, 6);

        // Slot raqami
        painter.setPen(Qt::white);
        painter.setFont(slotFont);
        painter.drawText(slotRect.adjusted(0, 8, 0, 0), Qt::AlignTop | Qt::AlignHCenter, slot.slotNumber);

        // Holat yozuvi
        QFont statusTextFont("Segoe UI", 7, QFont::DemiBold);
        painter.setFont(statusTextFont);
        painter.drawText(slotRect.adjusted(0, 0, 0, -8), Qt::AlignBottom | Qt::AlignHCenter, slot.status);

        // Agar mashina turgan bo'lsa, davlat raqamini ko'rsatish
        if (!slot.currentPlate.isEmpty()) {
            QRect plateBox(slotRect.x() + 5, slotRect.y() + 45, slotRect.width() - 10, 24);
            painter.setBrush(Qt::white);
            painter.setPen(Qt::black);
            painter.drawRoundedRect(plateBox, 3, 3);
            painter.setFont(plateFont);
            painter.drawText(plateBox, Qt::AlignCenter, slot.currentPlate);
        }
    }
}

void ParkingMapWidget::mousePressEvent(QMouseEvent* event) {
    for (const auto& slot : m_slots) {
        QRect slotRect(slot.posX, slot.posY, slot.width, slot.height);
        if (slotRect.contains(event->pos())) {
            m_selectedSlotNumber = slot.slotNumber;
            update();
            emit slotSelected(slot);
            return;
        }
    }
}
