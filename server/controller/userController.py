# UserController에 대응
# user 관련 요청을 처리하는 모듈

from fastapi import APIRouter, Depends, HTTPException, Request
from schemas.userSchema import UserCreate, UserResponse, UserUpdate, UserLogin, UserHealthInfoResponse, UserHealthInfoUpdate
from services import userService

router = APIRouter()

# 의존성: DB 가져오기
def get_db(request: Request):
    return request.app.mongodb

# 회원가입
@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db=Depends(get_db)):
    """
    새로운 사용자 등록
    - **id**: 사용자 아이디
    - **password**: 비밀번호
    - **name**: 이름
    - **role**: 역할 (PATIENT, DOCTOR, CAREGIVER)
    """
    try:
        user = await userService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"회원가입 실패: {str(e)}")

# 로그인
@router.post("/login", response_model=UserResponse)
async def login(login_data: UserLogin, db=Depends(get_db)):
    """
    사용자 로그인
    - **id**: 사용자 아이디
    - **password**: 비밀번호
    """
    user = await userService.login_user(db, login_data)
    if not user:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못되었습니다.")
    return user

# 사용자 정보 조회
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db=Depends(get_db)):
    """
    사용자 정보 조회
    - **user_id**: 사용자 아이디
    """
    user = await userService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user

# 사용자 정보 수정
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserUpdate, db=Depends(get_db)):
    """
    사용자 정보 수정
    - **user_id**: 사용자 아이디
    - **user_data**: 수정할 사용자 정보 (일부 필드만 전송 가능)
    """
    # ID 일치 확인
    if user_data.id != user_id:
        raise HTTPException(status_code=400, detail="요청 경로의 user_id와 본문의 id가 일치하지 않습니다.")
    
    # None이 아닌 필드만 추출
    update_dict = user_data.model_dump(exclude_unset=True, exclude={"id"})
    
    updated_user = await userService.update_user(db, user_id, update_dict)
    if not updated_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return updated_user

# 사용자 건강 정보 조회
@router.get("/{user_id}/health", response_model=UserHealthInfoResponse)
async def get_user_health_info(user_id: str, db=Depends(get_db)):
    """
    사용자 기본 건강 정보 조회
    - **user_id**: 사용자 아이디
    """
    health_info = await userService.get_user_health_info(db, user_id)
    if not health_info:
        raise HTTPException(status_code=404, detail="사용자의 건강 정보를 찾을 수 없습니다.")
    return health_info

# 사용자 건강 정보 수정
@router.put("/{user_id}/health", response_model=UserHealthInfoResponse)
async def update_user_health_info(user_id: str, health_data: UserHealthInfoUpdate, db=Depends(get_db)):
    """
    사용자 기본 건강 정보 수정
    - **user_id**: 사용자 아이디
    - **health_data**: 수정할 건강 정보 (일부 필드만 전송 가능)
    """
    # ID 일치 확인
    if health_data.id != user_id:
        raise HTTPException(status_code=400, detail="요청 경로의 user_id와 본문의 id가 일치하지 않습니다.")
    
    # None이 아닌 필드만 추출
    update_dict = health_data.model_dump(exclude_unset=True, exclude={"id"})
    
    updated_info = await userService.update_user_health_info(db, user_id, update_dict)
    if not updated_info:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return updated_info
