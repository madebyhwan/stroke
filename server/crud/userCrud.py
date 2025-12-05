# DB와 직접 상호작용하는 User CRUD 함수들

from motor.motor_asyncio import AsyncIOMotorDatabase
from models.userModel import UserDB
from typing import Optional

# 사용자 생성
async def create_user(db: AsyncIOMotorDatabase, user: UserDB) -> UserDB:
    """새로운 사용자를 DB에 저장"""
    user_dict = user.model_dump(by_alias=True)
    await db.users.insert_one(user_dict)
    return user

# 사용자 ID로 조회
async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserDB]:
    """ID로 사용자 조회"""
    user_data = await db.users.find_one({"_id": user_id})
    if user_data:
        return UserDB(**user_data)
    return None

# 모든 사용자 조회
async def get_all_users(db: AsyncIOMotorDatabase) -> list[UserDB]:
    """모든 사용자 조회"""
    users = []
    cursor = db.users.find()
    async for user_data in cursor:
        users.append(UserDB(**user_data))
    return users

# 사용자 정보 업데이트
async def update_user(db: AsyncIOMotorDatabase, user_id: str, update_data: dict) -> bool:
    """사용자 정보 업데이트"""
    result = await db.users.update_one(
        {"_id": user_id},
        {"$set": update_data}
    )
    return result.modified_count > 0

# 사용자 삭제
async def delete_user(db: AsyncIOMotorDatabase, user_id: str) -> bool:
    """사용자 삭제"""
    result = await db.users.delete_one({"_id": user_id})
    return result.deleted_count > 0
