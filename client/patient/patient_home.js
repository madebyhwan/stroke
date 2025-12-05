const BASE_URL = "http://localhost:8000";

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
        window.location.href = "login.html";
        return;
    }

    try {
        const res = await fetch(`${BASE_URL}/users/${userId}`);
        const data = await res.json();

        if (!res.ok) {
            alert("사용자 정보를 불러오지 못했습니다.");
            console.log(data);
            return;
        }

        // 1. 이름 업데이트
        const userName = data.name;
        document.getElementById("userNameTitle").innerText = userName;
        document.getElementById("profileName").innerText = userName + " 님";
        
        // 프로필 이니셜 (이름의 마지막 두 글자)
        const initial = userName.length >= 2 ? userName.slice(-2) : userName;
        document.getElementById("profileInitial").innerText = initial;

        // 2. 위험도 퍼센트
        const riskScore = data.riskScore;
        document.getElementById("riskPercent").innerText = riskScore;

        // 3. 위험 레벨 판단
        const riskLevel = getRiskLevel(riskScore);
        const colorClasses = getRiskColorClasses(riskScore);

        // 4. 위험 레벨 텍스트 및 색상 업데이트
        const riskLevelText = document.getElementById("riskLevelText");
        riskLevelText.innerText = riskLevel;
        riskLevelText.className = `text-sm font-bold mt-1 ${colorClasses.text}`;

        // 5. 상태 배지 업데이트
        const statusBadge = document.getElementById("statusBadge");
        statusBadge.className = `inline-block px-4 py-2 rounded-full font-bold mb-2 ${colorClasses.bg} ${colorClasses.text}`;
        document.getElementById("statusText").innerText = riskLevel;

        // 6. 상태 설명 업데이트
        document.getElementById("statusDescription").innerText = getStatusDescription(riskScore);

        // 7. 날짜 업데이트
        document.getElementById("lastUpdate").innerText = data.lastUpdate || "2024.05.20";

        // 8. 원형 차트 업데이트
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