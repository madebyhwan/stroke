# DB와 상호작용하는 Health 모델을 정의

from pydantic import BaseModel, Field
from datetime import date, datetime

from server.schemas.healthSchema import sexEnum

class HealthDataDB(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    sex: sexEnum
    birth_date: date
    height_cm: int
    stroke_history: bool
    hypertension: bool
    heart_disease: bool
    diabetes: bool
    smoking_status: bool

    weight_kg: float
    systolic_bp: int
    diastolic_bp: int
    glucose_level: int
    smoking: int

    created_at: datetime = Field(default_factory=datetime.now)