const BASE_URL = "http://localhost:8000";

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleRegister();
});

async function handleRegister() {
    const name = document.getElementById('userName').value;
    const role = document.getElementById('userRole').value;

    if (!name) {
        alert("이름을 입력해주세요.");
        return;
    }

    const payload = {
        id: name + "@test.com",
        password: "password123",
        name: name,
        role: role
    };

    try {
        const res = await fetch(`${BASE_URL}/users/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        if (res.ok) {
            // 사용자 정보 저장
            localStorage.setItem('currentUserId', data.id);
            localStorage.setItem('currentUserName', name);
            
            // 건강 입력 페이지로 이동
            window.location.href = 'health-input.html';
        } else {
            alert("오류 발생: " + JSON.stringify(data));
        }
    } catch (error) {
        alert("서버 연결 실패! 백엔드가 켜져 있나요?");
        console.error(error);
    }
}
