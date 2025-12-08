# DB와 직접 상호작용하는 Health CRUD 함수들
# 시계열 건강 측정 데이터

from motor.motor_asyncio import AsyncIOMotorDatabase
from models.healthModel import HealthRecordDB
from typing import Optional, List
from bson import ObjectId

# 건강 측정 데이터 생성
async def create_health_record(db: AsyncIOMotorDatabase, health_record: HealthRecordDB) -> HealthRecordDB:
    """새로운 건강 측정 데이터를 DB에 저장"""
    health_dict = health_record.model_dump(by_alias=True)
    if health_dict["_id"] == "":
        health_dict["_id"] = str(ObjectId())
    
    await db.health_records.insert_one(health_dict)
    return health_record

# 사용자 ID로 건강 측정 데이터 조회
async def get_health_records_by_user_id(db: AsyncIOMotorDatabase, user_id: str) -> List[HealthRecordDB]:
    """특정 사용자의 모든 건강 측정 데이터 조회 (최신순)"""
    records = []
    cursor = db.health_records.find({"user_id": user_id}).sort("created_at", -1)
    async for record in cursor:
        records.append(HealthRecordDB(**record))
    return records

# 건강 측정 데이터 ID로 조회
async def get_health_record_by_id(db: AsyncIOMotorDatabase, record_id: str) -> Optional[HealthRecordDB]:
    """ID로 건강 측정 데이터 조회"""
    record = await db.health_records.find_one({"_id": record_id})
    if record:
        return HealthRecordDB(**record)
    return None

# 최신 건강 측정 데이터 조회
async def get_latest_health_record(db: AsyncIOMotorDatabase, user_id: str) -> Optional[HealthRecordDB]:
    """사용자의 가장 최근 건강 측정 데이터 조회"""
    record = await db.health_records.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )
    if record:
        return HealthRecordDB(**record)
    return None

# 건강 측정 데이터 삭제
async def delete_health_record(db: AsyncIOMotorDatabase, record_id: str) -> Optional[HealthRecordDB]:
    """건강 측정 데이터 삭제"""
    record = await db.health_records.find_one({"_id": record_id})
    if record:
        result = await db.health_records.delete_one({"_id": record_id})
        return HealthRecordDB(**record) if result.deleted_count > 0 else None
    return None