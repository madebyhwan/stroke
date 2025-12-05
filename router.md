# StrokeManage API 라우터 명세

## 📋 목차
- [User API](#user-api)
- [Health API](#health-api)
- [Memo API](#memo-api)
- [Monitoring API](#monitoring-api)

---

## 🔐 User API

**Base URL**: `/users`

### 1. 회원가입
- **Endpoint**: `POST /users/register`
- **설명**: 새로운 사용자 등록
- **Request Body**:
  ```json
  {
    "id": "user123",
    "password": "password123",
    "name": "홍길동",
    "role": "PATIENT"
  }
  ```
- **Response**: `UserResponse` (201 Created)
  ```json
  {
    "id": "user123",
    "name": "홍길동",
    "role": "PATIENT"
  }
  ```
- **Error**:
  - `400`: 이미 존재하는 아이디
  - `500`: 회원가입 실패

### 2. 로그인
- **Endpoint**: `POST /users/login`
- **설명**: 사용자 로그인
- **Request Body**:
  ```json
  {
    "id": "user123",
    "password": "password123"
  }
  ```
- **Response**: `UserResponse` (200 OK)
  ```json
  {
    "id": "user123",
    "name": "홍길동",
    "role": "PATIENT"
  }
  ```
- **Error**:
  - `401`: 아이디 또는 비밀번호가 잘못됨

### 3. 사용자 정보 조회
- **Endpoint**: `GET /users/{user_id}`
- **설명**: 특정 사용자의 기본 정보 조회
- **Path Parameter**:
  - `user_id`: 사용자 아이디
- **Response**: `UserResponse` (200 OK)
  ```json
  {
    "id": "user123",
    "name": "홍길동",
    "role": "PATIENT"
  }
  ```
- **Error**:
  - `404`: 사용자를 찾을 수 없음

### 4. 사용자 정보 수정
- **Endpoint**: `PUT /users/{user_id}`
- **설명**: 사용자의 기본 정보 수정 (이름, 비밀번호만 가능)
- **Path Parameter**:
  - `user_id`: 사용자 아이디
- **Request Body**: `UserUpdate` (모든 필드 optional)
  ```json
  {
    "id": "user123",
    "name": "홍길동_수정",
    "password": "newpassword123"
  }
  ```
- **Response**: `UserResponse` (200 OK)
  ```json
  {
    "id": "user123",
    "name": "홍길동_수정",
    "role": "PATIENT"
  }
  ```
- **Error**:
  - `400`: 요청 경로의 user_id와 본문의 id가 불일치
  - `404`: 사용자를 찾을 수 없음
- **참고**:
  - 부분 업데이트 지원 (변경할 필드만 전송 가능)
  - `role` 필드는 보안상 수정 불가 (관리자 권한 필요)
  - `updated_at`은 서버에서 자동 설정

### 5. 사용자 건강 프로필 조회
- **Endpoint**: `GET /users/{user_id}/health`
- **설명**: 사용자의 기본 건강 정보 조회 (프로필)
- **Path Parameter**:
  - `user_id`: 사용자 아이디
- **Response**: `UserHealthInfoResponse` (200 OK)
  ```json
  {
    "sex": "M",
    "birth_date": "1990-01-01",
    "height_cm": 175,
    "stroke_history": false,
    "hypertension": false,
    "heart_disease": false,
    "smoking_history": "NON_SMOKER",
    "diabetes": false,
    "measured_at": "2025-12-05T10:30:00"
  }
  ```
- **Error**:
  - `404`: 사용자의 건강 정보를 찾을 수 없음

### 6. 사용자 건강 프로필 수정
- **Endpoint**: `PUT /users/{user_id}/health`
- **설명**: 사용자의 기본 건강 정보 수정 (부분 업데이트 가능)
- **Path Parameter**:
  - `user_id`: 사용자 아이디
- **Request Body**: `UserHealthInfoUpdate` (모든 필드 optional)
  ```json
  {
    "id": "user123",
    "height_cm": 176,
    "hypertension": true
  }
  ```
- **Response**: `UserHealthInfoResponse` (200 OK)
- **Error**:
  - `400`: 요청 경로의 user_id와 본문의 id가 불일치
  - `404`: 사용자를 찾을 수 없음
- **참고**:
  - 부분 업데이트 지원 (변경할 필드만 전송 가능)
  - `measured_at`은 서버에서 자동으로 현재 시간 설정

---

## 🏥 Health API

**Base URL**: `/health`

### 1. 건강 측정 데이터 생성
- **Endpoint**: `POST /health/records`
- **설명**: 새로운 건강 측정 데이터 생성 (시계열 데이터)
- **Request Body**: `HealthRecordInput`
  ```json
  {
    "user_id": "user123",
    "weight_kg": 70.5,
    "systolic_bp": 120,
    "diastolic_bp": 80,
    "glucose_level": 95,
    "smoking": 0
  }
  ```
- **Response**: `HealthRecordResponse` (201 Created)
  ```json
  {
    "id": "record_123",
    "user_id": "user123",
    "weight_kg": 70.5,
    "systolic_bp": 120,
    "diastolic_bp": 80,
    "glucose_level": 95,
    "smoking": 0,
    "created_at": "2025-12-05T14:30:00"
  }
  ```

### 2. 사용자별 건강 측정 데이터 조회
- **Endpoint**: `GET /health/records/user/{user_id}`
- **설명**: 특정 사용자의 건강 측정 데이터 목록 조회 (최신순)
- **Path Parameter**:
  - `user_id`: 사용자 아이디
- **Response**: `List[HealthRecordResponse]` (200 OK)

### 3. 최신 건강 측정 데이터 조회
- **Endpoint**: `GET /health/records/user/{user_id}/latest`
- **설명**: 사용자의 가장 최근 건강 측정 데이터 조회
- **Path Parameter**:
  - `user_id`: 사용자 아이디
- **Response**: `HealthRecordResponse` (200 OK)
- **Error**:
  - `404`: 건강 측정 데이터를 찾을 수 없음

### 4. 건강 측정 데이터 삭제
- **Endpoint**: `DELETE /health/records/{record_id}`
- **설명**: 건강 측정 데이터 삭제
- **Path Parameter**:
  - `record_id`: 건강 측정 데이터 ID
- **Response**: `204 No Content`
- **Error**:
  - `404`: 건강 측정 데이터를 찾을 수 없음

---

## 📝 Memo API

**Base URL**: `/memos`

### 1. 메모 작성
- **Endpoint**: `POST /memos/`
- **설명**: 새로운 메모 작성
- **Request Body**:
  ```json
  {
    "user_id": "user123",
    "title": "오늘의 건강 기록",
    "content": "아침 운동 30분 완료"
  }
  ```
- **Response**: `MemoResponse` (201 Created)

### 2. 사용자별 메모 목록 조회
- **Endpoint**: `GET /memos/user/{user_id}`
- **설명**: 특정 사용자의 메모 목록 조회
- **Path Parameter**:
  - `user_id`: 사용자 아이디
- **Response**: `List[MemoResponse]` (200 OK)

### 3. 메모 상세 조회
- **Endpoint**: `GET /memos/{memo_id}`
- **설명**: 특정 메모 상세 정보 조회
- **Response**: `MemoResponse` (200 OK)
- **Error**:
  - `404`: 메모를 찾을 수 없음

### 4. 메모 수정
- **Endpoint**: `PUT /memos/{memo_id}`
- **설명**: 기존 메모 수정
- **Request Body**:
  ```json
  {
    "title": "수정된 제목",
    "content": "수정된 내용"
  }
  ```
- **Response**: `MemoResponse` (200 OK)

### 5. 메모 삭제
- **Endpoint**: `DELETE /memos/{memo_id}`
- **설명**: 메모 삭제
- **Response**: `204 No Content`

---

## 👥 Monitoring API

**Base URL**: `/monitoring`

### 1. 모니터링 요청 생성
- **Endpoint**: `POST /monitoring/request`
- **설명**: 의사/보호자가 환자에게 모니터링 요청
- **Request Body**:
  ```json
  {
    "patient_id": "patient123",
    "message": "건강 상태를 모니터링하고 싶습니다"
  }
  ```
- **Response**: `MonitoringRequestResponse` (201 Created)

### 2. 대기 중인 요청 조회 (환자용)
- **Endpoint**: `GET /monitoring/requests/pending/{patient_id}`
- **설명**: 환자가 받은 대기 중인 모니터링 요청 목록
- **Path Parameter**:
  - `patient_id`: 환자 아이디
- **Response**: `List[MonitoringRequestResponse]` (200 OK)

### 3. 모니터링 요청 승인/거부
- **Endpoint**: `POST /monitoring/approve`
- **설명**: 환자가 모니터링 요청 승인 또는 거부
- **Request Body**:
  ```json
  {
    "request_id": "req_123",
    "approved": true
  }
  ```
- **Response**: `MonitoringRequestResponse` (200 OK)

### 4. 모니터링 관계 조회
- **Endpoint**: `GET /monitoring/relations/{patient_id}`
- **설명**: 특정 환자의 승인된 모니터링 관계 목록
- **Path Parameter**:
  - `patient_id`: 환자 아이디
- **Response**: `List[MonitoringRelationResponse]` (200 OK)

### 5. 내가 모니터링하는 환자 목록
- **Endpoint**: `GET /monitoring/my-patients/{monitor_id}`
- **설명**: 의사/보호자가 모니터링 중인 환자 목록
- **Path Parameter**:
  - `monitor_id`: 의사/보호자 아이디
- **Response**: `List[MonitoringRelationResponse]` (200 OK)

### 6. 모니터링 관계 해제
- **Endpoint**: `DELETE /monitoring/relation/{relation_id}`
- **설명**: 승인된 모니터링 관계 해제
- **Response**: `204 No Content`

---

## 📊 공통 응답 형식

### 성공 응답
```json
{
  "status": "success",
  "data": { ... }
}
```

### 에러 응답
```json
{
  "detail": "에러 메시지"
}
```

---

## 🔑 데이터 타입 정의

### UserRole (Enum)
- `PATIENT`: 환자
- `DOCTOR`: 의사
- `CAREGIVER`: 보호자

### Sex (Enum)
- `M`: 남성
- `F`: 여성

### MonitoringStatus (Enum)
- `PENDING`: 대기 중
- `APPROVED`: 승인됨
- `REJECTED`: 거부됨

---

## 📌 참고사항

- 모든 날짜는 ISO 8601 형식 (`YYYY-MM-DD`)
- 모든 타임스탬프는 ISO 8601 형식 (`YYYY-MM-DDTHH:MM:SS`)
- 비밀번호는 bcrypt로 해싱되어 저장됨
- MongoDB의 `_id` 필드는 API에서 `id`로 표현됨
- 현재는 인증 없이 작동 (추후 JWT 토큰 기반 인증 추가 예정)

**데이터 구조**:
- `users` 컬렉션: 사용자 기본 정보 + 건강 프로필 (정적 데이터)
- `health_records` 컬렉션: 건강 측정 데이터 (시계열 데이터)
- 건강 프로필은 가입 후 별도로 설정 가능
- 건강 측정 데이터는 필요할 때마다 생성

---

## 🚀 실행 방법

```bash
# 서버 실행
cd server
python -m uvicorn main:app --reload --port 8000

# API 문서 확인
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## 📮 Postman 테스트 가이드

### 환경 변수 설정
```
BASE_URL = http://localhost:8000
```

### 테스트 시나리오

#### 1️⃣ 회원가입 및 로그인
```bash
# 1-1. 회원가입
POST {{BASE_URL}}/users/register
Content-Type: application/json

{
  "id": "patient001",
  "password": "test1234",
  "name": "김환자",
  "role": "PATIENT"
}

# 1-2. 로그인
POST {{BASE_URL}}/users/login
Content-Type: application/json

{
  "id": "patient001",
  "password": "test1234"
}

# 1-3. 사용자 정보 조회
GET {{BASE_URL}}/users/patient001

# 1-4. 사용자 정보 수정 (이름만)
PUT {{BASE_URL}}/users/patient001
Content-Type: application/json

{
  "id": "patient001",
  "name": "김환자_수정"
}

# 1-5. 사용자 정보 수정 (비밀번호만)
PUT {{BASE_URL}}/users/patient001
Content-Type: application/json

{
  "id": "patient001",
  "password": "newpassword123"
}
```

#### 2️⃣ 건강 프로필 설정
```bash
# 2-1. 건강 프로필 수정
PUT {{BASE_URL}}/users/patient001/health
Content-Type: application/json

{
  "id": "patient001",
  "sex": "M",
  "birth_date": "1990-05-15",
  "height_cm": 175,
  "stroke_history": false,
  "hypertension": false,
  "heart_disease": false,
  "smoking_history": "NON_SMOKER",
  "diabetes": false
}

# 2-2. 건강 프로필 조회
GET {{BASE_URL}}/users/patient001/health
```

#### 3️⃣ 건강 측정 데이터 입력
```bash
# 3-1. 첫 번째 측정 데이터
POST {{BASE_URL}}/health/records
Content-Type: application/json

{
  "user_id": "patient001",
  "weight_kg": 72.5,
  "systolic_bp": 125,
  "diastolic_bp": 82,
  "glucose_level": 98,
  "smoking": 0
}

# 3-2. 두 번째 측정 데이터 (다음날)
POST {{BASE_URL}}/health/records
Content-Type: application/json

{
  "user_id": "patient001",
  "weight_kg": 71.8,
  "systolic_bp": 122,
  "diastolic_bp": 80,
  "glucose_level": 95,
  "smoking": 0
}
```

#### 4️⃣ 건강 데이터 조회
```bash
# 4-1. 모든 측정 데이터 조회 (최신순)
GET {{BASE_URL}}/health/records/user/patient001

# 4-2. 최신 측정 데이터만 조회
GET {{BASE_URL}}/health/records/user/patient001/latest
```

#### 5️⃣ 사용자 정보 부분 업데이트
```bash
# 5-1. 이름만 수정
PUT {{BASE_URL}}/users/patient001
Content-Type: application/json

{
  "id": "patient001",
  "name": "김환자_최종"
}

# 5-2. 비밀번호만 수정
PUT {{BASE_URL}}/users/patient001
Content-Type: application/json

{
  "id": "patient001",
  "password": "supersecure456"
}
```

#### 6️⃣ 건강 프로필 부분 업데이트
```bash
# 6-1. 키와 고혈압만 수정
PUT {{BASE_URL}}/users/patient001/health
Content-Type: application/json

{
  "id": "patient001",
  "height_cm": 176,
  "hypertension": true
}
```

#### 7️⃣ 데이터 삭제
```bash
# 7-1. 건강 측정 데이터 삭제
DELETE {{BASE_URL}}/health/records/{record_id}
```

### Postman Collection JSON

아래 내용을 복사하여 Postman에서 Import하세요:

```json
{
  "info": {
    "name": "StrokeManage API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "BASE_URL",
      "value": "http://localhost:8000"
    },
    {
      "key": "user_id",
      "value": "patient001"
    }
  ],
  "item": [
    {
      "name": "User",
      "item": [
        {
          "name": "회원가입",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{BASE_URL}}/users/register",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"id\": \"patient001\",\n  \"password\": \"test1234\",\n  \"name\": \"김환자\",\n  \"role\": \"PATIENT\"\n}"
            }
          }
        },
        {
          "name": "로그인",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{BASE_URL}}/users/login",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"id\": \"{{user_id}}\",\n  \"password\": \"test1234\"\n}"
            }
          }
        },
        {
          "name": "사용자 정보 조회",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/users/{{user_id}}"
          }
        },
        {
          "name": "건강 프로필 조회",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/users/{{user_id}}/health"
          }
        },
        {
          "name": "건강 프로필 수정",
          "request": {
            "method": "PUT",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{BASE_URL}}/users/{{user_id}}/health",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"id\": \"{{user_id}}\",\n  \"sex\": \"M\",\n  \"birth_date\": \"1990-05-15\",\n  \"height_cm\": 175,\n  \"stroke_history\": false,\n  \"hypertension\": false,\n  \"heart_disease\": false,\n  \"smoking_history\": \"NON_SMOKER\",\n  \"diabetes\": false\n}"
            }
          }
        }
      ]
    },
    {
      "name": "Health",
      "item": [
        {
          "name": "건강 측정 데이터 생성",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{BASE_URL}}/health/records",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"user_id\": \"{{user_id}}\",\n  \"weight_kg\": 72.5,\n  \"systolic_bp\": 125,\n  \"diastolic_bp\": 82,\n  \"glucose_level\": 98,\n  \"smoking\": 0\n}"
            }
          }
        },
        {
          "name": "사용자 측정 데이터 조회",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/health/records/user/{{user_id}}"
          }
        },
        {
          "name": "최신 측정 데이터 조회",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/health/records/user/{{user_id}}/latest"
          }
        },
        {
          "name": "측정 데이터 삭제",
          "request": {
            "method": "DELETE",
            "url": "{{BASE_URL}}/health/records/{record_id}"
          }
        }
      ]
    }
  ]
}
```

### 테스트 순서
1. **회원가입** → 새 사용자 생성
2. **로그인** → 인증 확인
3. **사용자 정보 수정** → 이름 또는 비밀번호 변경 (선택)
4. **건강 프로필 수정** → 기본 건강 정보 설정
5. **건강 프로필 조회** → 저장된 정보 확인
6. **건강 측정 데이터 생성** (여러 번) → 시계열 데이터 축적
7. **사용자 측정 데이터 조회** → 모든 측정 기록 확인
8. **최신 측정 데이터 조회** → 가장 최근 기록만 확인
