# 🏥 StrokeManage

뇌졸중 위험 관리 및 모니터링 시스템

## 📋 프로젝트 소개

StrokeManage는 뇌졸중 고위험군 환자의 건강 데이터를 체계적으로 관리하고, 의사 및 보호자가 환자를 실시간으로 모니터링할 수 있는 헬스케어 시스템입니다.

### 주요 기능

- 👤 **사용자 관리**: 환자, 의사, 보호자 역할 기반 회원가입/로그인
- 🏥 **건강 프로필 관리**: 성별, 생년월일, 키, 질병력 등 정적 건강 정보 관리
- 📊 **건강 측정 데이터**: 체중, 혈압, 혈당, 흡연량 등 시계열 측정 데이터 기록
- 👥 **모니터링 시스템**: 의사/보호자가 환자 건강 상태 모니터링 요청/승인
- 📝 **메모 기능**: 건강 관련 메모 작성 및 관리
- ⚠️ **위험도 분석**: 건강 데이터 기반 뇌졸중 위험도 계산 (예정)

## 🛠 기술 스택

### Backend
- **FastAPI** (0.109.0+): 고성능 비동기 웹 프레임워크
- **MongoDB** + **Motor**: 비동기 NoSQL 데이터베이스
- **Pydantic v2**: 데이터 검증 및 직렬화

### Frontend
- **HTML5** + **Vanilla JavaScript**
- **Tailwind CSS**: 유틸리티 기반 스타일링
- **Lucide Icons**: 아이콘 라이브러리

## 📁 프로젝트 구조

```
StrokeManage/
├── server/                      # 백엔드
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── controller/             # API 엔드포인트
│   │   ├── userController.py
│   │   ├── healthController.py
│   │   ├── memoController.py
│   │   └── monitoringController.py
│   ├── services/               # 비즈니스 로직
│   │   ├── userService.py
│   │   ├── healthService.py
│   │   ├── memoService.py
│   │   └── monitoringService.py
│   ├── crud/                   # DB CRUD 연산
│   │   ├── userCrud.py
│   │   ├── healthCrud.py
│   │   ├── memoCrud.py
│   │   └── monitoringCrud.py
│   ├── models/                 # MongoDB 모델
│   │   ├── userModel.py
│   │   ├── healthModel.py
│   │   ├── memoModel.py
│   │   └── monitoringModel.py
│   ├── schemas/                # Pydantic 스키마
│   │   ├── userSchema.py
│   │   ├── healthSchema.py
│   │   ├── memoSchema.py
│   │   └── monitoringSchema.py
│   └── core/                   # 핵심 유틸리티
│       └── riskCalculator.py
├── client/                     # 프론트엔드
│   ├── index.html             # 메인 페이지
│   ├── login.html             # 로그인 페이지
│   ├── register.html          # 회원가입 페이지
│   ├── health-input.html      # 건강 데이터 입력
│   ├── result.html            # 결과 페이지
│   ├── style.css              # 공통 스타일
│   └── *.js                   # 페이지별 JavaScript
├── router.md                   # API 문서
├── db_run.sh                   # MongoDB 실행 스크립트
└── StrokeManage_API.postman_collection.json  # Postman 테스트 컬렉션
```

## 🚀 시작하기

### 사전 요구사항

- Python 3.9+
- MongoDB 4.0+
- pip

### 설치 및 실행

#### 1. 저장소 클론
```bash
git clone https://github.com/madebyhwan/stroke.git
cd StrokeManage
```

#### 2. Python 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

#### 3. 의존성 설치
```bash
pip install fastapi==0.109.0
pip install "uvicorn[standard]"
pip install motor
pip install pydantic
```

#### 4. MongoDB 실행
```bash
# 방법 1: 스크립트 사용
chmod +x db_run.sh
./db_run.sh

# 방법 2: 직접 실행
mongod --dbpath=/Users/duck/data/db --port 27017
```

#### 5. 서버 실행
```bash
cd server
python -m uvicorn main:app --reload --port 8000
```

서버가 실행되면:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 6. 프론트엔드 실행
```bash
# 간단한 HTTP 서버 실행
cd client
python -m http.server 8080
```

프론트엔드 접속: http://localhost:8080

## 📚 API 문서

자세한 API 명세는 [router.md](./router.md) 파일을 참고하세요.

### 주요 엔드포인트

#### User API
- `POST /users/register` - 회원가입
- `POST /users/login` - 로그인
- `GET /users/{user_id}` - 사용자 정보 조회
- `GET /users/{user_id}/health` - 건강 프로필 조회
- `PUT /users/{user_id}/health` - 건강 프로필 수정

#### Health API
- `POST /health/records` - 건강 측정 데이터 생성
- `GET /health/records/user/{user_id}` - 측정 데이터 목록 조회
- `GET /health/records/user/{user_id}/latest` - 최신 측정 데이터 조회
- `DELETE /health/records/{record_id}` - 측정 데이터 삭제

## 💾 데이터베이스 구조

### Collections

#### users
사용자 기본 정보 + 건강 프로필 (정적 데이터)
```javascript
{
  _id: "patient001",
  name: "김환자",
  password: "hashed_password",
  role: "PATIENT",
  sex: "M",
  birth_date: "1990-05-15",
  height_cm: 175,
  stroke_history: false,
  hypertension: false,
  heart_disease: false,
  smoking_history: "NON_SMOKER",
  diabetes: false,
  measured_at: "2025-12-05T10:30:00",
  created_at: "2025-12-01T09:00:00",
  updated_at: "2025-12-05T10:30:00"
}
```

#### health_records
건강 측정 데이터 (시계열 데이터)
```javascript
{
  _id: "record_123",
  user_id: "patient001",
  weight_kg: 72.5,
  systolic_bp: 125,
  diastolic_bp: 82,
  glucose_level: 98,
  smoking: 0,
  created_at: "2025-12-05T14:30:00"
}
```

#### monitoring_requests
모니터링 요청 (예정)

#### monitoring_relations
모니터링 관계 (예정)

#### memos
메모 (예정)

## 📝 개발 노트

### 데이터 구조 설계 원칙
1. **정적 데이터 vs 동적 데이터 분리**
   - 정적: 성별, 키, 질병력 등 → `users` 컬렉션
   - 동적: 체중, 혈압, 혈당 등 → `health_records` 컬렉션

2. **시계열 데이터 최적화**
   - MongoDB의 정렬 인덱스 활용 (created_at)
   - 최신 데이터 조회 시 전체 데이터 로드 방지

3. **부분 업데이트 지원**
   - Pydantic의 `exclude_unset=True` 활용
   - 클라이언트가 변경된 필드만 전송 가능

## 🚧 향후 개발 계획

- 모니터링 시스템 구현
- 메모 시스템 구현
- 뇌졸중 위험도 계산 알고리즘 구현
- 실시간 알림 기능 (WebSocket)
- 데이터 시각화 차트
- 관리자 대시보드

## 📞 문의

프로젝트 관련 문의사항은 GitHub Issues를 이용해주세요.
