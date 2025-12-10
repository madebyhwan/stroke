# HealthService에 대응
# health record 관련 비즈니스 로직을 처리하는 모듈

from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.healthSchema import HealthRecordInput, HealthRecordResponse
from models.healthModel import HealthRecordDB
from crud import healthCrud, userCrud
from core.riskCalculator import calculate_stroke_risk, get_risk_level, calculate_age
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

# 건강 기록 생성
async def create_health_record(db: AsyncIOMotorDatabase, health_input: HealthRecordInput) -> HealthRecordResponse:
    """새로운 건강 기록 생성 (시계열 측정 데이터) + 위험도 계산"""
    
    # 사용자 정보 조회 (위험도 계산을 위해 필요)
    user = await userCrud.get_user_by_id(db, health_input.user_id)
    if not user:
        raise ValueError("사용자를 찾을 수 없습니다.")
    
    # 나이 계산
    age = calculate_age(user.birth_date) if user.birth_date else 50
    
    # 위험도 계산
    risk_score = calculate_stroke_risk(
        age=age,
        sex=user.sex.value if hasattr(user.sex, 'value') else user.sex,
        stroke_history=user.stroke_history,
        hypertension=user.hypertension,
        heart_disease=user.heart_disease,
        diabetes=user.diabetes,
        smoking_history=user.smoking_history.value if hasattr(user.smoking_history, 'value') else user.smoking_history,
        systolic_bp=health_input.systolic_bp,
        diastolic_bp=health_input.diastolic_bp,
        weight_kg=health_input.weight_kg,
        height_cm=user.height_cm,
        glucose_level=health_input.glucose_level,
        smoking=health_input.smoking
    )
    
    risk_level = get_risk_level(risk_score)
    
    # HealthRecordDB 모델로 변환
    health_db = HealthRecordDB(
        id=str(ObjectId()),
        user_id=health_input.user_id,
        weight_kg=health_input.weight_kg,
        systolic_bp=health_input.systolic_bp,
        diastolic_bp=health_input.diastolic_bp,
        glucose_level=health_input.glucose_level,
        smoking=health_input.smoking,
        stroke_risk_score=risk_score,
        stroke_risk_level=risk_level,
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
        stroke_risk_score=created.stroke_risk_score,
        stroke_risk_level=created.stroke_risk_level,
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
            stroke_risk_score=h.stroke_risk_score,
            stroke_risk_level=h.stroke_risk_level,
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
        stroke_risk_score=latest.stroke_risk_score,
        stroke_risk_level=latest.stroke_risk_level,
        created_at=latest.created_at
    )

# 건강 기록 삭제
async def delete_health_record(db: AsyncIOMotorDatabase, record_id: str) -> Optional[HealthRecordResponse]:
    """건강 기록 삭제"""
    deleted_record = await healthCrud.delete_health_record(db, record_id)
    if not deleted_record:
        return None
    
    return HealthRecordResponse(
        id=deleted_record.id,
        user_id=deleted_record.user_id,
        weight_kg=deleted_record.weight_kg,
        systolic_bp=deleted_record.systolic_bp,
        diastolic_bp=deleted_record.diastolic_bp,
        glucose_level=deleted_record.glucose_level,
        smoking=deleted_record.smoking,
        stroke_risk_score=deleted_record.stroke_risk_score,
        stroke_risk_level=deleted_record.stroke_risk_level,
        created_at=deleted_record.created_at
    )

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