# DB와 상호작용하는 Health 모델을 정의
# 시계열 건강 측정 데이터 (자주 변경되는 데이터)

from pydantic import BaseModel, Field
from datetime import datetime

class HealthRecordDB(BaseModel):
    """시계열 건강 측정 기록"""
    id: str = Field(..., alias="_id")
    user_id: str                # users 컬렉션 참조
    weight_kg: int = 70         # 체중
    systolic_bp: int = 120      # 수축기 혈압
    diastolic_bp: int = 80      # 이완기 혈압
    glucose_level: int = 100    # 혈당
    smoking: int = 0            # 흡연량 (개비/일)
    
    created_at: datetime = Field(default_factory=datetime.now)