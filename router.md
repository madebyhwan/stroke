# 🔗 StrokeManage API 명세서

뇌졸중 위험도 분석 및 모니터링 시스템 REST API 문서

## 📑 목차

1. [User API](#1-user-api) - 사용자 인증/관리
2. [Health API](#2-health-api) - 건강 데이터 관리
3. [Monitoring API](#3-monitoring-api) - 모니터링 관계 관리
4. [Memo API](#4-memo-api) - 메모 관리
5. [에러 코드](#5-에러-코드)
6. [데이터 타입](#6-데이터-타입)

---

## 1. User API

### 1.1 회원가입
사용자 계정을 생성합니다. 환자 계정의 경우 건강 프로필 정보를 함께 입력할 수 있습니다.

- **Endpoint**: `POST /users/register`
- **Request Body**:
```json
{
  "id": "patient001",
  "password": "securePassword123",
  "name": "김환자",
  "role": "PATIENT",
  
  // 환자일 경우 건강 프로필 (선택사항)
  "sex": "M",
  "birth_date": "1990-05-15",
  "height_cm": 175,
  "stroke_history": false,
  "hypertension": true,
  "heart_disease": false,
  "smoking_history": "NON_SMOKER",
  "diabetes": false
}
```

**Request Body 필드**:
- `id` (required): 사용자 ID (고유값)
- `password` (required): 비밀번호
- `name` (required): 사용자 이름
- `role` (required): 사용자 역할 (`PATIENT`, `DOCTOR`, `CAREGIVER`)
- `sex` (optional): 성별 (`M`, `F`)
- `birth_date` (optional): 생년월일 (YYYY-MM-DD)
- `height_cm` (optional): 키 (cm)
- `stroke_history` (optional): 뇌졸중 이력 (true/false)
- `hypertension` (optional): 고혈압 여부 (true/false)
- `heart_disease` (optional): 심장병 여부 (true/false)
- `smoking_history` (optional): 흡연 이력 (`NON_SMOKER`, `PAST_SMOKER`, `SMOKER`)
- `diabetes` (optional): 당뇨병 여부 (true/false)

- **Response** (200 OK):
```json
{
  "id": "patient001",
  "name": "김환자",
  "role": "PATIENT"
}
```

---

### 1.2 로그인
사용자 인증을 수행합니다.

- **Endpoint**: `POST /users/login`
- **Request Body**:
```json
{
  "id": "patient001",
  "password": "securePassword123"
}
```

- **Response** (200 OK):
```json
{
  "id": "patient001",
  "name": "김환자",
  "role": "PATIENT"
}
```

- **Error Responses**:
  - `401 Unauthorized`: 비밀번호 오류
  - `404 Not Found`: 존재하지 않는 사용자

---

### 1.3 사용자 조회
특정 사용자의 기본 정보를 조회합니다.

- **Endpoint**: `GET /users/{user_id}`
- **Path Parameters**:
  - `user_id`: 조회할 사용자 ID

- **Response** (200 OK):
```json
{
  "id": "patient001",
  "name": "김환자",
  "role": "PATIENT"
}
```

**⚠️ 알려진 이슈**: 현재 UserResponse 스키마가 기본 정보만 반환하여 건강 프로필 필드 (sex, birth_date, height_cm 등)가 누락됩니다. 모니터 모달에서 환자 상세 정보가 표시되지 않는 문제가 있습니다.

---

### 1.4 사용자 정보 수정
사용자의 이름 또는 비밀번호를 수정합니다. 역할(role)은 보안상 수정할 수 없습니다.

- **Endpoint**: `PUT /users/{user_id}`
- **Path Parameters**:
  - `user_id`: 수정할 사용자 ID

- **Request Body**:
```json
{
  "id": "patient001",
  "name": "김환자(수정)",
  "password": "newPassword456"
}
```

**Request Body 필드** (모두 선택사항):
- `id` (required): 사용자 ID
- `name` (optional): 새로운 이름
- `password` (optional): 새로운 비밀번호

- **Response** (200 OK):
```json
{
  "id": "patient001",
  "name": "김환자(수정)",
  "role": "PATIENT"
}
```

---

### 1.5 건강 프로필 조회
사용자의 건강 프로필 정보를 조회합니다. 환자 계정에서만 사용됩니다.

- **Endpoint**: `GET /users/{user_id}/health`
- **Path Parameters**:
  - `user_id`: 조회할 사용자 ID

- **Response** (200 OK):
```json
{
  "sex": "M",
  "birth_date": "1990-05-15",
  "height_cm": 175,
  "stroke_history": false,
  "hypertension": true,
  "heart_disease": false,
  "smoking_history": "NON_SMOKER",
  "diabetes": false,
  "measured_at": "2025-12-06T10:00:00Z"
}
```

---

### 1.6 건강 프로필 수정
사용자의 건강 프로필 정보를 수정합니다.

- **Endpoint**: `PUT /users/{user_id}/health`
- **Path Parameters**:
  - `user_id`: 수정할 사용자 ID

- **Request Body**:
```json
{
  "id": "patient001",
  "sex": "M",
  "birth_date": "1990-05-15",
  "height_cm": 176,
  "stroke_history": true,
  "hypertension": true,
  "heart_disease": false,
  "smoking_history": "PAST_SMOKER",
  "diabetes": false,
  "measured_at": "2025-12-06T10:30:00Z"
}
```

- **Response** (200 OK):
```json
{
  "sex": "M",
  "birth_date": "1990-05-15",
  "height_cm": 176,
  "stroke_history": true,
  "hypertension": true,
  "heart_disease": false,
  "smoking_history": "PAST_SMOKER",
  "diabetes": false,
  "measured_at": "2025-12-06T10:30:00Z"
}
```

---

## 2. Health API

### 2.1 건강 데이터 생성
새로운 건강 측정 데이터를 생성하고, 뇌졸중 위험도를 자동으로 계산합니다.

- **Endpoint**: `POST /health/records`
- **Request Body**:
```json
{
  "user_id": "patient001",
  "weight_kg": 72.5,
  "systolic_bp": 135,
  "diastolic_bp": 88,
  "glucose_level": 110,
  "smoking": 5
}
```

**Request Body 필드**:
- `user_id` (required): 사용자 ID
- `weight_kg` (required): 체중 (kg)
- `systolic_bp` (required): 수축기 혈압 (mmHg)
- `diastolic_bp` (required): 이완기 혈압 (mmHg)
- `glucose_level` (required): 혈당 수치 (mg/dL)
- `smoking` (required): 하루 흡연량 (개비)

- **Response** (201 Created):
```json
{
  "id": "record_001",
  "user_id": "patient001",
  "weight_kg": 72.5,
  "systolic_bp": 135,
  "diastolic_bp": 88,
  "glucose_level": 110,
  "smoking": 5,
  "created_at": "2025-12-06T14:30:00Z",
  "stroke_risk_score": 48.5,
  "stroke_risk_level": "높음"
}
```

**자동 계산 필드**:
- `stroke_risk_score`: 0-100 사이 위험도 점수
- `stroke_risk_level`: 위험도 등급 (`낮음`, `보통`, `높음`, `매우 높음`)

---

### 2.2 사용자 건강 데이터 조회
특정 사용자의 모든 건강 측정 기록을 조회합니다. 최신 순으로 정렬됩니다.

- **Endpoint**: `GET /health/records/user/{user_id}`
- **Path Parameters**:
  - `user_id`: 조회할 사용자 ID

- **Query Parameters**:
  - `limit` (optional): 조회할 최대 개수 (기본값: 전체)

- **Response** (200 OK):
```json
[
  {
    "id": "record_002",
    "user_id": "patient001",
    "weight_kg": 72.5,
    "systolic_bp": 135,
    "diastolic_bp": 88,
    "glucose_level": 110,
    "smoking": 5,
    "created_at": "2025-12-06T14:30:00Z",
    "stroke_risk_score": 48.5,
    "stroke_risk_level": "높음"
  },
  {
    "id": "record_001",
    "user_id": "patient001",
    "weight_kg": 70.0,
    "systolic_bp": 125,
    "diastolic_bp": 80,
    "glucose_level": 95,
    "smoking": 0,
    "created_at": "2025-12-05T10:00:00Z",
    "stroke_risk_score": 35.0,
    "stroke_risk_level": "보통"
  }
]
```

---

### 2.3 최신 건강 데이터 조회
특정 사용자의 가장 최근 건강 측정 데이터를 조회합니다.

- **Endpoint**: `GET /health/records/user/{user_id}/latest`
- **Path Parameters**:
  - `user_id`: 조회할 사용자 ID

- **Response** (200 OK):
```json
{
  "id": "record_002",
  "user_id": "patient001",
  "weight_kg": 72.5,
  "systolic_bp": 135,
  "diastolic_bp": 88,
  "glucose_level": 110,
  "smoking": 5,
  "created_at": "2025-12-06T14:30:00Z",
  "stroke_risk_score": 48.5,
  "stroke_risk_level": "높음"
}
```

---

### 2.4 모니터링용 환자 건강 데이터 조회
모니터(의사/보호자)가 승인된 환자의 건강 데이터를 조회합니다. 권한이 확인됩니다.

- **Endpoint**: `GET /health/records/monitor/{monitor_id}/patient/{patient_id}`
- **Path Parameters**:
  - `monitor_id`: 모니터 사용자 ID
  - `patient_id`: 환자 사용자 ID

- **Query Parameters**:
  - `limit` (optional): 조회할 최대 개수

- **Response** (200 OK):
```json
[
  {
    "id": "record_002",
    "user_id": "patient001",
    "weight_kg": 72.5,
    "systolic_bp": 135,
    "diastolic_bp": 88,
    "glucose_level": 110,
    "smoking": 5,
    "created_at": "2025-12-06T14:30:00Z",
    "stroke_risk_score": 48.5,
    "stroke_risk_level": "높음"
  }
]
```

- **Error Responses**:
  - `403 Forbidden`: 모니터링 권한 없음
  - `404 Not Found`: 모니터링 관계 미존재

---

### 2.5 건강 데이터 삭제
특정 건강 측정 데이터를 삭제합니다.

- **Endpoint**: `DELETE /health/records/{record_id}`
- **Path Parameters**:
  - `record_id`: 삭제할 건강 기록 ID

- **Response** (200 OK):
```json
{
  "message": "Health record deleted successfully"
}
```

---

## 3. Monitoring API

### 3.1 모니터링 요청 생성
의사 또는 보호자가 환자에게 모니터링 요청을 보냅니다.

- **Endpoint**: `POST /monitoring/request`
- **Request Body**:
```json
{
  "patient_id": "patient001",
  "requester_id": "doctor001"
}
```

**Request Body 필드**:
- `patient_id` (required): 모니터링할 환자 ID
- `requester_id` (required): 요청자 ID (의사/보호자)

- **Response** (201 Created):
```json
{
  "id": "req_001",
  "patient_id": "patient001",
  "patient_name": "김환자",
  "requester_id": "doctor001",
  "requester_name": "김의사",
  "requester_role": "DOCTOR",
  "status": "PENDING",
  "created_at": "2025-12-06T10:00:00Z",
  "responded_at": null
}
```

---

### 3.2 받은 모니터링 요청 조회
환자가 받은 모니터링 요청 목록을 조회합니다.

- **Endpoint**: `GET /monitoring/requests/received/{user_id}`
- **Path Parameters**:
  - `user_id`: 환자 ID

- **Response** (200 OK):
```json
[
  {
    "id": "req_001",
    "patient_id": "patient001",
    "patient_name": "김환자",
    "requester_id": "doctor001",
    "requester_name": "김의사",
    "requester_role": "DOCTOR",
    "status": "PENDING",
    "created_at": "2025-12-06T10:00:00Z",
    "responded_at": null
  }
]
```

---

### 3.3 보낸 모니터링 요청 조회
의사/보호자가 보낸 모니터링 요청 목록을 조회합니다.

- **Endpoint**: `GET /monitoring/requests/sent/{user_id}`
- **Path Parameters**:
  - `user_id`: 요청자 ID

- **Response** (200 OK):
```json
[
  {
    "id": "req_001",
    "patient_id": "patient001",
    "patient_name": "김환자",
    "requester_id": "doctor001",
    "requester_name": "김의사",
    "requester_role": "DOCTOR",
    "status": "PENDING",
    "created_at": "2025-12-06T10:00:00Z",
    "responded_at": null
  }
]
```

---

### 3.4 모니터링 요청 응답
환자가 모니터링 요청을 승인 또는 거절합니다.

- **Endpoint**: `PUT /monitoring/request/{request_id}/respond`
- **Path Parameters**:
  - `request_id`: 모니터링 요청 ID

- **Request Body**:
```json
{
  "request_id": "req_001",
  "approved": true
}
```

**Request Body 필드**:
- `request_id` (required): 요청 ID
- `approved` (required): true (승인) / false (거절)

- **Response** (200 OK):
```json
{
  "id": "req_001",
  "patient_id": "patient001",
  "patient_name": "김환자",
  "requester_id": "doctor001",
  "requester_name": "김의사",
  "requester_role": "DOCTOR",
  "status": "APPROVED",
  "created_at": "2025-12-06T10:00:00Z",
  "responded_at": "2025-12-06T11:00:00Z"
}
```

**상태 변화**:
- `approved: true` → `status: "APPROVED"` (monitoring_relations 컬렉션에 관계 생성)
- `approved: false` → `status: "REJECTED"`

---

### 3.5 모니터링 요청 취소
요청자가 대기 중인 모니터링 요청을 취소합니다.

- **Endpoint**: `DELETE /monitoring/request/{request_id}`
- **Path Parameters**:
  - `request_id`: 모니터링 요청 ID

- **Response** (200 OK):
```json
{
  "message": "Monitoring request cancelled successfully"
}
```

---

### 3.6 내 환자 목록 조회
의사/보호자가 모니터링 중인 환자 목록을 조회합니다.

- **Endpoint**: `GET /monitoring/my-patients/{monitor_id}`
- **Path Parameters**:
  - `monitor_id`: 모니터 사용자 ID

- **Response** (200 OK):
```json
[
  {
    "id": "rel_001",
    "patient_id": "patient001",
    "patient_name": "김환자",
    "monitor_id": "doctor001",
    "monitor_name": "김의사",
    "monitor_role": "DOCTOR",
    "granted_at": "2025-12-06T11:00:00Z"
  }
]
```

---

### 3.7 나를 모니터링하는 사람 조회
환자가 자신을 모니터링하는 의사/보호자 목록을 조회합니다.

- **Endpoint**: `GET /monitoring/my-monitors/{patient_id}`
- **Path Parameters**:
  - `patient_id`: 환자 ID

- **Response** (200 OK):
```json
[
  {
    "id": "rel_001",
    "patient_id": "patient001",
    "patient_name": "김환자",
    "monitor_id": "doctor001",
    "monitor_name": "김의사",
    "monitor_role": "DOCTOR",
    "granted_at": "2025-12-06T11:00:00Z"
  }
]
```

---

### 3.8 모니터링 관계 해제
환자 또는 모니터가 모니터링 관계를 해제합니다.

- **Endpoint**: `DELETE /monitoring/relation/{relation_id}`
- **Path Parameters**:
  - `relation_id`: 모니터링 관계 ID

- **Response** (200 OK):
```json
{
  "message": "Monitoring relation removed successfully"
}
```

---

## 4. Memo API

### 4.1 메모 작성
의사가 환자에게 메모를 작성합니다.

- **Endpoint**: `POST /memos`
- **Request Body**:
```json
{
  "doctor_id": "doctor001",
  "patient_id": "patient001",
  "content": "혈압이 높습니다. 염분 섭취를 줄이시고, 규칙적인 운동을 시작하세요."
}
```

**Request Body 필드**:
- `doctor_id` (required): 작성자 의사 ID
- `patient_id` (required): 대상 환자 ID
- `content` (required): 메모 내용

- **Response** (201 Created):
```json
{
  "id": "memo_001",
  "doctor_id": "doctor001",
  "patient_id": "patient001",
  "content": "혈압이 높습니다. 염분 섭취를 줄이시고, 규칙적인 운동을 시작하세요.",
  "created_at": "2025-12-06T15:00:00Z"
}
```

**권한**: 의사(DOCTOR) 역할만 메모 작성 가능

---

### 4.2 메모 목록 조회
환자 또는 의사가 메모 목록을 조회합니다.

- **Endpoint**: `GET /memos`
- **Query Parameters**:
  - `patient_id` (optional): 특정 환자의 메모 필터링
  - `doctor_id` (optional): 특정 의사의 메모 필터링

- **Response** (200 OK):
```json
[
  {
    "id": "memo_002",
    "doctor_id": "doctor001",
    "patient_id": "patient001",
    "content": "혈당 수치가 개선되었습니다. 현재 식단을 유지하세요.",
    "created_at": "2025-12-07T10:00:00Z"
  },
  {
    "id": "memo_001",
    "doctor_id": "doctor001",
    "patient_id": "patient001",
    "content": "혈압이 높습니다. 염분 섭취를 줄이시고, 규칙적인 운동을 시작하세요.",
    "created_at": "2025-12-06T15:00:00Z"
  }
]
```

**사용 예시**:
- `/memos?patient_id=patient001`: patient001의 모든 메모
- `/memos?doctor_id=doctor001`: doctor001이 작성한 모든 메모
- `/memos?patient_id=patient001&doctor_id=doctor001`: 특정 의사→환자 메모

---

### 4.3 특정 메모 조회
메모 ID로 특정 메모를 조회합니다.

- **Endpoint**: `GET /memos/{memo_id}`
- **Path Parameters**:
  - `memo_id`: 메모 ID

- **Response** (200 OK):
```json
{
  "id": "memo_001",
  "doctor_id": "doctor001",
  "patient_id": "patient001",
  "content": "혈압이 높습니다. 염분 섭취를 줄이시고, 규칙적인 운동을 시작하세요.",
  "created_at": "2025-12-06T15:00:00Z"
}
```

---

### 4.4 메모 삭제
작성자 본인만 메모를 삭제할 수 있습니다.

- **Endpoint**: `DELETE /memos/{memo_id}`
- **Path Parameters**:
  - `memo_id`: 삭제할 메모 ID

- **Response** (200 OK):
```json
{
  "message": "Memo deleted successfully"
}
```

**권한**: 메모 작성자(doctor_id)만 삭제 가능

---

## 5. 에러 코드

### HTTP 상태 코드
- `200 OK`: 요청 성공
- `201 Created`: 리소스 생성 성공
- `400 Bad Request`: 잘못된 요청 (유효성 검증 실패)
- `401 Unauthorized`: 인증 실패 (비밀번호 오류)
- `403 Forbidden`: 권한 없음 (모니터링 미승인, 메모 삭제 권한 등)
- `404 Not Found`: 리소스 없음 (사용자, 건강 데이터, 모니터링 관계 등)
- `409 Conflict`: 리소스 충돌 (중복 ID, 중복 모니터링 요청)
- `500 Internal Server Error`: 서버 오류

### 에러 응답 형식
```json
{
  "detail": "에러 메시지 설명"
}
```

**일반적인 에러 메시지**:
- `"User not found"`: 사용자 없음
- `"Password incorrect"`: 비밀번호 오류
- `"Monitoring relationship not found"`: 모니터링 관계 미존재
- `"Not authorized to view this patient's data"`: 데이터 조회 권한 없음
- `"Only the memo author can delete this memo"`: 메모 삭제 권한 없음

---

## 6. 데이터 타입

### 6.1 열거형 (Enum)

#### UserRole
사용자 역할
```python
"PATIENT"    # 환자
"DOCTOR"     # 의사
"CAREGIVER"  # 보호자
```

#### sexEnum
성별
```python
"M"  # 남성 (Male)
"F"  # 여성 (Female)
```

#### smokingEnum
흡연 이력
```python
"NON_SMOKER"   # 비흡연자
"PAST_SMOKER"  # 과거 흡연자
"SMOKER"       # 현재 흡연자
```

#### MonitoringStatus
모니터링 요청 상태
```python
"PENDING"   # 대기 중
"APPROVED"  # 승인됨
"REJECTED"  # 거절됨
```

### 6.2 위험도 분류

#### stroke_risk_level
뇌졸중 위험도 등급
```python
"낮음"        # 0 ≤ score < 20
"보통"        # 20 ≤ score < 40
"높음"        # 40 ≤ score < 60
"매우 높음"   # 60 ≤ score
```

### 6.3 날짜 형식

#### date
날짜 형식 (ISO 8601)
```
"YYYY-MM-DD"
예: "1990-05-15"
```

#### datetime
날짜+시간 형식 (ISO 8601 with timezone)
```
"YYYY-MM-DDTHH:MM:SSZ"
예: "2025-12-06T14:30:00Z"
```

---

## 📌 추가 정보

### 인증 시스템
현재 버전은 기본적인 ID/비밀번호 인증을 사용합니다.
**향후 개선 계획**:
- JWT 토큰 기반 인증
- bcrypt 비밀번호 해싱
- 세션 관리

### 권한 시스템
- **환자**: 본인의 건강 데이터 생성/조회/삭제, 모니터링 요청 승인/거절, 메모 조회
- **의사**: 승인된 환자 데이터 조회, 메모 작성/삭제, 모니터링 요청
- **보호자**: 승인된 환자 데이터 조회, 모니터링 요청

### 데이터 흐름
1. **회원가입** → 사용자 계정 생성 (건강 프로필 포함)
2. **로그인** → 사용자 인증
3. **건강 데이터 입력** → 위험도 자동 계산
4. **모니터링 요청** → 환자 승인 → 관계 생성
5. **메모 작성** → 환자에게 알림
6. **그래프 표시** → 최근 7개 데이터 포인트로 추세 분석

### 컬렉션 간 관계
```
users (1) ─── (N) health_records
users (1) ─── (N) monitoring_requests (requester)
users (1) ─── (N) monitoring_requests (patient)
users (1) ─── (N) monitoring_relations (monitor)
users (1) ─── (N) monitoring_relations (patient)
users (1) ─── (N) memos (doctor)
users (1) ─── (N) memos (patient)
```

---

**Last Updated**: 2025-12-06  
**API Version**: 1.0  
**Base URL**: `http://localhost:8000`
