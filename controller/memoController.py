# MemoController에 대응
# memo 관련 요청을 처리하는 모듈

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from schemas.memoSchema import MemoCreate, MemoResponse
from services import memoService
from typing import List, Optional

router = APIRouter()

# 의존성: DB 가져오기
def get_db(request: Request):
    return request.app.mongodb

# 메모 생성
@router.post("", response_model=MemoResponse, status_code=201)
async def create_memo(memo_data: MemoCreate, db=Depends(get_db)):
    """
    새로운 메모 생성
    - **doctor_id**: 의사 ID (작성자)
    - **patient_id**: 환자 ID (대상)
    - **content**: 메모 내용
    """
    try:
        memo = await memoService.create_memo(db, memo_data)
        return memo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메모 생성 실패: {str(e)}")

# 메모 ID로 조회
@router.get("/{memo_id}", response_model=MemoResponse)
async def get_memo(memo_id: str, db=Depends(get_db)):
    """
    메모 ID로 단건 조회
    - **memo_id**: 메모 ID
    """
    memo = await memoService.get_memo(db, memo_id)
    if not memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    return memo

# 메모 목록 조회 (다양한 필터)
@router.get("", response_model=List[MemoResponse])
async def get_memos(
    doctor_id: Optional[str] = Query(None, description="의사 ID로 필터링"),
    patient_id: Optional[str] = Query(None, description="환자 ID로 필터링"),
    db=Depends(get_db)
):
    """
    메모 목록 조회
    - **doctor_id**: (선택) 특정 의사가 작성한 메모만 조회
    - **patient_id**: (선택) 특정 환자에 대한 메모만 조회
    - 두 파라미터 모두 제공 시: 특정 의사가 특정 환자에 대해 작성한 메모 조회
    """
    try:
        if doctor_id and patient_id:
            # 특정 의사가 특정 환자에 대해 작성한 메모
            memos = await memoService.get_memos_by_doctor_and_patient(db, doctor_id, patient_id)
        elif doctor_id:
            # 특정 의사가 작성한 모든 메모
            memos = await memoService.get_memos_by_doctor(db, doctor_id)
        elif patient_id:
            # 특정 환자에 대한 모든 메모
            memos = await memoService.get_memos_by_patient(db, patient_id)
        else:
            raise HTTPException(status_code=400, detail="doctor_id 또는 patient_id 중 최소 하나를 제공해야 합니다.")
        
        return memos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메모 조회 실패: {str(e)}")

# 메모 삭제
@router.delete("/{memo_id}", status_code=204)
async def delete_memo(
    memo_id: str,
    doctor_id: str = Query(..., description="삭제 요청자(의사) ID"),
    db=Depends(get_db)
):
    """
    메모 삭제 (작성자만 가능)
    - **memo_id**: 메모 ID
    - **doctor_id**: 삭제 요청자 ID (작성자와 일치해야 함)
    """
    try:
        success = await memoService.delete_memo(db, memo_id, doctor_id)
        if not success:
            raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
        return None
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메모 삭제 실패: {str(e)}")
