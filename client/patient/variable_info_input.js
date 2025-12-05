const BASE_URL = "http://localhost:8000";

// 페이지 로드 시 사용자 정보 확인 및 현재 시간 표시
window.addEventListener('DOMContentLoaded', () => {
    const userId = localStorage.getItem('currentUserId');
    const userName = localStorage.getItem('currentUserName');
    
    if (!userId || !userName) {
        alert('로그인이 필요합니다.');
        window.location.href = 'index.html';
        return;
    }
    
    // 사용자 이름 표시
    document.getElementById('profileName').textContent = `${userName} 님`;
    document.getElementById('profileInitial').textContent = userName.substring(0, 2);
    
    // Lucide 아이콘 초기화
    lucide.createIcons();
    
    // 현재 시간 표시 및 업데이트
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
});

// 현재 시간 표시
function updateCurrentTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const date = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    const timeString = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
    document.getElementById('currentTime').textContent = timeString;
}

// 폼 제출 처리
document.getElementById('variableInfoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleSubmitVariableInfo();
});

async function handleSubmitVariableInfo() {
    const userId = localStorage.getItem('currentUserId');
    
    // 기본 정보 먼저 확인 (키가 필요함)
    let height = null;
    try {
        const basicInfoResponse = await fetch(`${BASE_URL}/user/basic-info/${userId}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        
        if (basicInfoResponse.ok) {
            const basicInfo = await basicInfoResponse.json();
            height = basicInfo.height_cm;
        }
    } catch (error) {
        console.error('기본 정보 조회 오류:', error);
    }
    
    if (!height) {
        alert('기본 정보를 먼저 입력해주세요. (키 정보가 필요합니다)');
        window.location.href = 'basic_info_input.html';
        return;
    }
    
    // 폼 데이터 수집
    const variableInfo = {
        user_id: userId,
        systolic_bp: parseInt(document.getElementById('systolicBp').value),
        diastolic_bp: parseInt(document.getElementById('diastolicBp').value),
        glucose_level: parseInt(document.getElementById('glucoseLevel').value),
        weight_kg: parseFloat(document.getElementById('weight').value),
        height_cm: height, // 기본 정보에서 가져온 키
        created_at: new Date().toISOString() // 현재 시간
    };

    try {
        // POST 요청으로 새 기록 추가
        const response = await fetch(`${BASE_URL}/health/record`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(variableInfo)
        });

        if (response.ok) {
            const data = await response.json();
            alert('건강 기록이 추가되었습니다.');
            
            // 위험도 점수가 있으면 표시
            if (data.risk_score !== undefined) {
                alert(`위험도 점수: ${data.risk_score}점`);
            }
            
            window.location.href = 'health_info.html';
        } else {
            const error = await response.json();
            alert(`저장 실패: ${error.detail || '알 수 없는 오류'}`);
        }
    } catch (error) {
        console.error('가변 정보 저장 오류:', error);
        alert('서버 오류가 발생했습니다.');
    }
}