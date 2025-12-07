from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi import Request

from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from controller import healthController, memoController, monitoringController, userController

# MongoDB 설정 (로컬 DB 기준)
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
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
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates 설정
templates = Jinja2Templates(directory="templates")

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
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# HTML 페이지 라우트
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/patient/home", response_class=HTMLResponse)
async def patient_home(request: Request):
    return templates.TemplateResponse("patient/home.html", {"request": request})

@app.get("/patient/basic-info", response_class=HTMLResponse)
async def basic_info_input(request: Request):
    return templates.TemplateResponse("patient/basic_info.html", {"request": request})

@app.get("/patient/health-data-input", response_class=HTMLResponse)
async def health_data_input(request: Request):
    return templates.TemplateResponse("patient/health_data_input.html", {"request": request})

@app.get("/patient/health-data-inquiry", response_class=HTMLResponse)
async def health_data_inquiry(request: Request):
    return templates.TemplateResponse("patient/health_data_inquiry.html", {"request": request})

@app.get("/patient/profile", response_class=HTMLResponse)
async def profile_edit(request: Request):
    return templates.TemplateResponse("patient/profile_edit.html", {"request": request})
