import os
import sys

# Offscreen mode for headless PyQt6 execution
os.environ["QT_QPA_PLATFORM"] = "offscreen"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "desktop_admin"))

from PyQt6.QtWidgets import QApplication, QMessageBox
from desktop_admin.db_manager import ParklyDatabase
from desktop_admin.run_admin_app import MainWindow

# Mock QMessageBox to prevent blocking modal loops during automated testing
QMessageBox.warning = lambda *args, **kwargs: QMessageBox.StandardButton.Ok
QMessageBox.information = lambda *args, **kwargs: QMessageBox.StandardButton.Ok
QMessageBox.critical = lambda *args, **kwargs: QMessageBox.StandardButton.Ok
QMessageBox.question = lambda *args, **kwargs: QMessageBox.StandardButton.Yes

def test_full_rbac_and_finance():
    app = QApplication(sys.argv)
    db = ParklyDatabase()

    print("==================================================")
    print("PARKLY.UZ — RBAC VA MOLIYA TIZIMI TESTLARI")
    print("==================================================")

    # 1. Huquqlar Matritsasi Tekshiruvi
    staff = db.get_all_staff()
    super_admins = [s for s in staff if s["role"] == "SUPER_ADMIN"]
    oddiy_admins = [s for s in staff if s["role"] == "ADMIN"]
    operators = [s for s in staff if s["role"] == "OPERATOR"]

    print(f"Jami xodimlar: {len(staff)} kishi")
    print(f"Super-Adminlar soni: {len(super_admins)} kishi (Kutilgan: 2)")
    print(f"Oddiy Adminlar soni: {len(oddiy_admins)} kishi (Kutilgan: 4)")
    print(f"Operatorlar soni: {len(operators)} kishi (Kutilgan: 2)")

    assert len(super_admins) == 2, f"Kutilgan 2 ta Super-Admin, lekin topildi: {len(super_admins)}"
    assert len(oddiy_admins) == 4, f"Kutilgan 4 ta Oddiy Admin, lekin topildi: {len(oddiy_admins)}"
    assert len(operators) == 2, f"Kutilgan 2 ta Operator, lekin topildi: {len(operators)}"

    # 2. Super-Admin Seansi
    print("\n--- TEST 1: SUPER-ADMIN SESSIYASI ---")
    user_super = db.authenticate("admin", "admin123")
    assert user_super is not None, "Super admin login xatosi"
    w_super = MainWindow(db, user_super)
    print("Super-Admin MainWindow muvaffaqiyatli ochildi.")

    for idx in range(7):
        w_super.navigate_module(idx, f"Modul {idx}")
        assert w_super.stack.currentIndex() == idx, f"Super admin {idx}-modulga o'ta olmadi"
    print("Super-Admin barcha 7 ta modulga to'liq kirdi!")

    # 3. 4. Moliya va Tranzaksiyalar Bo'limi (Module 3) Funksiyalari
    print("\n--- TEST 2: MOLIYA VA TRANZAKSIYALAR BO'LIMI ---")
    w_super.navigate_module(3, "4. Moliya va Tranzaksiyalar")

    # A. get_financial_summary()
    fin_day = db.get_financial_summary("day")
    fin_week = db.get_financial_summary("week")
    fin_month = db.get_financial_summary("month")
    print(f"Kunlik tushum: {fin_day['today_revenue']} UZS ({fin_day['today_count']} ta tranzaksiya)")
    print(f"Haftalik tushum: {fin_week['week_revenue']} UZS ({fin_week['week_count']} ta tranzaksiya)")
    print(f"Oylik tushum: {fin_month['month_revenue']} UZS ({fin_month['month_count']} ta tranzaksiya)")
    print(f"Bar Chart nuqtalari soni: {len(fin_week['chart_data'])} ta kun")
    assert len(fin_week["chart_data"]) == 7, "7 kunlik chart ma'lumotlari to'liq emas"

    # B. get_transaction_history()
    tx_all = db.get_transaction_history(limit=50)
    tx_payme = db.get_transaction_history(provider="Payme", limit=50)
    tx_click = db.get_transaction_history(provider="Click", limit=50)
    print(f"Jami tranzaksiyalar: {len(tx_all)} ta")
    print(f"Payme to'lovlari: {len(tx_payme)} ta | Click to'lovlari: {len(tx_click)} ta")
    assert len(tx_all) >= 20, "Tranzaksiyalar bazasi kamida 20 ta bo'lishi kerak"

    # C. export_financial_report()
    ok_exp, path_exp = db.export_financial_report(export_format="csv")
    print(f"Eksport holati: {ok_exp} | Fayl: {path_exp}")
    assert ok_exp is True and os.path.exists(path_exp), "Eksport fayli yaratilmadi"

    # D. update_tariff_rates() - Super Admin muvaffaqiyatli
    ok_tar_super, msg_tar_super = db.update_tariff_rates(
        {"day_rate": 6000, "night_rate": 3500, "minute_rate": 120, "ev_rate": 3000},
        user_role="SUPER_ADMIN"
    )
    print(f"Super-Admin tarif yangilashi: {ok_tar_super} | {msg_tar_super}")
    assert ok_tar_super is True, "Super admin tarif o'zgartira olmadi"

    # 4. Oddiy Admin Seansi va RBAC Blokirovkasi
    print("\n--- TEST 3: ODDIY ADMIN SESSIYASI VA RBAC CHEKLOVLARI ---")
    user_admin = db.authenticate("admin_yunusobod", "admin123")
    assert user_admin is not None, "Oddiy admin login xatosi"
    assert user_admin["role"] == "ADMIN", "Rol ADMIN bo'lishi kerak"
    w_admin = MainWindow(db, user_admin)
    print("Oddiy Admin MainWindow ochildi.")

    # A. Oddiy Admin ruxsat etilgan modullar: 0, 1, 2, 3, 4
    for idx in [0, 1, 2, 3, 4]:
        w_admin.navigate_module(idx, f"Modul {idx}")
        assert w_admin.stack.currentIndex() == idx, f"Oddiy admin ruxsat etilgan {idx}-modulga o'ta olmadi"
    print("Oddiy Admin ruxsat etilgan modullarga (Dashboard, Map, Kameralar, Moliya, Sessiyalar) kirdi.")

    # B. Oddiy Admin bloklangan modullar: 5 (Xodimlar) va 6 (Sozlamalar)
    cur_idx = w_admin.stack.currentIndex()
    w_admin.navigate_module(5, "6. Xodimlar (RBAC)")
    assert w_admin.stack.currentIndex() == cur_idx, "XATOLIK: Oddiy Admin Xodimlar moduliga kirib ketdi!"
    print("RBAC Himoyasi: Oddiy Admin 6. Xodimlar modulidan bloklandi!")

    w_admin.navigate_module(6, "7. Tizim Sozlamalari")
    assert w_admin.stack.currentIndex() == cur_idx, "XATOLIK: Oddiy Admin Tizim Sozlamalari moduliga kirib ketdi!"
    print("RBAC Himoyasi: Oddiy Admin 7. Tizim Sozlamalari modulidan bloklandi!")

    # C. Oddiy Admin Tarif o'zgartirishga urinishi (rad etilishi kerak)
    ok_tar_admin, msg_tar_admin = db.update_tariff_rates(
        {"day_rate": 9999},
        user_role="ADMIN"
    )
    print(f"Oddiy Admin tarif o'zgartirishga urinishi: {ok_tar_admin} | {msg_tar_admin}")
    assert ok_tar_admin is False, "XATOLIK: Oddiy Admin tarifni o'zgartira oldi!"

    print("\n==================================================")
    print("BARCHA TESTLAR 100% MUVAFFAQIShIYATLI O'TDI!")
    print("==================================================")

if __name__ == "__main__":
    test_full_rbac_and_finance()
