# HealthDataController에 대응
# health data 관련 요청을 처리하는 모듈
# 시계열 건강 측정 데이터

from fastapi import APIRouter, Depends, HTTPException, Request
from schemas.healthSchema import HealthRecordInput, HealthRecordResponse
from services import healthService
from typing import List

router = APIRouter()

# 의존성: DB 가져오기
def get_db(request: Request):
    return request.app.mongodb

# 건강 측정 데이터 생성
@router.post("/records", response_model=HealthRecordResponse, status_code=201)
async def create_health_record(record_input: HealthRecordInput, db=Depends(get_db)):
    """
    새로운 건강 측정 데이터 생성
    - **user_id**: 사용자 ID
    - **weight_kg**: 몸무게 (kg)
    - **systolic_bp**: 수축기 혈압 (mmHg)
    - **diastolic_bp**: 이완기 혈압 (mmHg)
    - **glucose_level**: 혈당 (mg/dL)
    - **smoking**: 흡연량 (개비/일)
    """
    try:
        record = await healthService.create_health_record(db, record_input)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"건강 측정 데이터 생성 실패: {str(e)}")

# 사용자별 건강 측정 데이터 조회
@router.get("/records/user/{user_id}", response_model=List[HealthRecordResponse])
async def get_user_health_records(user_id: str, db=Depends(get_db)):
    """
    특정 사용자의 건강 측정 데이터 목록 조회 (최신순)
    - **user_id**: 사용자 ID
    """
    records = await healthService.get_user_health_records(db, user_id)
    return records

# 최신 건강 측정 데이터 조회
@router.get("/records/user/{user_id}/latest", response_model=HealthRecordResponse)
async def get_latest_health_record(user_id: str, db=Depends(get_db)):
    """
    사용자의 가장 최근 건강 측정 데이터 조회
    - **user_id**: 사용자 ID
    """
    record = await healthService.get_latest_health_record(db, user_id)
    if not record:
        raise HTTPException(status_code=404, detail="건강 측정 데이터를 찾을 수 없습니다.")
    return record

# 건강 측정 데이터 삭제
@router.delete("/records/{record_id}", status_code=204)
async def delete_health_record(record_id: str, db=Depends(get_db)):
    """
    건강 측정 데이터 삭제
    - **record_id**: 건강 측정 데이터 ID
    """
    success = await healthService.delete_health_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="건강 측정 데이터를 찾을 수 없습니다.")
    return None
