# 🏥 StrokeManage

뇌졸중 위험도 분석 및 실시간 모니터링 시스템

## 📋 프로젝트 소개

StrokeManage는 뇌졸중 고위험군 환자의 건강 데이터를 체계적으로 관리하고, 의료진과 보호자가 환자를 실시간으로 모니터링할 수 있는 통합 헬스케어 플랫폼입니다.

### 핵심 기능

#### 🎯 위험도 분석 시스템
- **자동 위험도 계산**: 건강 데이터 입력 시 10가지 위험 요인 기반 자동 점수 산출
- **4단계 위험도 분류**: 낮음(0-20) / 보통(20-40) / 높음(40-60) / 매우 높음(60+)
- **시계열 추이 분석**: Chart.js 기반 위험도 변화 추이 그래프 제공
- **실시간 알림**: 위험도 상승 시 즉각적인 피드백

#### 👥 사용자 역할 시스템
- **환자 (PATIENT)**: 건강 데이터 입력, 위험도 확인, 메모 수신
- **의사 (DOCTOR)**: 환자 모니터링, 메모 작성, 건강 데이터 조회
- **보호자 (CAREGIVER)**: 환자 모니터링, 건강 상태 확인

#### 🏥 건강 데이터 관리
- **기본 정보**: 성별, 생년월일, 키, 질병력 (뇌졸중, 고혈압, 심장병, 당뇨)
- **측정 데이터**: 체중, 혈압(수축기/이완기), 혈당, 흡연량
- **시계열 저장**: 모든 측정 기록 보존으로 추세 분석 가능

#### 👨‍⚕️ 모니터링 시스템
- **요청/승인 프로세스**: 의사/보호자의 모니터링 요청 후 환자 승인
- **실시간 데이터 공유**: 승인된 모니터에게 건강 데이터 실시간 공유
- **환자 상세 모달**: 기본 정보, 최근 건강 데이터, 위험도 그래프 통합 제공

#### 📝 메모 시스템
- **의사 → 환자 메모**: 건강 조언, 주의사항 전달
- **알림 기능**: 새 메모 도착 시 빨간 배지 알림
- **권한 관리**: 의사만 작성, 본인 메모만 삭제 가능

## 🛠 기술 스택

### Backend
- **FastAPI** (0.109.0+): 고성능 비동기 웹 프레임워크
- **MongoDB** + **Motor**: 비동기 NoSQL 데이터베이스
- **Pydantic v2**: 데이터 검증 및 직렬화

### Frontend
- **Jinja2 Templates**: 서버 사이드 렌더링
- **Vanilla JavaScript**: 동적 UI 및 API 통신
- **Tailwind CSS**: 유틸리티 기반 반응형 디자인
- **Lucide Icons**: 모던 아이콘 라이브러리
- **Chart.js v4.4.0**: 인터랙티브 데이터 시각화

### Core Algorithm
- **위험도 계산 엔진**: 10가지 요인 가중치 기반 점수 산출
  - 나이 (20점), 뇌졸중 이력 (30점), 혈압 (20점), 고혈압 (15점)
  - 심장병 (15점), 흡연 (15점), 당뇨 (10점), BMI (10점), 혈당 (10점), 성별 (5점)

## 📁 프로젝트 구조

```
StrokeManage/
├── main.py                      # FastAPI 앱 진입점
├── db_run.sh                    # MongoDB 실행 스크립트
├── README.md                    # 프로젝트 문서
├── router.md                    # API 상세 명세
│
├── controller/                  # API 엔드포인트 계층
│   ├── userController.py       # 사용자 인증/관리 (회원가입, 로그인, 프로필)
│   ├── healthController.py     # 건강 데이터 CRUD 및 위험도 계산
│   ├── monitoringController.py # 모니터링 요청/관계 관리
│   └── memoController.py       # 메모 작성/조회/삭제
│
├── services/                    # 비즈니스 로직 계층
│   ├── userService.py          # 사용자 비즈니스 로직
│   ├── healthService.py        # 건강 데이터 처리 + 위험도 자동 계산
│   ├── monitoringService.py    # 모니터링 권한 검증
│   └── memoService.py          # 메모 권한 검증
│
├── crud/                        # 데이터베이스 CRUD 계층
│   ├── userCrud.py             # 사용자 DB 연산
│   ├── healthCrud.py           # 건강 데이터 DB 연산
│   ├── monitoringCrud.py       # 모니터링 관계 DB 연산
│   └── memoCrud.py             # 메모 DB 연산
│
├── models/                      # MongoDB 문서 모델
│   ├── userModel.py            # 사용자 스키마 (+ 건강 프로필)
│   ├── healthModel.py          # 건강 측정 데이터 스키마 (+ 위험도)
│   ├── monitoringModel.py      # 모니터링 요청/관계 스키마
│   └── memoModel.py            # 메모 스키마
│
├── schemas/                     # API 요청/응답 스키마
│   ├── userSchema.py           # 사용자 DTO
│   ├── healthSchema.py         # 건강 데이터 DTO
│   ├── monitoringSchema.py     # 모니터링 DTO
│   └── memoSchema.py           # 메모 DTO
│
├── core/                        # 핵심 유틸리티
│   └── riskCalculator.py       # 뇌졸중 위험도 계산 알고리즘
│
├── static/                      # 정적 파일
│   ├── css/
│   │   └── style.css           # 공통 스타일
│   └── js/
│       └── script.js           # 공통 JavaScript
│
└── templates/                   # Jinja2 템플릿
    ├── base.html               # 기본 레이아웃
    ├── login.html              # 로그인 페이지
    ├── register.html           # 회원가입 페이지
    ├── patient/                # 환자 페이지
    │   ├── home.html           # 홈 (위험도 카드, 최근 기록, FAST 검사)
    │   ├── health_data_input.html    # 건강 데이터 입력
    │   ├── health_data_inquiry.html  # 건강 데이터 조회 + 그래프
    │   ├── basic_info.html     # 기본 정보 수정
    │   ├── my_monitors.html    # 나를 모니터링하는 사람 관리
    │   ├── profile_edit.html   # 프로필 수정
    │   ├── _bottom_nav.html    # 하단 네비게이션 바
    │   └── _common_scripts.html # 공통 스크립트 (알림 등)
    └── monitor/                # 모니터 페이지
        └── home.html           # 환자 목록 + 상세 모달 (위험도 그래프 포함)
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
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

#### 3. 의존성 설치
```bash
pip3 install fastapi
pip3 install uvicorn
pip3 install motor
pip3 install pydantic
pip3 install jinja2
```

#### 4. MongoDB 실행
```
./.env.example 활용
```

#### 5. 서버 실행
```bash
python3 main.py
```

서버가 실행되면:
- **웹 애플리케이션**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API 문서

자세한 API 명세는 [router.md](./router.md) 파일을 참고하세요.

### 주요 엔드포인트

#### 🔐 User API (`/users`)
- `POST /users/register` - 회원가입
- `POST /users/login` - 로그인
- `GET /users/{user_id}` - 사용자 정보 조회
- `PUT /users/{user_id}` - 사용자 정보 수정
- `GET /users/{user_id}/health` - 건강 프로필 조회
- `PUT /users/{user_id}/health` - 건강 프로필 수정

#### 🏥 Health API (`/health`)
- `POST /health/records` - 건강 데이터 생성 (위험도 자동 계산)
- `GET /health/records/user/{user_id}` - 사용자별 건강 데이터 조회
- `GET /health/records/user/{user_id}/latest` - 최신 건강 데이터 조회
- `GET /health/records/monitor/{monitor_id}/patient/{patient_id}` - 모니터링 데이터 조회
- `DELETE /health/records/{record_id}` - 건강 데이터 삭제

#### 👥 Monitoring API (`/monitoring`)
- `POST /monitoring/request` - 모니터링 요청 생성
- `GET /monitoring/requests/received/{user_id}` - 받은 요청 조회
- `GET /monitoring/requests/sent/{user_id}` - 보낸 요청 조회
- `PUT /monitoring/request/{request_id}/respond` - 요청 응답 (승인/거절)
- `DELETE /monitoring/request/{request_id}` - 요청 취소
- `GET /monitoring/my-patients/{monitor_id}` - 내 환자 목록 조회
- `GET /monitoring/my-monitors/{patient_id}` - 나를 모니터링하는 사람 조회
- `DELETE /monitoring/relation/{relation_id}` - 모니터링 관계 해제

#### 📝 Memo API (`/memos`)
- `POST /memos` - 메모 작성 (의사만)
- `GET /memos` - 메모 조회 (patient_id, doctor_id 필터)
- `GET /memos/{memo_id}` - 특정 메모 조회
- `DELETE /memos/{memo_id}` - 메모 삭제 (작성자만)

## 💾 데이터베이스 구조

### Collections

#### users
사용자 기본 정보 + 건강 프로필 (정적 데이터)
```javascript
{
  _id: "patient001",
  password: "hashed_password",
  name: "김환자",
  role: "PATIENT",  // PATIENT | DOCTOR | CAREGIVER
  sex: "M",  // M | F
  birth_date: "1990-05-15",
  height_cm: 175,
  stroke_history: false,
  hypertension: true,
  heart_disease: false,
  diabetes: false,
  smoking_history: "NON_SMOKER",  // NON_SMOKER | PAST_SMOKER | SMOKER
  measured_at: "2025-12-05T10:30:00",
  created_at: "2025-12-01T09:00:00",
  updated_at: "2025-12-05T10:30:00"
}
```

#### health_records
건강 측정 데이터 (시계열 데이터) + 자동 계산된 위험도
```javascript
{
  _id: "record_123",
  user_id: "patient001",
  weight_kg: 72.5,
  systolic_bp: 135,
  diastolic_bp: 88,
  glucose_level: 110,
  smoking: 0,  // 0: 비흡연, 1: 과거 흡연, 2: 현재 흡연
  stroke_risk_score: 45.2,  // 0-100 점수
  stroke_risk_level: "높음",  // 낮음 | 보통 | 높음 | 매우 높음
  created_at: "2025-12-05T14:30:00"
}
```

#### monitoring_requests
모니터링 요청
```javascript
{
  _id: "req_001",
  requester_id: "doctor001",
  requester_name: "김의사",
  patient_id: "patient001",
  patient_name: "김환자",
  status: "PENDING",  // PENDING | APPROVED | REJECTED
  created_at: "2025-12-01T10:00:00",
  responded_at: null
}
```

#### monitoring_relations
모니터링 관계 (승인된 관계)
```javascript
{
  _id: "rel_001",
  monitor_id: "doctor001",
  monitor_name: "김의사",
  monitor_role: "DOCTOR",
  patient_id: "patient001",
  patient_name: "김환자",
  approved_at: "2025-12-01T11:00:00"
}
```

#### memos
의사 → 환자 메모
```javascript
{
  _id: "memo_001",
  doctor_id: "doctor001",
  patient_id: "patient001",
  content: "혈압이 높습니다. 염분 섭취를 줄이세요.",
  created_at: "2025-12-05T16:00:00"
}
```

## 🎨 UI/UX 특징

### 환자 페이지
- **홈**: 위험도 카드 (점수 + 그래프), 최근 건강 기록 3개, FAST 뇌졸중 자가검사
- **건강 기록**: 측정 데이터 입력 폼 (체중, 혈압, 혈당, 흡연량)
- **건강 분석**: 위험도 카드 + 시계열 그래프 (최근 7개 데이터 포인트)
- **기본 정보**: 질병력, 흡연력 수정
- **내 모니터**: 나를 모니터링하는 의사/보호자 목록, 요청 승인/거절

### 모니터 페이지
- **환자 관리**: 환자 검색, 모니터링 요청, 등록 환자 목록
- **환자 상세 모달**: 
  - 기본 정보 (이름, 나이, 성별, 키)
  - 최근 건강 데이터
  - 위험도 카드 (점수 + 그래프, 최근 7개 포인트)
  - 메모 작성 (의사만) 및 이전 메모 목록

### 공통 기능
- **알림 시스템**: 새 메모, 새 모니터링 요청 시 빨간 배지 표시
- **반응형 디자인**: 모바일/태블릿/데스크톱 대응

## 🔍 위험도 계산 알고리즘

### 점수 산출 방식
```python
총점 = 나이점수(20) + 성별점수(5) + 뇌졸중이력(30) + 
       고혈압(15) + 심장병(15) + 당뇨(10) + 흡연(15) + 
       혈압점수(20) + BMI점수(10) + 혈당점수(10)
```

### 위험도 분류
- **낮은 위험도 (0-20)**: 건강한 상태
- **보통 위험도 (20-40)**: 주의 필요
- **높은 위험도 (40-60)**: 의료 상담 권장
- **매우 높은 위험도 (60+)**: 즉시 의료 조치 필요

### 시각화
- **점수**: 숫자 + 색상 코딩 (초록/노랑/주황/빨강)
- **그래프**: Chart.js 라인 차트, 각 데이터 포인트 색상 구분
- **추이 분석**: 최근 7개 측정 데이터로 변화 추세 파악

## 📝 개발 노트

### 아키텍처 설계 원칙
1. **계층 분리**: Controller → Service → CRUD 3계층 구조
2. **관심사 분리**: 비즈니스 로직과 DB 연산 분리
3. **단일 책임**: 각 모듈은 하나의 역할만 수행
4. **의존성 역전**: 상위 레이어가 하위 레이어 의존

### 데이터 설계
1. **정적 vs 동적 분리**: 
   - 정적 (성별, 키, 질병력) → `users` 컬렉션
   - 동적 (체중, 혈압, 혈당) → `health_records` 컬렉션
2. **위험도 자동 계산**: 건강 데이터 입력 시 자동으로 점수 산출 및 저장
3. **시계열 최적화**: `created_at` 인덱스로 최신 데이터 빠르게 조회

### 보안 고려사항
1. **권한 검증**: 
   - 메모 작성: 의사만 가능
   - 메모 삭제: 작성자만 가능
   - 데이터 조회: 본인 또는 승인된 모니터만 가능

## 📞 문의

프로젝트 관련 문의사항은 GitHub Issues를 이용해주세요.

- Repository: https://github.com/madebyhwan/stroke
- Issues: https://github.com/madebyhwan/stroke/issues
