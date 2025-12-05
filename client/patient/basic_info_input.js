const BASE_URL = "http://localhost:8000";

// 페이지 로드 시 사용자 정보 확인 및 기존 데이터 불러오기
window.addEventListener('DOMContentLoaded', async () => {
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
    
    // 기존 기본 정보 불러오기 (있으면 폼에 채우기)
    await loadExistingBasicInfo(userId);
});

// 기존 기본 정보 불러오기
async function loadExistingBasicInfo(userId) {
    try {
        const response = await fetch(`${BASE_URL}/user/basic-info/${userId}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (response.ok) {
            const data = await response.json();
            
            // 폼에 기존 데이터 채우기
            if (data.birth_date) {
                document.getElementById('birthDate').value = data.birth_date;
            }
            if (data.sex) {
                document.querySelector(`input[name="sex"][value="${data.sex}"]`).checked = true;
            }
            if (data.height_cm) {
                document.getElementById('height').value = data.height_cm;
            }
            
            // 기저 질환
            document.getElementById('hypertension').checked = data.hypertension || false;
            document.getElementById('diabetes').checked = data.diabetes || false;
            document.getElementById('heartDisease').checked = data.heart_disease || false;
            document.getElementById('strokeHistory').checked = data.stroke_history || false;
            
            // 흡연 여부
            if (data.smoking_status !== undefined) {
                document.querySelector(`input[name="smoking"][value="${data.smoking_status}"]`).checked = true;
            }
            
            // 음주 여부
            if (data.drinking_frequency) {
                document.getElementById('drinking').value = data.drinking_frequency;
            }
        }
    } catch (error) {
        console.log('기존 기본 정보가 없습니다. 새로 입력합니다.');
    }
}

// 폼 제출 처리
document.getElementById('basicInfoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleSubmitBasicInfo();
});

async function handleSubmitBasicInfo() {
    const userId = localStorage.getItem('currentUserId');
    
    // 폼 데이터 수집
    const basicInfo = {
        user_id: userId,
        birth_date: document.getElementById('birthDate').value,
        sex: document.querySelector('input[name="sex"]:checked').value,
        height_cm: parseFloat(document.getElementById('height').value),
        hypertension: document.getElementById('hypertension').checked,
        diabetes: document.getElementById('diabetes').checked,
        heart_disease: document.getElementById('heartDisease').checked,
        stroke_history: document.getElementById('strokeHistory').checked,
        smoking_status: document.querySelector('input[name="smoking"]:checked').value === 'true',
        drinking_frequency: document.getElementById('drinking').value
    };

    try {
        // PUT 요청으로 업데이트 (없으면 생성)
        const response = await fetch(`${BASE_URL}/user/basic-info`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(basicInfo)
        });

        if (response.ok) {
            alert('기본 정보가 저장되었습니다.');
            window.location.href = 'health_input.html';
        } else {
            const error = await response.json();
            alert(`저장 실패: ${error.detail || '알 수 없는 오류'}`);
        }
    } catch (error) {
        console.error('기본 정보 저장 오류:', error);
        alert('서버 오류가 발생했습니다.');
    }
}