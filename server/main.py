from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from controller import healthController, memoController, monitoringController, userController
from contextlib import asynccontextmanager

# MongoDB 설정 (로컬 DB 기준)
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.stroke_db  # 'stroke_db'라는 데이터베이스 사용

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행
    app.mongodb_client = client
    app.mongodb = db
    print("✅ MongoDB Connected!")
    yield
    # 종료 시 실행
    app.mongodb_client.close()
    print("❌ MongoDB Disconnected")

app = FastAPI(lifespan=lifespan)

# CORS 설정 (프론트엔드 연결을 위해 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 단계에서는 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 컨트롤러 등록 (라우터 연결)
app.include_router(userController.router, prefix="/users", tags=["Users"])
app.include_router(healthController.router, prefix="/health", tags=["Health"])
app.include_router(monitoringController.router, prefix="/monitoring", tags=["Monitoring"])
# app.include_router(memoController.router, prefix="/memos", tags=["Memos"])

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": "🏥 뇌졸중 관리 시스템 API",
        "status": "running",
        "docs": "/docs"
    }
