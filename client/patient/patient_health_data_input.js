const BASE_URL = "http://localhost:8000";

// 페이지 로드 시 사용자 정보 확인
window.addEventListener('DOMContentLoaded', () => {
    const userId = localStorage.getItem('currentUserId');
    const userName = localStorage.getItem('currentUserName');
    
    if (!userId || !userName) {
        alert('로그인이 필요합니다.');
        window.location.href = 'index.html';
        return;
    }
    
    document.getElementById('userName').textContent = userName;
    document.getElementById('displayUserName').textContent = userName;
});

document.getElementById('healthForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleSubmitHealth();
});

async function handleSubmitHealth() {
    const bp = document.getElementById('bpInput').value;
    const sugar = document.getElementById('sugarInput').value;
    const drinking = document.getElementById('drinkingInput').value === "true";
    const smoking = document.getElementById('smokingInput').value === "true";

    if (!bp || !sugar) {
        alert("모든 수치를 입력해주세요.");
        return;
    }

    const currentUserId = localStorage.getItem('currentUserId');

    // 프론트에서 백엔드로 요청하는 데이터
    const payload = {
        user_id: currentUserId,
        sex: "M",
        birth_date: "1990-01-01",
        height_cm: 170,
        weight_kg: 70,
        systolic_bp: parseInt(bp),
        diastolic_bp: 80,
        glucose_level: parseInt(sugar),
        drinking: drinking ? 10 : 0,
        smoking: smoking ? 10 : 0,
        stroke_history: false,
        hypertension: false,
        heart_disease: false,
        diabetes: false,
        drinking_status: drinking
        smoking_status: smoking
    };

    try {
        const res = await fetch(`${BASE_URL}/health/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok) {
            // 건강 데이터 입력 저장
            localStorage.setItem('riskLevel', data.risk_level || "MEDIUM");
            
            // 환자 홈 페이지로 이동
            window.location.href = 'patient_home.html';
        } else {
            alert("데이터 처리 오류");
        }
    } catch (error) {
        console.error(error);
        alert("서버 오류 발생");
    }
}
