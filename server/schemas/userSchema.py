# client와 server 간에 주고받는 user data의 스키마 정의

from pydantic import BaseModel
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    CAREGIVER = "CAREGIVER"

class UserBase(BaseModel):
    id: str
    name: str
    role: UserRole

class UserCreate(UserBase):
    password: str  # 생성 시에만 필요

class UserResponse(UserBase):
    pass  # 비밀번호 제외

class UserLogin(BaseModel):
    id: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None