# DB와 상호작용하는 Monitoring 모델을 정의
# MongoDB에 실제로 저장될 형태 정의

from pydantic import BaseModel, Field
from datetime import datetime
from server.schemas.monitoringSchema import MonitoringStatus
from typing import Optional

class MonitoringRequestDB(BaseModel):
    """모니터링 요청 DB 모델 (모든 요청 이력 보관)"""
    id: str = Field(..., alias="_id")
    patient_id: str          # 환자 ID
    requester_id: str        # 요청자 ID (의사/보호자)
    status: MonitoringStatus # PENDING, APPROVED, REJECTED
    created_at: datetime = Field(default_factory=datetime.now)
    responded_at: Optional[datetime] = None  # 응답 시간

class MonitoringRelationDB(BaseModel):
    """승인된 모니터링 관계 DB 모델 (활성 관계만 저장)"""
    id: str = Field(..., alias="_id")
    patient_id: str          # 환자 ID
    monitor_id: str          # 모니터링하는 사용자 ID
    request_id: str          # 원본 요청 ID (참조용)
    granted_at: datetime = Field(default_factory=datetime.now)