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

### 4. 모니터링 권한으로 환자 데이터 조회
- **Endpoint**: `GET /health/records/monitor/{monitor_id}/patient/{patient_id}`
- **설명**: 모니터링 권한이 있는 사용자가 환자의 건강 측정 데이터 조회
- **Path Parameter**:
  - `monitor_id`: 모니터(의사/보호자) 아이디
  - `patient_id`: 환자 아이디
- **Response**: `List[HealthRecordResponse]` (200 OK)
- **Error**:
  - `403`: 모니터링 권한 없음
  - `500`: 데이터 조회 실패

### 5. 모니터링 권한으로 환자 최신 데이터 조회
- **Endpoint**: `GET /health/records/monitor/{monitor_id}/patient/{patient_id}/latest`
- **설명**: 모니터링 권한이 있는 사용자가 환자의 최신 건강 측정 데이터 조회
- **Path Parameter**:
  - `monitor_id`: 모니터(의사/보호자) 아이디
  - `patient_id`: 환자 아이디
- **Response**: `HealthRecordResponse` (200 OK)
- **Error**:
  - `403`: 모니터링 권한 없음
  - `404`: 건강 측정 데이터를 찾을 수 없음
  - `500`: 데이터 조회 실패

### 6. 건강 측정 데이터 삭제
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

### 0. 개발 중,,,

---

## 👥 Monitoring API

**Base URL**: `/monitoring`

### 1. 모니터링 요청 생성
- **Endpoint**: `POST /monitoring/request`
- **설명**: 의사/보호자가 환자에게 모니터링 요청
- **Request Body**: `MonitoringRequestCreate`
  ```json
  {
    "patient_id": "patient001",
    "requester_id": "doctor001"
  }
  ```
- **Response**: `MonitoringRequestResponse` (201 Created)
  ```json
  {
    "id": "req_123",
    "patient_id": "patient001",
    "patient_name": "김환자",
    "requester_id": "doctor001",
    "requester_name": "이의사",
    "requester_role": "DOCTOR",
    "status": "PENDING",
    "created_at": "2025-12-05T10:00:00",
    "responded_at": null
  }
  ```
- **Error**:
  - `400`: 환자/요청자를 찾을 수 없음, 이미 모니터링 관계가 존재함
  - `500`: 요청 생성 실패

### 2. 대기 중인 요청 조회 (환자용)
- **Endpoint**: `GET /monitoring/requests/pending/{patient_id}`
- **설명**: 환자가 받은 대기 중인 모니터링 요청 목록
- **Path Parameter**:
  - `patient_id`: 환자 아이디
- **Response**: `List[MonitoringRequestResponse]` (200 OK)
  ```json
  [
    {
      "id": "req_123",
      "patient_id": "patient001",
      "patient_name": "",
      "requester_id": "doctor001",
      "requester_name": "이의사",
      "requester_role": "DOCTOR",
      "status": "PENDING",
      "created_at": "2025-12-05T10:00:00",
      "responded_at": null
    }
  ]
  ```

### 3. 모니터링 요청 승인/거부
- **Endpoint**: `POST /monitoring/approve`
- **설명**: 환자가 모니터링 요청 승인 또는 거부
- **Request Body**: `MonitoringApproval`
  ```json
  {
    "request_id": "req_123",
    "approved": true
  }
  ```
- **Response**: `MonitoringRequestResponse` (200 OK)
  ```json
  {
    "id": "req_123",
    "patient_id": "patient001",
    "patient_name": "김환자",
    "requester_id": "doctor001",
    "requester_name": "이의사",
    "requester_role": "DOCTOR",
    "status": "APPROVED",
    "created_at": "2025-12-05T10:00:00",
    "responded_at": "2025-12-05T11:00:00"
  }
  ```
- **Error**:
  - `400`: 요청을 찾을 수 없음, 이미 처리된 요청
  - `500`: 요청 처리 실패
- **참고**:
  - `approved: true` 시 자동으로 `monitoring_relations`에 관계 생성
  - `approved: false` 시 요청만 REJECTED로 변경

### 4. 모니터링 관계 조회 (환자용)
- **Endpoint**: `GET /monitoring/relations/{patient_id}`
- **설명**: 특정 환자의 승인된 모니터링 관계 목록
- **Path Parameter**:
  - `patient_id`: 환자 아이디
- **Response**: `List[MonitoringRelationResponse]` (200 OK)
  ```json
  [
    {
      "id": "rel_456",
      "patient_id": "patient001",
      "patient_name": "",
      "monitor_id": "doctor001",
      "monitor_name": "이의사",
      "monitor_role": "DOCTOR",
      "granted_at": "2025-12-05T11:00:00"
    }
  ]
  ```

### 5. 내가 모니터링하는 환자 목록 (의사/보호자용)
- **Endpoint**: `GET /monitoring/my-patients/{monitor_id}`
- **설명**: 의사/보호자가 모니터링 중인 환자 목록
- **Path Parameter**:
  - `monitor_id`: 의사/보호자 아이디
- **Response**: `List[MonitoringRelationResponse]` (200 OK)
  ```json
  [
    {
      "id": "rel_456",
      "patient_id": "patient001",
      "patient_name": "김환자",
      "monitor_id": "doctor001",
      "monitor_name": "",
      "monitor_role": "",
      "granted_at": "2025-12-05T11:00:00"
    }
  ]
  ```

### 6. 모니터링 관계 해제
- **Endpoint**: `DELETE /monitoring/relation/{relation_id}`
- **설명**: 승인된 모니터링 관계 해제
- **Path Parameter**:
  - `relation_id`: 관계 ID
- **Response**: `204 No Content`
- **Error**:
  - `404`: 모니터링 관계를 찾을 수 없음
  - `500`: 관계 해제 실패
- **참고**: 관계가 해제되면 연결된 요청 기록도 함께 삭제됨

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

#### 8️⃣ 모니터링 시스템 테스트
```bash
# 8-1. 의사 회원가입
POST {{BASE_URL}}/users/register
Content-Type: application/json

{
  "id": "doctor001",
  "password": "doc1234",
  "name": "이의사",
  "role": "DOCTOR"
}

# 8-2. 모니터링 요청 (의사 → 환자)
POST {{BASE_URL}}/monitoring/request
Content-Type: application/json

{
  "patient_id": "patient001",
  "requester_id": "doctor001"
}

# 8-3. 대기 중인 요청 확인 (환자)
GET {{BASE_URL}}/monitoring/requests/pending/patient001

# 8-4. 요청 승인 (환자)
POST {{BASE_URL}}/monitoring/approve
Content-Type: application/json

{
  "request_id": "req_123",
  "approved": true
}

# 8-5. 내가 모니터링하는 환자 목록 (의사)
GET {{BASE_URL}}/monitoring/my-patients/doctor001

# 8-6. 환자의 모니터링 관계 목록 (환자)
GET {{BASE_URL}}/monitoring/relations/patient001

# 8-7. 관계 해제
DELETE {{BASE_URL}}/monitoring/relation/{relation_id}
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
    },
    {
      "name": "Monitoring",
      "item": [
        {
          "name": "의사 회원가입",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{BASE_URL}}/users/register",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"id\": \"doctor001\",\n  \"password\": \"doc1234\",\n  \"name\": \"이의사\",\n  \"role\": \"DOCTOR\"\n}"
            }
          }
        },
        {
          "name": "모니터링 요청 생성",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{BASE_URL}}/monitoring/request",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"patient_id\": \"{{user_id}}\",\n  \"requester_id\": \"doctor001\"\n}"
            }
          }
        },
        {
          "name": "대기 중인 요청 조회",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/monitoring/requests/pending/{{user_id}}"
          }
        },
        {
          "name": "요청 승인",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{BASE_URL}}/monitoring/approve",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"request_id\": \"{request_id}\",\n  \"approved\": true\n}"
            }
          }
        },
        {
          "name": "내가 모니터링하는 환자",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/monitoring/my-patients/doctor001"
          }
        },
        {
          "name": "환자의 모니터링 관계",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/monitoring/relations/{{user_id}}"
          }
        },
        {
          "name": "관계 해제",
          "request": {
            "method": "DELETE",
            "url": "{{BASE_URL}}/monitoring/relation/{relation_id}"
          }
        }
      ]
    }
  ]
}
```

### 테스트 순서
1. **회원가입** → 환자 계정 생성 (patient001)
2. **로그인** → 인증 확인
3. **사용자 정보 수정** → 이름 또는 비밀번호 변경 (선택)
4. **건강 프로필 수정** → 기본 건강 정보 설정
5. **건강 프로필 조회** → 저장된 정보 확인
6. **건강 측정 데이터 생성** (여러 번) → 시계열 데이터 축적
7. **사용자 측정 데이터 조회** → 모든 측정 기록 확인
8. **최신 측정 데이터 조회** → 가장 최근 기록만 확인
9. **의사 회원가입** → 의사 계정 생성 (doctor001)
10. **모니터링 요청** → 의사가 환자에게 요청
11. **대기 중인 요청 조회** → 환자가 요청 확인
12. **요청 승인** → 환자가 승인
13. **모니터링 관계 확인** → 양방향 확인
14. **관계 해제** → 모니터링 종료 (선택)
