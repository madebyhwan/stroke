# MonitoringService에 대응
# monitoring 관련 비즈니스 로직을 처리하는 모듈

from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.monitoringSchema import (
    MonitoringRequestCreate, 
    MonitoringRequestResponse, 
    MonitoringApproval,
    MonitoringRelationResponse,
    MonitoringStatus
)
from models.monitoringModel import MonitoringRequestDB, MonitoringRelationDB
from crud import monitoringCrud, userCrud
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

# ==================== 모니터링 요청 ====================

async def create_monitoring_request(
    db: AsyncIOMotorDatabase, 
    request_data: MonitoringRequestCreate
) -> MonitoringRequestResponse:
    """새로운 모니터링 요청 생성"""
    # 환자와 요청자 확인
    patient = await userCrud.get_user_by_id(db, request_data.patient_id)
    if not patient:
        raise ValueError("환자를 찾을 수 없습니다.")
    
    # 환자 역할 확인
    if patient.role != "PATIENT":
        raise ValueError("환자 역할의 사용자에게만 요청할 수 있습니다.")
    
    requester = await userCrud.get_user_by_id(db, request_data.requester_id)
    if not requester:
        raise ValueError("요청자를 찾을 수 없습니다.")
    
    # 요청자 역할 확인
    if requester.role not in ["DOCTOR", "CAREGIVER"]:
        raise ValueError("의사 또는 보호자만 모니터링을 요청할 수 있습니다.")
    
    # 이미 대기중인 요청이 있는지 확인
    existing_requests = await monitoringCrud.request_exists(
        db,
        request_data.patient_id,
        request_data.requester_id
    )
    if existing_requests:
        raise ValueError("이미 대기 중인 요청이 존재합니다.")
    
    # 이미 관계가 존재하는지 확인
    relation_exists = await monitoringCrud.relation_exists(
        db, 
        request_data.patient_id, 
        request_data.requester_id
    )
    if relation_exists:
        raise ValueError("이미 모니터링 관계가 존재합니다.")
    
    # DB 모델로 변환
    request_db = MonitoringRequestDB(
        id=str(ObjectId()),
        patient_id=request_data.patient_id,
        requester_id=request_data.requester_id,
        status=MonitoringStatus.PENDING,
        created_at=datetime.now(),
        responded_at=None
    )
    
    # DB 저장
    created = await monitoringCrud.create_monitoring_request(db, request_db)
    
    # 응답 변환
    return MonitoringRequestResponse(
        id=created.id,
        patient_id=created.patient_id,
        patient_name=patient.name,
        requester_id=created.requester_id,
        requester_name=requester.name,
        requester_role=requester.role,
        status=created.status,
        created_at=created.created_at,
        responded_at=created.responded_at
    )

async def get_pending_requests_for_patient(
    db: AsyncIOMotorDatabase, 
    patient_id: str
) -> List[MonitoringRequestResponse]:
    """환자가 받은 대기 중인 모니터링 요청 목록"""
    requests = await monitoringCrud.get_pending_requests_for_patient(db, patient_id)
    
    result = []
    for req in requests:
        requester = await userCrud.get_user_by_id(db, req.requester_id)
        if requester:
            result.append(MonitoringRequestResponse(
                id=req.id,
                patient_id=req.patient_id,
                patient_name="",  # 환자 본인이므로 불필요
                requester_id=req.requester_id,
                requester_name=requester.name,
                requester_role=requester.role,
                status=req.status,
                created_at=req.created_at,
                responded_at=req.responded_at
            ))
    
    return result

async def get_requests_by_requester(
    db: AsyncIOMotorDatabase, 
    requester_id: str
) -> List[MonitoringRequestResponse]:
    """의사/보호자가 보낸 모니터링 요청 목록"""
    requests = await monitoringCrud.get_requests_by_requester(db, requester_id)
    
    result = []
    for req in requests:
        patient = await userCrud.get_user_by_id(db, req.patient_id)
        if patient:
            result.append(MonitoringRequestResponse(
                id=req.id,
                patient_id=req.patient_id,
                patient_name=patient.name,
                requester_id=req.requester_id,
                requester_name="",  # 본인이므로 불필요
                requester_role="",
                status=req.status,
                created_at=req.created_at,
                responded_at=req.responded_at
            ))
    
    return result

async def approve_monitoring_request(
    db: AsyncIOMotorDatabase, 
    approval_data: MonitoringApproval
) -> MonitoringRequestResponse:
    """모니터링 요청 승인/거부 처리"""
    # 요청 확인
    request = await monitoringCrud.get_request_by_id(db, approval_data.request_id)
    if not request:
        raise ValueError("요청을 찾을 수 없습니다.")
    
    if request.status != MonitoringStatus.PENDING:
        raise ValueError("이미 처리된 요청입니다.")
    
    # 상태 업데이트
    new_status = MonitoringStatus.APPROVED if approval_data.approved else MonitoringStatus.REJECTED
    success = await monitoringCrud.update_request_status(db, approval_data.request_id, new_status)
    
    if not success:
        raise ValueError("요청 처리에 실패했습니다.")
    
    # 승인된 경우 관계 생성
    if approval_data.approved:
        relation = MonitoringRelationDB(
            id=str(ObjectId()),
            patient_id=request.patient_id,
            monitor_id=request.requester_id,
            request_id=request.id,
            granted_at=datetime.now()
        )
        await monitoringCrud.create_monitoring_relation(db, relation)
    
    # 업데이트된 요청 조회
    updated_request = await monitoringCrud.get_request_by_id(db, approval_data.request_id)
    patient = await userCrud.get_user_by_id(db, updated_request.patient_id)
    requester = await userCrud.get_user_by_id(db, updated_request.requester_id)
    
    return MonitoringRequestResponse(
        id=updated_request.id,
        patient_id=updated_request.patient_id,
        patient_name=patient.name if patient else "",
        requester_id=updated_request.requester_id,
        requester_name=requester.name if requester else "",
        requester_role=requester.role if requester else "",
        status=updated_request.status,
        created_at=updated_request.created_at,
        responded_at=updated_request.responded_at
    )

# ==================== 모니터링 관계 ====================

async def get_patient_relations(
    db: AsyncIOMotorDatabase, 
    patient_id: str
) -> List[MonitoringRelationResponse]:
    """환자의 승인된 모니터링 관계 목록"""
    relations = await monitoringCrud.get_relations_by_patient(db, patient_id)
    
    result = []
    for rel in relations:
        monitor = await userCrud.get_user_by_id(db, rel.monitor_id)
        if monitor:
            result.append(MonitoringRelationResponse(
                id=rel.id,
                patient_id=rel.patient_id,
                patient_name="",  # 환자 본인
                monitor_id=rel.monitor_id,
                monitor_name=monitor.name,
                monitor_role=monitor.role,
                granted_at=rel.granted_at
            ))
    
    return result

async def get_my_patients(
    db: AsyncIOMotorDatabase, 
    monitor_id: str
) -> List[MonitoringRelationResponse]:
    """의사/보호자가 모니터링하는 환자 목록"""
    relations = await monitoringCrud.get_patients_by_monitor(db, monitor_id)
    
    result = []
    for rel in relations:
        patient = await userCrud.get_user_by_id(db, rel.patient_id)
        if patient:
            result.append(MonitoringRelationResponse(
                id=rel.id,
                patient_id=rel.patient_id,
                patient_name=patient.name,
                monitor_id=rel.monitor_id,
                monitor_name="",  # 본인
                monitor_role="",
                granted_at=rel.granted_at
            ))
    
    return result

async def delete_monitoring_relation(
    db: AsyncIOMotorDatabase, 
    relation_id: str
) -> bool:
    """모니터링 관계 해제"""
    # 관계 존재 확인
    relation = await monitoringCrud.get_relation_by_id(db, relation_id)
    if not relation:
        raise ValueError("모니터링 관계를 찾을 수 없습니다.")
    
    # 관계 삭제
    deleted = await monitoringCrud.delete_monitoring_relation(db, relation_id)
    
    # 해당 관계와 연결된 요청도 삭제
    if relation.request_id:
        await monitoringCrud.delete_request_by_id(db, relation.request_id)
    
    return deleted

async def delete_monitoring_request(
    db: AsyncIOMotorDatabase, 
    request_id: str
) -> bool:
    """모니터링 요청 삭제 (취소)"""
    # 요청 존재 확인
    request = await monitoringCrud.get_request_by_id(db, request_id)
    if not request:
        raise ValueError("요청을 찾을 수 없습니다.")
    
    # PENDING 상태만 삭제 가능
    if request.status != MonitoringStatus.PENDING:
        raise ValueError("대기 중인 요청만 취소할 수 있습니다.")
    
    # 요청 삭제
    deleted = await monitoringCrud.delete_request_by_id(db, request_id)
    return deleted
