# DB와 직접 상호작용하는 Monitoring CRUD 함수들

from motor.motor_asyncio import AsyncIOMotorDatabase
from models.monitoringModel import MonitoringRequestDB, MonitoringRelationDB
from schemas.monitoringSchema import MonitoringStatus
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

# ==================== MonitoringRequest ====================

# 모니터링 요청 생성
async def create_monitoring_request(db: AsyncIOMotorDatabase, request: MonitoringRequestDB) -> MonitoringRequestDB:
    """새로운 모니터링 요청 생성"""
    request_dict = request.model_dump(by_alias=True)
    if request_dict["_id"] == "":
        request_dict["_id"] = str(ObjectId())
    
    await db.monitoring_requests.insert_one(request_dict)
    return request

# 요청 ID로 조회
async def get_request_by_id(db: AsyncIOMotorDatabase, request_id: str) -> Optional[MonitoringRequestDB]:
    """요청 ID로 모니터링 요청 조회"""
    request_data = await db.monitoring_requests.find_one({"_id": request_id})
    if request_data:
        return MonitoringRequestDB(**request_data)
    return None

# 환자가 받은 대기 중인 요청 조회
async def get_pending_requests_for_patient(db: AsyncIOMotorDatabase, patient_id: str) -> List[MonitoringRequestDB]:
    """특정 환자가 받은 대기 중인 모니터링 요청 목록"""
    requests = []
    cursor = db.monitoring_requests.find({
        "patient_id": patient_id,
        "status": MonitoringStatus.PENDING
    }).sort("created_at", -1)
    
    async for request_data in cursor:
        requests.append(MonitoringRequestDB(**request_data))
    return requests

# 요청 상태 업데이트
async def update_request_status(
    db: AsyncIOMotorDatabase, 
    request_id: str, 
    status: MonitoringStatus
) -> bool:
    """모니터링 요청 상태 업데이트 (승인/거부)"""
    result = await db.monitoring_requests.update_one(
        {"_id": request_id},
        {
            "$set": {
                "status": status,
                "responded_at": datetime.now()
            }
        }
    )
    return result.modified_count > 0

# 요청자가 보낸 요청 조회
async def get_requests_by_requester(db: AsyncIOMotorDatabase, requester_id: str) -> List[MonitoringRequestDB]:
    """특정 사용자가 보낸 모든 모니터링 요청"""
    requests = []
    cursor = db.monitoring_requests.find({
        "requester_id": requester_id
    }).sort("created_at", -1)
    
    async for request_data in cursor:
        requests.append(MonitoringRequestDB(**request_data))
    return requests

# ==================== MonitoringRelation ====================

# 모니터링 관계 생성
async def create_monitoring_relation(db: AsyncIOMotorDatabase, relation: MonitoringRelationDB) -> MonitoringRelationDB:
    """새로운 모니터링 관계 생성 (승인 후)"""
    relation_dict = relation.model_dump(by_alias=True)
    if relation_dict["_id"] == "":
        relation_dict["_id"] = str(ObjectId())
    
    await db.monitoring_relations.insert_one(relation_dict)
    return relation

# 환자의 모니터링 관계 조회
async def get_relations_by_patient(db: AsyncIOMotorDatabase, patient_id: str) -> List[MonitoringRelationDB]:
    """특정 환자의 승인된 모니터링 관계 목록"""
    relations = []
    cursor = db.monitoring_relations.find({
        "patient_id": patient_id
    }).sort("granted_at", -1)
    
    async for relation_data in cursor:
        relations.append(MonitoringRelationDB(**relation_data))
    return relations

# 모니터링하는 사용자의 환자 목록
async def get_patients_by_monitor(db: AsyncIOMotorDatabase, monitor_id: str) -> List[MonitoringRelationDB]:
    """특정 의사/보호자가 모니터링하는 환자 목록"""
    relations = []
    cursor = db.monitoring_relations.find({
        "monitor_id": monitor_id
    }).sort("granted_at", -1)
    
    async for relation_data in cursor:
        relations.append(MonitoringRelationDB(**relation_data))
    return relations

# 특정 관계 존재 확인
async def relation_exists(db: AsyncIOMotorDatabase, patient_id: str, monitor_id: str) -> bool:
    """환자-모니터 간 관계가 이미 존재하는지 확인"""
    relation = await db.monitoring_relations.find_one({
        "patient_id": patient_id,
        "monitor_id": monitor_id
    })
    return relation is not None

# 모니터링 관계 삭제
async def delete_monitoring_relation(db: AsyncIOMotorDatabase, relation_id: str) -> bool:
    """모니터링 관계 해제"""
    result = await db.monitoring_relations.delete_one({"_id": relation_id})
    return result.deleted_count > 0

# 관계 ID로 조회
async def get_relation_by_id(db: AsyncIOMotorDatabase, relation_id: str) -> Optional[MonitoringRelationDB]:
    """관계 ID로 모니터링 관계 조회"""
    relation_data = await db.monitoring_relations.find_one({"_id": relation_id})
    if relation_data:
        return MonitoringRelationDB(**relation_data)
    return None
