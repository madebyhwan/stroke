# DB와 상호작용하는 Health 모델을 정의
# 시계열 건강 측정 데이터 (자주 변경되는 데이터)

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class HealthRecordDB(BaseModel):
    """시계열 건강 측정 기록"""
    id: str = Field(..., alias="_id")
    user_id: str                # users 컬렉션 참조
    weight_kg: float = 70.0     # 체중
    systolic_bp: int = 120      # 수축기 혈압
    diastolic_bp: int = 80      # 이완기 혈압
    glucose_level: int = 100    # 혈당
    smoking: int = 0            # 흡연량 (개비/일)
    
    # 계산된 위험도
    stroke_risk_score: Optional[float] = None  # 뇌졸중 위험도 점수 (0-100)
    stroke_risk_level: Optional[str] = None    # 위험도 등급 (낮음, 보통, 높음, 매우 높음)
    
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True  # id와 _id 모두 허용
