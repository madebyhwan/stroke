# client와 server 간에 주고받는 user data의 스키마 정의

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from models.userModel import UserRole, sexEnum, smokingEnum

class UserBase(BaseModel):
    id: str
    name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    id: str
    password: str

class UserResponse(UserBase):
    pass

class UserUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    password: Optional[str] = None
    # role은 보안상 수정 불가 (관리자만 변경 가능하도록 별도 API 필요)
    # updated_at은 서버에서 자동 설정

class UserBaseHealthInfo(BaseModel):
    sex: sexEnum
    birth_date: date
    height_cm: int
    stroke_history: bool
    hypertension: bool
    heart_disease: bool
    smoking_history: smokingEnum
    diabetes: bool

class UserHealthInfoUpdate(BaseModel):
    id: str
    sex: Optional[sexEnum] = None
    birth_date: Optional[date] = None
    height_cm: Optional[int] = None
    stroke_history: Optional[bool] = None
    hypertension: Optional[bool] = None
    heart_disease: Optional[bool] = None
    smoking_history: Optional[smokingEnum] = None
    diabetes: Optional[bool] = None
    measured_at: Optional[datetime] = None

class UserHealthInfoResponse(UserBaseHealthInfo):
    measured_at: datetime