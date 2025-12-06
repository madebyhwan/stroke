# HealthService에 대응
# health record 관련 비즈니스 로직을 처리하는 모듈

from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.healthSchema import HealthRecordInput, HealthRecordResponse
from models.healthModel import HealthRecordDB
from crud import healthCrud
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

# 건강 기록 생성
async def create_health_record(db: AsyncIOMotorDatabase, health_input: HealthRecordInput) -> HealthRecordResponse:
    """새로운 건강 기록 생성 (시계열 측정 데이터)"""
    # HealthRecordDB 모델로 변환
    health_db = HealthRecordDB(
        id=str(ObjectId()),
        user_id=health_input.user_id,
        weight_kg=health_input.weight_kg,
        systolic_bp=health_input.systolic_bp,
        diastolic_bp=health_input.diastolic_bp,
        glucose_level=health_input.glucose_level,
        smoking=health_input.smoking,
        created_at=datetime.now()
    )
    
    # DB 저장
    created = await healthCrud.create_health_record(db, health_db)
    
    # 응답 변환
    return HealthRecordResponse(
        id=created.id,
        user_id=created.user_id,
        weight_kg=created.weight_kg,
        systolic_bp=created.systolic_bp,
        diastolic_bp=created.diastolic_bp,
        glucose_level=created.glucose_level,
        smoking=created.smoking,
        created_at=created.created_at
    )

# 사용자의 건강 기록 목록 조회
async def get_user_health_records(db: AsyncIOMotorDatabase, user_id: str) -> List[HealthRecordResponse]:
    """특정 사용자의 건강 기록 목록 조회"""
    health_list = await healthCrud.get_health_records_by_user_id(db, user_id)
    
    return [
        HealthRecordResponse(
            id=h.id,
            user_id=h.user_id,
            weight_kg=h.weight_kg,
            systolic_bp=h.systolic_bp,
            diastolic_bp=h.diastolic_bp,
            glucose_level=h.glucose_level,
            smoking=h.smoking,
            created_at=h.created_at
        )
        for h in health_list
    ]

# 최신 건강 기록 조회
async def get_latest_health_record(db: AsyncIOMotorDatabase, user_id: str) -> Optional[HealthRecordResponse]:
    """사용자의 가장 최근 건강 기록 조회"""
    latest = await healthCrud.get_latest_health_record(db, user_id)
    if not latest:
        return None
    
    return HealthRecordResponse(
        id=latest.id,
        user_id=latest.user_id,
        weight_kg=latest.weight_kg,
        systolic_bp=latest.systolic_bp,
        diastolic_bp=latest.diastolic_bp,
        glucose_level=latest.glucose_level,
        smoking=latest.smoking,
        created_at=latest.created_at
    )

# 건강 기록 삭제
async def delete_health_record(db: AsyncIOMotorDatabase, record_id: str) -> bool:
    """건강 기록 삭제"""
    return await healthCrud.delete_health_record(db, record_id)

# 모니터링 권한으로 환자 건강 기록 조회
async def get_monitored_patient_records(
    db: AsyncIOMotorDatabase, 
    monitor_id: str, 
    patient_id: str
) -> List[HealthRecordResponse]:
    """모니터링 권한이 있는 사용자가 환자의 건강 기록 조회"""
    from crud import monitoringCrud
    
    # 모니터링 관계 확인
    relation_exists = await monitoringCrud.relation_exists(db, patient_id, monitor_id)
    if not relation_exists:
        raise ValueError("해당 환자에 대한 모니터링 권한이 없습니다.")
    
    # 권한이 확인되면 건강 기록 조회
    return await get_user_health_records(db, patient_id)

# 모니터링 권한으로 환자 최신 건강 기록 조회
async def get_monitored_patient_latest_record(
    db: AsyncIOMotorDatabase, 
    monitor_id: str, 
    patient_id: str
) -> Optional[HealthRecordResponse]:
    """모니터링 권한이 있는 사용자가 환자의 최신 건강 기록 조회"""
    from crud import monitoringCrud
    
    # 모니터링 관계 확인
    relation_exists = await monitoringCrud.relation_exists(db, patient_id, monitor_id)
    if not relation_exists:
        raise ValueError("해당 환자에 대한 모니터링 권한이 없습니다.")
    
    # 권한이 확인되면 최신 건강 기록 조회
    return await get_latest_health_record(db, patient_id)