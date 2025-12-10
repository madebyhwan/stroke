# MemoService에 대응
# memo 관련 비즈니스 로직을 처리하는 모듈

from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.memoSchema import MemoCreate, MemoResponse
from models.memoModel import MemoDB
from crud import memoCrud, userCrud
from typing import Optional, List
from datetime import datetime
import uuid

# 메모 생성
async def create_memo(db: AsyncIOMotorDatabase, memo_data: MemoCreate) -> MemoResponse:
    """새로운 메모 생성"""
    # 의사 확인
    doctor = await userCrud.get_user_by_id(db, memo_data.doctor_id)
    if not doctor:
        raise ValueError("존재하지 않는 의사입니다.")
    if doctor.role != "DOCTOR":
        raise ValueError("의사만 메모를 작성할 수 있습니다.")
    
    # 환자 확인
    patient = await userCrud.get_user_by_id(db, memo_data.patient_id)
    if not patient:
        raise ValueError("존재하지 않는 환자입니다.")
    if patient.role != "PATIENT":
        raise ValueError("환자에 대해서만 메모를 작성할 수 있습니다.")
    
    # 메모 생성
    memo_id = str(uuid.uuid4())
    memo_db = MemoDB(
        id=memo_id,
        doctor_id=memo_data.doctor_id,
        patient_id=memo_data.patient_id,
        content=memo_data.content,
        created_at=datetime.now()
    )
    
    # DB 저장
    created_memo = await memoCrud.create_memo(db, memo_db)
    
    # 응답
    return MemoResponse(
        id=created_memo.id,
        doctor_id=created_memo.doctor_id,
        patient_id=created_memo.patient_id,
        content=created_memo.content,
        created_at=created_memo.created_at
    )

# 메모 조회 (ID로)
async def get_memo(db: AsyncIOMotorDatabase, memo_id: str) -> Optional[MemoResponse]:
    """메모 ID로 조회"""
    memo = await memoCrud.get_memo_by_id(db, memo_id)
    if not memo:
        return None
    
    return MemoResponse(
        id=memo.id,
        doctor_id=memo.doctor_id,
        patient_id=memo.patient_id,
        content=memo.content,
        created_at=memo.created_at
    )

# 특정 의사가 작성한 메모 목록 조회
async def get_memos_by_doctor(db: AsyncIOMotorDatabase, doctor_id: str) -> List[MemoResponse]:
    """특정 의사가 작성한 모든 메모 조회"""
    # 의사 확인
    doctor = await userCrud.get_user_by_id(db, doctor_id)
    if not doctor:
        raise ValueError("존재하지 않는 의사입니다.")
    if doctor.role != "DOCTOR":
        raise ValueError("의사만 조회할 수 있습니다.")
    
    memos = await memoCrud.get_memos_by_doctor(db, doctor_id)
    return [
        MemoResponse(
            id=memo.id,
            doctor_id=memo.doctor_id,
            patient_id=memo.patient_id,
            content=memo.content,
            created_at=memo.created_at
        )
        for memo in memos
    ]

# 특정 환자에 대한 메모 목록 조회
async def get_memos_by_patient(db: AsyncIOMotorDatabase, patient_id: str) -> List[MemoResponse]:
    """특정 환자에 대한 모든 메모 조회"""
    # 환자 확인
    patient = await userCrud.get_user_by_id(db, patient_id)
    if not patient:
        raise ValueError("존재하지 않는 환자입니다.")
    if patient.role != "PATIENT":
        raise ValueError("환자에 대해서만 조회할 수 있습니다.")
    
    memos = await memoCrud.get_memos_by_patient(db, patient_id)
    return [
        MemoResponse(
            id=memo.id,
            doctor_id=memo.doctor_id,
            patient_id=memo.patient_id,
            content=memo.content,
            created_at=memo.created_at
        )
        for memo in memos
    ]

# 특정 의사가 특정 환자에 대해 작성한 메모 조회
async def get_memos_by_doctor_and_patient(
    db: AsyncIOMotorDatabase, 
    doctor_id: str, 
    patient_id: str
) -> List[MemoResponse]:
    """특정 의사가 특정 환자에 대해 작성한 메모 조회"""
    # 의사 확인
    doctor = await userCrud.get_user_by_id(db, doctor_id)
    if not doctor or doctor.role != "DOCTOR":
        raise ValueError("유효하지 않은 의사입니다.")
    
    # 환자 확인
    patient = await userCrud.get_user_by_id(db, patient_id)
    if not patient or patient.role != "PATIENT":
        raise ValueError("유효하지 않은 환자입니다.")
    
    memos = await memoCrud.get_memos_by_doctor_and_patient(db, doctor_id, patient_id)
    return [
        MemoResponse(
            id=memo.id,
            doctor_id=memo.doctor_id,
            patient_id=memo.patient_id,
            content=memo.content,
            created_at=memo.created_at
        )
        for memo in memos
    ]

# 메모 삭제
async def delete_memo(db: AsyncIOMotorDatabase, memo_id: str, doctor_id: str) -> bool:
    """메모 삭제 (작성자만 가능)"""
    # 메모 확인
    memo = await memoCrud.get_memo_by_id(db, memo_id)
    if not memo:
        return False
    
    # 작성자 확인
    if memo.doctor_id != doctor_id:
        raise ValueError("본인이 작성한 메모만 삭제할 수 있습니다.")
    
    # 삭제
    return await memoCrud.delete_memo(db, memo_id)
