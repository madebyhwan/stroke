# client와 server 간에 주고받는 health data의 스키마 정의

from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime

class sexEnum(str, Enum):
    MALE = "M"
    FEMALE = "F"

class BaseHealth(BaseModel):
    user_id: str
    sex: sexEnum
    birth_date: date
    height_cm: int
    stroke_history: bool
    hypertension: bool  # 고혈압
    heart_disease: bool
    diabetes: bool
    smoking_status: bool

class HealthInput(BaseHealth):
    weight_kg: float
    systolic_bp: int    # 수축기 혈압 (mmHg)
    diastolic_bp: int   # 이완기 혈압 (mmHg)
    glucose_level: int  # 공복 혈당 (mg/dL)
    smoking: int        # 흡연량 (개비/일)

class HealthResponse(HealthInput):
    id: str
    created_at: datetime