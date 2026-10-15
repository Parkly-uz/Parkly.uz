"""
Parkly.uz — Tizim konfiguratsiyasi, tariflar va 10-daqiqalik SLA qoidalari.
"""

from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "Parkly.uz Smart Parking System"
    API_V1_STR: str = "/api/v1"
    
    # ⏱️ SLA Qoidalari
    SLA_MAX_WAIT_SECONDS: int = 600      # 10 daqiqa (Fail-Safe Emergency)
    SLA_WARNING_SECONDS: int = 300       # 5 daqiqa (Sariq)
    SLA_URGENT_SECONDS: int = 420        # 7 daqiqa (Qizil)
    
    # 💳 Rasmiy Tariflar (so'mda)
    GRACE_PERIOD_MINUTES: int = 15       # Dastlabki 15 daqiqa bepul
    RATE_DAY_HOURLY: float = 5000.0      # 08:00 - 20:00 (5,000 so'm/soat)
    RATE_NIGHT_HOURLY: float = 3000.0    # 20:00 - 08:00 (3,000 so'm/soat)
    RATE_PEAK_HOURLY: float = 8000.0     # To'lalik > 85% bo'lganda (8,000 so'm)
    RATE_DAILY_FIXED: float = 40000.0    # 24 soat fiksirlangan (40,000 so'm)
    
    # Ma'lumotlar bazasi
    DATABASE_URL: str = "sqlite+aiosqlite:///./parkly_production.db"
    
    class Config:
        case_sensitive = True


settings = Settings()
