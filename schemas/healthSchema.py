# client와 server 간에 주고받는 health data의 스키마 정의
# 시계열 건강 측정 데이터

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthRecordInput(BaseModel):
    """건강 측정 데이터 입력"""
    user_id: str
    weight_kg: float    # 체중 (kg)
    systolic_bp: int    # 수축기 혈압 (mmHg)
    diastolic_bp: int   # 이완기 혈압 (mmHg)
    glucose_level: int  # 혈당 (mg/dL)
    smoking: int        # 흡연량 (개비/일)

class HealthRecordResponse(HealthRecordInput):
    """건강 측정 데이터 응답"""
    id: str
    created_at: datetime
    stroke_risk_score: Optional[float] = None  # 뇌졸중 위험도 점수
    stroke_risk_level: Optional[str] = None    # 위험도 등급
