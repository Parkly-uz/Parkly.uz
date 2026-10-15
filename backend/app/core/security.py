"""
Parkly.uz — RBAC (Role-Based Access Control) va 8 ta akkaunt huquqlari.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"      # Erjigit va Sherzod (To'liq nazorat)
    ADMIN = "ADMIN"                  # 4 ta filial adminlari
    OPERATOR = "OPERATOR"            # 2 ta smena nazoratchilari


class UserAccount(BaseModel):
    username: str
    full_name: str
    role: UserRole
    branch_id: Optional[str] = None
    can_change_tariffs: bool = False
    can_manual_open_barrier: bool = False
    can_view_audit_logs: bool = False


# Rasmiy 8 ta tasdiqlangan akkaunt
OFFICIAL_ACCOUNTS: Dict[str, UserAccount] = {
    "admin": UserAccount(
        username="admin",
        full_name="Erjigit (Bosh Rahbar)",
        role=UserRole.SUPER_ADMIN,
        can_change_tariffs=True,
        can_manual_open_barrier=True,
        can_view_audit_logs=True
    ),
    "superadmin2": UserAccount(
        username="superadmin2",
        full_name="Sherzod Aliyev (Tizim Arxitektori)",
        role=UserRole.SUPER_ADMIN,
        can_change_tariffs=True,
        can_manual_open_barrier=True,
        can_view_audit_logs=True
    ),
    "admin_yunusobod": UserAccount(
        username="admin_yunusobod",
        full_name="Jahongir Qodirov",
        role=UserRole.ADMIN,
        branch_id="YUNUSOBOD",
        can_change_tariffs=False,
        can_manual_open_barrier=False,
        can_view_audit_logs=False
    ),
    "admin_chilonzor": UserAccount(
        username="admin_chilonzor",
        full_name="Aziz Rustamov",
        role=UserRole.ADMIN,
        branch_id="CHILONZOR",
        can_change_tariffs=False,
        can_manual_open_barrier=False,
        can_view_audit_logs=False
    ),
    "admin_mirobod": UserAccount(
        username="admin_mirobod",
        full_name="Bobur Mirzayev",
        role=UserRole.ADMIN,
        branch_id="MIROBOD",
        can_change_tariffs=False,
        can_manual_open_barrier=False,
        can_view_audit_logs=False
    ),
    "admin_sergeli": UserAccount(
        username="admin_sergeli",
        full_name="Dilshod Karimov",
        role=UserRole.ADMIN,
        branch_id="SERGELI",
        can_change_tariffs=False,
        can_manual_open_barrier=False,
        can_view_audit_logs=False
    ),
    "operator1": UserAccount(
        username="operator1",
        full_name="Farrux Yusupov",
        role=UserRole.OPERATOR,
        can_change_tariffs=False,
        can_manual_open_barrier=True,  # Faqat favqulodda sabab bilan
        can_view_audit_logs=False
    ),
    "operator2": UserAccount(
        username="operator2",
        full_name="G'ayrat Xoliqov",
        role=UserRole.OPERATOR,
        can_change_tariffs=False,
        can_manual_open_barrier=True,
        can_view_audit_logs=False
    ),
}


def check_permission(username: str, action: str) -> bool:
    """Foydalanuvchi huquqini qat'iy tekshirish."""
    user = OFFICIAL_ACCOUNTS.get(username)
    if not user:
        return False
    if user.role == UserRole.SUPER_ADMIN:
        return True
    if action == "change_tariffs":
        return user.can_change_tariffs
    if action == "view_audit":
        return user.can_view_audit_logs
    if action == "open_barrier":
        return user.can_manual_open_barrier
    return False
