# DB와 직접 상호작용하는 Memo CRUD 함수들

from motor.motor_asyncio import AsyncIOMotorDatabase
from models.memoModel import MemoDB
from typing import Optional, List
from datetime import datetime

# 메모 생성
async def create_memo(db: AsyncIOMotorDatabase, memo: MemoDB) -> MemoDB:
    """새로운 메모를 DB에 저장"""
    memo_dict = memo.model_dump(by_alias=True)
    await db.memos.insert_one(memo_dict)
    return memo

# 메모 ID로 조회
async def get_memo_by_id(db: AsyncIOMotorDatabase, memo_id: str) -> Optional[MemoDB]:
    """ID로 메모 조회"""
    memo_data = await db.memos.find_one({"_id": memo_id})
    if memo_data:
        return MemoDB(**memo_data)
    return None

# 특정 의사가 작성한 메모 조회
async def get_memos_by_doctor(db: AsyncIOMotorDatabase, doctor_id: str) -> List[MemoDB]:
    """특정 의사가 작성한 모든 메모 조회"""
    memos = []
    cursor = db.memos.find({"doctor_id": doctor_id}).sort("created_at", -1)
    async for memo_data in cursor:
        memos.append(MemoDB(**memo_data))
    return memos

# 특정 환자에 대한 메모 조회
async def get_memos_by_patient(db: AsyncIOMotorDatabase, patient_id: str) -> List[MemoDB]:
    """특정 환자에 대한 모든 메모 조회"""
    memos = []
    cursor = db.memos.find({"patient_id": patient_id}).sort("created_at", -1)
    async for memo_data in cursor:
        memos.append(MemoDB(**memo_data))
    return memos

# 특정 의사가 특정 환자에 대해 작성한 메모 조회
async def get_memos_by_doctor_and_patient(
    db: AsyncIOMotorDatabase, 
    doctor_id: str, 
    patient_id: str
) -> List[MemoDB]:
    """특정 의사가 특정 환자에 대해 작성한 메모 조회"""
    memos = []
    cursor = db.memos.find({
        "doctor_id": doctor_id,
        "patient_id": patient_id
    }).sort("created_at", -1)
    async for memo_data in cursor:
        memos.append(MemoDB(**memo_data))
    return memos

# 메모 삭제
async def delete_memo(db: AsyncIOMotorDatabase, memo_id: str) -> bool:
    """메모 삭제"""
    result = await db.memos.delete_one({"_id": memo_id})
    return result.deleted_count > 0
