const BASE_URL = "http://127.0.0.1:8000";

// 페이지 로드 시 사용자 정보 확인
window.addEventListener('DOMContentLoaded', () => {
    const userId = localStorage.getItem('currentUserId');
    const userName = localStorage.getItem('currentUserName');
    
    if (!userId || !userName) {
        alert('로그인이 필요합니다.');
        window.location.href = '/login';
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
    const systolicBp = document.getElementById('bpInput').value;
    const glucoseLevel = document.getElementById('sugarInput').value;
    const weight = document.getElementById('weightInput') ? document.getElementById('weightInput').value : 70;
    const smoking = document.getElementById('smokingInput') ? parseInt(document.getElementById('smokingInput').value) : 0;

    if (!systolicBp || !glucoseLevel) {
        alert("모든 수치를 입력해주세요.");
        return;
    }

    const currentUserId = localStorage.getItem('currentUserId');

    // 백엔드 API에 맞는 payload
    const payload = {
        user_id: currentUserId,
        weight_kg: parseInt(weight),
        systolic_bp: parseInt(systolicBp),
        diastolic_bp: 80, // 기본값 (또는 입력 필드 추가)
        glucose_level: parseInt(glucoseLevel),
        smoking: smoking
    };

    try {
        const res = await fetch(`${BASE_URL}/health/records`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok) {
            alert('건강 기록이 추가되었습니다.');
            // 환자 홈 페이지로 이동
            window.location.href = '/patient/home';
        } else {
            alert("데이터 처리 오류: " + (data.detail || JSON.stringify(data)));
        }
    } catch (error) {
        console.error(error);
        alert("서버 오류 발생");
    }
}
