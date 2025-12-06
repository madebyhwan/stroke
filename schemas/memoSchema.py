# client와 server 간에 주고받는 memo data의 스키마 정의

from pydantic import BaseModel
from datetime import datetime

class MemoBase(BaseModel):
    doctor_id: str
    patient_id: str
    content: str

class MemoCreate(MemoBase):
    pass

class MemoResponse(MemoBase):
    id: str
    created_at: datetime