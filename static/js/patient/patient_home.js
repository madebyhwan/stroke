const BASE_URL = "http://127.0.0.1:8000";

const userId = localStorage.getItem("currentUserId");

// 위험도 레벨 판단 함수
function getRiskLevel(score) {
    if (score >= 70) return "위험";
    if (score >= 40) return "주의";
    return "정상";
}

// 위험도에 따른 색상 클래스 반환
function getRiskColorClasses(score) {
    if (score >= 70) {
        return {
            text: "text-red-500",
            bg: "bg-red-100",
            border: "border-red-200",
            chartColor: "#ef4444"
        };
    } else if (score >= 40) {
        return {
            text: "text-yellow-500",
            bg: "bg-yellow-100",
            border: "border-yellow-200",
            chartColor: "#eab308"
        };
    } else {
        return {
            text: "text-teal-600",
            bg: "bg-teal-100",
            border: "border-teal-200",
            chartColor: "#0d9488"
        };
    }
}

// 위험도 계산 함수 (클라이언트 측)
function calculateRiskScore(healthData, healthInfo) {
    let score = 0;
    
    // 혈압 위험도 (수축기)
    if (healthData.systolic_bp >= 180) score += 30;
    else if (healthData.systolic_bp >= 140) score += 20;
    else if (healthData.systolic_bp >= 120) score += 10;
    
    // 혈압 위험도 (이완기)
    if (healthData.diastolic_bp >= 120) score += 20;
    else if (healthData.diastolic_bp >= 90) score += 15;
    else if (healthData.diastolic_bp >= 80) score += 5;
    
    // 혈당 위험도
    if (healthData.glucose_level >= 200) score += 25;
    else if (healthData.glucose_level >= 126) score += 15;
    else if (healthData.glucose_level >= 100) score += 5;
    
    // 흡연 위험도
    if (healthData.smoking >= 20) score += 20;
    else if (healthData.smoking >= 10) score += 15;
    else if (healthData.smoking >= 1) score += 10;
    
    // BMI 계산 (체중과 키)
    if (healthInfo && healthInfo.height_cm) {
        const heightM = healthInfo.height_cm / 100;
        const bmi = healthData.weight_kg / (heightM * heightM);
        
        if (bmi >= 30) score += 15;
        else if (bmi >= 25) score += 10;
        else if (bmi < 18.5) score += 5;
    }
    
    // 기저질환 가중치
    if (healthInfo) {
        if (healthInfo.hypertension) score += 10;
        if (healthInfo.diabetes) score += 10;
        if (healthInfo.heart_disease) score += 15;
        if (healthInfo.stroke_history) score += 20;
    }
    
    return Math.min(Math.round(score), 100);
}

// 상태 설명 텍스트 반환
function getStatusDescription(score) {
    if (score >= 70) {
        return "지속적인 모니터링과 주의가 필요한 상태입니다.";
    } else if (score >= 40) {
        return "정기적인 건강 관리가 필요한 상태입니다.";
    } else {
        return "양호한 상태를 유지하고 계십니다.";
    }
}

async function loadDashboard() {
    if (!userId) {
        alert("로그인이 필요합니다.");
        window.location.href = "/login";
        return;
    }

    try {
        // 사용자 정보 조회
        const userRes = await fetch(`${BASE_URL}/users/${userId}`);
        const userData = await userRes.json();

        if (!userRes.ok) {
            alert("사용자 정보를 불러오지 못했습니다.");
            console.log(userData);
            return;
        }

        // 1. 이름 업데이트
        const userName = userData.name;
        document.getElementById("userNameTitle").innerText = userName;
        document.getElementById("profileName").innerText = userName + " 님";
        
        // 프로필 이니셜 (이름의 마지막 두 글자)
        const initial = userName.length >= 2 ? userName.slice(-2) : userName;
        document.getElementById("profileInitial").innerText = initial;

        // 2. 최신 건강 기록 조회
        let riskScore = 0;
        let lastUpdate = "기록 없음";
        
        try {
            const healthRes = await fetch(`${BASE_URL}/health/records/user/${userId}/latest`);
            if (healthRes.ok) {
                const healthData = await healthRes.json();
                
                // 기본 건강 정보도 가져오기
                const healthInfoRes = await fetch(`${BASE_URL}/users/${userId}/health`);
                let healthInfo = null;
                if (healthInfoRes.ok) {
                    healthInfo = await healthInfoRes.json();
                }
                
                // 위험도 계산 (클라이언트 측)
                riskScore = calculateRiskScore(healthData, healthInfo);
                
                // 날짜 포맷팅
                const date = new Date(healthData.created_at);
                lastUpdate = `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`;
            }
        } catch (error) {
            console.log('건강 기록이 없습니다.');
        }

        // 3. 위험도 퍼센트 표시
        document.getElementById("riskPercent").innerText = riskScore;

        // 4. 위험 레벨 판단
        const riskLevel = getRiskLevel(riskScore);
        const colorClasses = getRiskColorClasses(riskScore);

        // 5. 위험 레벨 텍스트 및 색상 업데이트
        const riskLevelText = document.getElementById("riskLevelText");
        riskLevelText.innerText = riskLevel;
        riskLevelText.className = `text-sm font-bold mt-1 ${colorClasses.text}`;

        // 6. 상태 배지 업데이트
        const statusBadge = document.getElementById("statusBadge");
        statusBadge.className = `inline-block px-4 py-2 rounded-full font-bold mb-2 ${colorClasses.bg} ${colorClasses.text}`;
        document.getElementById("statusText").innerText = riskLevel;

        // 7. 상태 설명 업데이트
        document.getElementById("statusDescription").innerText = getStatusDescription(riskScore);

        // 8. 날짜 업데이트
        document.getElementById("lastUpdate").innerText = lastUpdate;

        // 9. 원형 차트 업데이트
        document.getElementById("riskChart").style.background =
            `conic-gradient(
                ${colorClasses.chartColor} 0% ${riskScore}%,
                #f3f4f6 ${riskScore}% 100%
            )`;

    } catch (err) {
        console.error(err);
        alert("서버 연결 실패! FastAPI가 실행 중인가요?");
    }
}

// 페이지 로드시 자동 실행
window.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
    lucide.createIcons();
});