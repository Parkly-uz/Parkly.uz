"""
Parkly.uz — Rasmiy Jamoa Rollari (RBAC) va Vazifalar Taqsimoti.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel


class ProjectRole(str, Enum):
    PROJECT_MANAGER = "PROJECT_MANAGER"    # Samaxov Dilshod (Boshqaruv, muddatlar, sprintlar)
    LEAD_DEVELOPER = "LEAD_DEVELOPER"      # Erjigitov Mirhamid (Arxitektura, backend, vision, kod)
    STAKEHOLDER = "STAKEHOLDER"            # Saidov Abbos (Buyurtmachi, talablar, yakuniy qabul)
    BUSINESS_ANALYST = "BUSINESS_ANALYST"  # Tohirjonov Hikmatilla (Biznes mantiq, tariflar, tahlil)


class TeamMember(BaseModel):
    full_name: str
    role: ProjectRole
    responsibilities: List[str]
    github_access: str
    assigned_modules: List[str]


# 👥 Rasmiy 4 ta asosiy boshqaruv a'zolari
CORE_TEAM: Dict[str, TeamMember] = {
    "dilshod_pm": TeamMember(
        full_name="Samaxov Dilshod",
        role=ProjectRole.PROJECT_MANAGER,
        responsibilities=[
            "Loyiha rejasi, muddatlari va resurslarini boshqarish",
            "Sprintlarni rejalashtirish va Taskcafe / GitHub Kanban nazorati",
            "10 daqiqalik SLA qat'iy nazorati va risklarni boshqarish",
            "Jamoa a'zolari o'rtasida vazifalar taqsimoti"
        ],
        github_access="Maintain / Admin",
        assigned_modules=["Project Scope", "Taskcafe Board", "SLA Monitoring", "Risk Matrix"]
    ),
    "mirhamid_dev": TeamMember(
        full_name="Erjigitov Mirhamid",
        role=ProjectRole.LEAD_DEVELOPER,
        responsibilities=[
            "Tizim arxitekturasi va backend API ishlab chiqish",
            "Adversarial Weather CV va Two-Stage ANPR algoritmlari",
            "100% naqd pulsiz to'lov va zaxira qarz moduli (Cashless & Debt)",
            "Shlagbaum datchiklari va 10-daqiqalik Fail-Safe taymeri",
            "Unit testlar va CI/CD avtomatizatsiyasi"
        ],
        github_access="Admin / Owner",
        assigned_modules=["Core Engine", "Vision AI", "SLA Watchdog", "FastAPI Backend", "Pytest"]
    ),
    "abbos_stakeholder": TeamMember(
        full_name="Saidov Abbos",
        role=ProjectRole.STAKEHOLDER,
        responsibilities=[
            "Biznes talablarini belgilash va strategik yo'nalish berish",
            "Investitsiya va byudjet nazorati",
            "Yakuniy mahsulot qabuli (Acceptance & Sign-off)",
            "Bozor va mijozlar ehtiyojlarini tizimga integratsiya qilish"
        ],
        github_access="Triage / Reviewer",
        assigned_modules=["Product Strategy", "High-level Acceptance Criteria", "Business Value"]
    ),
    "hikmatilla_ba": TeamMember(
        full_name="Tohirjonov Hikmatilla",
        role=ProjectRole.BUSINESS_ANALYST,
        responsibilities=[
            "Biznes talablarini texnik spetsifikatsiyaga aylantirish (SRS)",
            "Tariflar tizimi, bepul oraliq va jarimalar hisob-kitob modeli",
            "User Story va batafsil Acceptance Criteria'larni ishlab chiqish",
            "Kirish/chiqish oqimlari (Enter/Exit User Journey) tahlili"
        ],
        github_access="Write / Collaborator",
        assigned_modules=["Pricing & Tariffs", "User Stories", "Process Flowcharts", "SRS Docs"]
    )
}
