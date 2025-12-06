# client와 server 간에 주고받는 monitoring data의 스키마 정의

from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class MonitoringStatus(str, Enum):
    PENDING = "PENDING"      # 대기 중
    APPROVED = "APPROVED"    # 승인됨
    REJECTED = "REJECTED"    # 거부됨

class MonitoringRequestCreate(BaseModel):
    """모니터링 요청 생성 (의사/보호자 → 환자)"""
    patient_id: str          # 모니터링 대상 환자 ID
    requester_id: str        # 요청자 ID (의사/보호자)

class MonitoringRequestResponse(BaseModel):
    """모니터링 요청 조회 (승인 전 - PENDING 상태)"""
    id: str
    patient_id: str             # 환자 ID
    patient_name: str           # 환자 이름
    requester_id: str           # 요청자 ID (의사/보호자)
    requester_name: str         # 요청자 이름
    requester_role: str         # 요청자 역할 (DOCTOR/CAREGIVER)
    status: MonitoringStatus    # PENDING, APPROVED, REJECTED
    created_at: datetime        # 요청 시간
    responded_at: Optional[datetime]    # 응답 시간

class MonitoringApproval(BaseModel):
    """모니터링 승인/거부 처리"""
    request_id: str
    approved: bool           # True: 승인, False: 거부

class MonitoringRelationResponse(BaseModel):
    """승인된 모니터링 관계 (APPROVED만)"""
    id: str
    patient_id: str
    patient_name: str
    monitor_id: str          # 모니터링하는 사용자 ID
    monitor_name: str
    monitor_role: str        # DOCTOR/CAREGIVER
    granted_at: datetime     # 승인된 시간