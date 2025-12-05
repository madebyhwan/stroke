# DB와 상호작용하는 User 모델을 정의
# MongoDB에 실제로 저장될 형태 정의

from pydantic import BaseModel, Field
from datetime import datetime

from server.schemas.userSchema import UserRole

class UserDB(BaseModel):
    id: str = Field(..., alias="_id")
    hashed_password: str
    name: str
    role: UserRole
    created_at: datetime = Field(default_factory=datetime.now)