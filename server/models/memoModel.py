# DB와 상호작용하는 Memo 모델을 정의

from pydantic import BaseModel, Field
from datetime import datetime

class MemoDB(BaseModel):
    id: str = Field(..., alias="_id")
    doctor_id: str
    patient_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True  # id와 _id 모두 허용