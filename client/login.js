// 백엔드 서버 기본 URL
const BASE_URL = "http://localhost:8000";

// 로그인 폼 제출 이벤트 등록
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();     // 새로고침 방지
    await handleLogin();    // 로그인 처리 함수 호출
});

async function handleLogin() {
    // 입력값 가져오기
    const id = document.getElementById('userId').value;
    const password = document.getElementById('userPassword').value;

    // 필수값 확인
    if (!id || !password) {
        alert("아이디와 비밀번호를 모두 입력해주세요.");
        return;
    }

    // 서버로 보낼 데이터
    const payload = {
        id: id,
        password: password
    };

    try {
        // 로그인 요청
        const res = await fetch(`${BASE_URL}/users/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok) {
            // 로그인 성공 → 사용자 정보 저장
            localStorage.setItem("currentUserId", data.id);
            localStorage.setItem("currentUserName", data.name);
            localStorage.setItem("currentUserRole", data.role);

            // 메인 페이지로 이동
            window.location.href = "patient_home.html";
        } else {
            // 실패 메시지 출력
            alert("로그인 실패: " + (data.detail ?? JSON.stringify(data)));
        }

    } catch (error) {
        alert("서버 연결 실패! 백엔드가 켜져 있나요?");
        console.error(error);
    }
}
