# RiskCalculator에 대응
# stroke risk 계산 모델을 구현하는 모듈

from datetime import datetime, date
from typing import Optional

def calculate_stroke_risk(
    # 사용자 기본 정보
    age: int,
    sex: str,  # "M" or "F"
    # 건강 상태 (고정)
    stroke_history: bool = False,
    hypertension: bool = False,
    heart_disease: bool = False,
    diabetes: bool = False,
    smoking_history: str = "NON_SMOKER",  # "SMOKER", "PAST_SMOKER", "NON_SMOKER"
    # 측정 데이터 (변동)
    systolic_bp: Optional[int] = None,
    diastolic_bp: Optional[int] = None,
    weight_kg: Optional[float] = None,
    height_cm: Optional[int] = None,
    glucose_level: Optional[int] = None,
    smoking: Optional[int] = None  # 현재 흡연량 (개비/일)
) -> float:
    """
    뇌졸중 위험도 점수 계산 (0-100점)
    
    위험 요인:
    1. 나이 (최대 20점)
    2. 성별 (남성 가산점 5점)
    3. 뇌졸중 이력 (30점)
    4. 고혈압 (15점)
    5. 심장 질환 (15점)
    6. 당뇨병 (10점)
    7. 흡연 (최대 15점)
    8. 혈압 수치 (최대 20점)
    9. BMI (최대 10점)
    10. 혈당 수치 (최대 10점)
    """
    
    risk_score = 0.0
    
    # 1. 나이 (최대 20점)
    # 40세 미만: 0점, 40-50: 5점, 50-60: 10점, 60-70: 15점, 70+: 20점
    if age < 40:
        risk_score += 0
    elif age < 50:
        risk_score += 5
    elif age < 60:
        risk_score += 10
    elif age < 70:
        risk_score += 15
    else:
        risk_score += 20
    
    # 2. 성별 (남성 가산 5점)
    if sex == "M":
        risk_score += 5
    
    # 3. 뇌졸중 이력 (30점) - 가장 중요한 위험 요인
    if stroke_history:
        risk_score += 30
    
    # 4. 고혈압 (15점)
    if hypertension:
        risk_score += 15
    
    # 5. 심장 질환 (15점)
    if heart_disease:
        risk_score += 15
    
    # 6. 당뇨병 (10점)
    if diabetes:
        risk_score += 10
    
    # 7. 흡연 이력 및 현재 흡연량 (최대 15점)
    if smoking_history == "SMOKER" or (smoking and smoking > 0):
        # 현재 흡연자
        if smoking:
            if smoking >= 20:  # 하루 한 갑 이상
                risk_score += 15
            elif smoking >= 10:
                risk_score += 12
            else:
                risk_score += 8
        else:
            risk_score += 10
    elif smoking_history == "PAST_SMOKER":
        # 과거 흡연자
        risk_score += 5
    
    # 8. 혈압 수치 (최대 20점)
    if systolic_bp and diastolic_bp:
        # 고혈압 단계별 점수
        if systolic_bp >= 180 or diastolic_bp >= 120:
            # Stage 3 고혈압 (고혈압 위기)
            risk_score += 20
        elif systolic_bp >= 160 or diastolic_bp >= 100:
            # Stage 2 고혈압
            risk_score += 15
        elif systolic_bp >= 140 or diastolic_bp >= 90:
            # Stage 1 고혈압
            risk_score += 10
        elif systolic_bp >= 130 or diastolic_bp >= 85:
            # 전단계 고혈압
            risk_score += 5
    
    # 9. BMI (최대 10점)
    if weight_kg and height_cm:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi >= 30:
            # 비만 (30 이상)
            risk_score += 10
        elif bmi >= 25:
            # 과체중 (25-30)
            risk_score += 5
        elif bmi < 18.5:
            # 저체중
            risk_score += 3
    
    # 10. 혈당 수치 (최대 10점)
    if glucose_level:
        if glucose_level >= 200:
            # 당뇨병 범위
            risk_score += 10
        elif glucose_level >= 140:
            # 전당뇨 범위
            risk_score += 7
        elif glucose_level >= 100:
            # 공복혈당장애
            risk_score += 4
    
    # 최종 점수는 0-100 사이로 제한
    risk_score = min(risk_score, 100.0)
    
    return round(risk_score, 1)


def get_risk_level(risk_score: float) -> str:
    """
    위험도 점수를 등급으로 변환
    
    Args:
        risk_score: 위험도 점수 (0-100)
    
    Returns:
        위험도 등급: "낮음", "보통", "높음", "매우 높음"
    """
    if risk_score < 20:
        return "낮음"
    elif risk_score < 40:
        return "보통"
    elif risk_score < 60:
        return "높음"
    else:
        return "매우 높음"


def calculate_age(birth_date: date) -> int:
    """생년월일로 나이 계산"""
    today = datetime.now().date()
    age = today.year - birth_date.year
    # 생일이 지나지 않았으면 -1
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age
