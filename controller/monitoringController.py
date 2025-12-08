# MonitoringController에 대응
# monitoring 관련 요청을 처리하는 모듈

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from schemas.monitoringSchema import (
    MonitoringRequestCreate,
    MonitoringRequestResponse,
    MonitoringApproval,
    MonitoringRelationResponse
)
from services import monitoringService
from typing import List

router = APIRouter()

# 의존성: DB 가져오기
def get_db(request: Request):
    return request.app.mongodb

# ==================== 모니터링 요청 ====================

# 모니터링 요청 생성
@router.post("/request", response_model=MonitoringRequestResponse, status_code=201)
async def create_monitoring_request(
    request_data: MonitoringRequestCreate,
    db=Depends(get_db)
):
    """
    새로운 모니터링 요청 생성 (의사/보호자 → 환자)
    - **patient_id**: 모니터링 대상 환자 ID
    - **requester_id**: 요청자 ID (의사/보호자)
    """
    try:
        request = await monitoringService.create_monitoring_request(db, request_data)
        return request
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"모니터링 요청 생성 실패: {str(e)}")

# 대기 중인 요청 조회 (환자용)
@router.get("/requests/pending/{patient_id}", response_model=List[MonitoringRequestResponse])
async def get_pending_requests(
    patient_id: str,
    db=Depends(get_db)
):
    """
    환자가 받은 대기 중인 모니터링 요청 목록
    - **patient_id**: 환자 ID
    """
    requests = await monitoringService.get_pending_requests_for_patient(db, patient_id)
    return requests

# 모니터가 보낸 요청 조회
@router.get("/requests/sent/{requester_id}", response_model=List[MonitoringRequestResponse])
async def get_sent_requests(
    requester_id: str,
    db=Depends(get_db)
):
    """
    의사/보호자가 보낸 모니터링 요청 목록
    - **requester_id**: 요청자 ID (의사/보호자)
    """
    requests = await monitoringService.get_requests_by_requester(db, requester_id)
    return requests

# 모니터링 요청 승인/거부
@router.post("/approve", response_model=MonitoringRequestResponse)
async def approve_request(
    approval_data: MonitoringApproval,
    db=Depends(get_db)
):
    """
    환자가 모니터링 요청 승인 또는 거부
    - **request_id**: 요청 ID
    - **approved**: True(승인), False(거부)
    """
    try:
        result = await monitoringService.approve_monitoring_request(db, approval_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요청 처리 실패: {str(e)}")

# 모니터링 요청 취소 (DELETE)
@router.delete("/request/{request_id}", status_code=204)
async def cancel_monitoring_request(
    request_id: str,
    db=Depends(get_db)
):
    """
    모니터링 요청 취소 (요청자가 대기 중인 요청 취소)
    - **request_id**: 요청 ID
    """
    try:
        deleted = await monitoringService.delete_monitoring_request(db, request_id)
        if not deleted:
            print(f"⚠️ 요청 삭제 실패: request_id={request_id}")
            raise HTTPException(status_code=500, detail=f"데이터베이스에서 요청(ID: {request_id})을 찾을 수 없거나 삭제에 실패했습니다.")
        return Response(status_code=204)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"❌ 요청 취소 오류: {e}")
        raise HTTPException(status_code=500, detail=f"요청 취소 실패: {str(e)}")

# ==================== 모니터링 관계 ====================

# 환자의 모니터링 관계 조회
@router.get("/relations/{patient_id}", response_model=List[MonitoringRelationResponse])
async def get_patient_relations(
    patient_id: str,
    db=Depends(get_db)
):
    """
    특정 환자의 승인된 모니터링 관계 목록
    - **patient_id**: 환자 ID
    """
    relations = await monitoringService.get_patient_relations(db, patient_id)
    return relations

# 내가 모니터링하는 환자 목록
@router.get("/my-patients/{monitor_id}", response_model=List[MonitoringRelationResponse])
async def get_my_patients(
    monitor_id: str,
    db=Depends(get_db)
):
    """
    의사/보호자가 모니터링 중인 환자 목록
    - **monitor_id**: 의사/보호자 ID
    """
    patients = await monitoringService.get_my_patients(db, monitor_id)
    return patients

# 모니터링 관계 해제
@router.delete("/relation/{relation_id}", status_code=204)
async def delete_relation(
    relation_id: str,
    db=Depends(get_db)
):
    """
    승인된 모니터링 관계 해제
    - **relation_id**: 관계 ID
    """
    try:
        deleted = await monitoringService.delete_monitoring_relation(db, relation_id)
        if not deleted:
            print(f"⚠️ 관계 삭제 실패: relation_id={relation_id}")
            raise HTTPException(status_code=500, detail=f"데이터베이스에서 관계(ID: {relation_id})를 찾을 수 없거나 삭제에 실패했습니다.")
        return Response(status_code=204)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"❌ 관계 해제 오류: {e}")
        raise HTTPException(status_code=500, detail=f"관계 해제 실패: {str(e)}")
