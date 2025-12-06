# UserService에 대응
# user 관련 비즈니스 로직을 처리하는 모듈

from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.userSchema import UserCreate, UserResponse, UserUpdate, UserLogin, UserHealthInfoResponse
from models.userModel import UserDB
from crud import userCrud
from typing import Optional

# 회원가입
async def register_user(db: AsyncIOMotorDatabase, user_data: UserCreate) -> UserResponse:
    """새로운 사용자 등록"""
    # 중복 확인
    existing_user = await userCrud.get_user_by_id(db, user_data.id)
    if existing_user:
        raise ValueError("이미 존재하는 아이디입니다.")

    # UserDB 모델로 변환
    user_db = UserDB(
        id=user_data.id,
        password=user_data.password,
        name=user_data.name,
        role=user_data.role
    )
    
    # DB 저장
    created_user = await userCrud.create_user(db, user_db)
    
    # 응답
    return UserResponse(
        id=created_user.id,
        name=created_user.name,
        role=created_user.role
    )

# 로그인
async def login_user(db: AsyncIOMotorDatabase, login_data: UserLogin) -> Optional[UserResponse]:
    """사용자 로그인"""
    # 사용자 조회
    user = await userCrud.get_user_by_id(db, login_data.id)
    if not user:
        return None
    
    # 비밀번호 검증
    if login_data.password != user.password:
        return None
    
    # 응답 (비밀번호 제외)
    return UserResponse(
        id=user.id,
        name=user.name,
        role=user.role
    )

# 사용자 조회
async def get_user(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserResponse]:
    """사용자 정보 조회"""
    user = await userCrud.get_user_by_id(db, user_id)
    if not user:
        return None
    
    return UserResponse(
        id=user.id,
        name=user.name,
        role=user.role
    )

# 사용자 정보 수정
async def update_user(db: AsyncIOMotorDatabase, user_id: str, update_dict: dict) -> Optional[UserResponse]:
    """사용자 정보 수정 (이름, 비밀번호만 가능)"""
    # 기존 사용자 확인
    existing_user = await userCrud.get_user_by_id(db, user_id)
    if not existing_user:
        return None
    
    # role 변경 시도 차단 (보안)
    if "role" in update_dict:
        del update_dict["role"]
    
    # updated_at 자동 설정
    from datetime import datetime
    update_dict["updated_at"] = datetime.now()
    
    # DB 업데이트
    success = await userCrud.update_user(db, user_id, update_dict)
    if not success:
        return None
    
    # 업데이트된 정보 조회
    updated_user = await userCrud.get_user_by_id(db, user_id)
    if not updated_user:
        return None
    
    return UserResponse(
        id=updated_user.id,
        name=updated_user.name,
        role=updated_user.role
    )

# 사용자 기본 건강 정보 조회
async def get_user_health_info(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserHealthInfoResponse]:
    """사용자의 기본 건강 정보 조회"""
    user = await userCrud.get_user_by_id(db, user_id)
    if not user:
        return None
    
    return UserHealthInfoResponse(
        sex=user.sex,
        birth_date=user.birth_date,
        height_cm=user.height_cm,
        stroke_history=user.stroke_history,
        hypertension=user.hypertension,
        heart_disease=user.heart_disease,
        smoking_history=user.smoking_history,
        diabetes=user.diabetes,
        measured_at=user.measured_at
    )

# 사용자 기본 건강 정보 수정
async def update_user_health_info(db: AsyncIOMotorDatabase, user_id: str, health_data: dict) -> Optional[UserHealthInfoResponse]:
    """사용자의 기본 건강 정보 수정"""
    # 기존 사용자 확인
    user = await userCrud.get_user_by_id(db, user_id)
    if not user:
        return None
    
    # measured_at 현재 시간으로 설정
    from datetime import datetime
    health_data['measured_at'] = datetime.now()
    
    # DB 업데이트
    success = await userCrud.update_user(db, user_id, health_data)
    if not success:
        return None
    
    # 업데이트된 정보 조회
    return await get_user_health_info(db, user_id)