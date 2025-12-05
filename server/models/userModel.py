# DB와 상호작용하는 User 모델을 정의
# MongoDB에 실제로 저장될 형태 정의

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    CAREGIVER = "CAREGIVER"

class sexEnum(str, Enum):
    MALE = "M"
    FEMALE = "F"

class smokingEnum(str, Enum):
    SMOKER = "SMOKER"
    PAST_SMOKER = "PAST_SMOKER"
    NON_SMOKER = "NON_SMOKER"

class UserDB(BaseModel):
    id: str = Field(..., alias="_id")
    password: str
    name: str
    role: UserRole
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # 환자 전용 필드 - 의사/보호자는 임의 설정
    sex: sexEnum = sexEnum.MALE  # "M" or "F"
    birth_date: date = Field(default_factory=date.today)
    height_cm: int = 170
    stroke_history: bool = False
    hypertension: bool = False
    heart_disease: bool = False
    diabetes: bool = False
    smoking_history: smokingEnum = smokingEnum.NON_SMOKER
    measured_at: datetime = Field(default_factory=datetime.now)