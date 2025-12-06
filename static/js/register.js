// 백엔드 서버 기본 URL 설정
const BASE_URL = "http://127.0.0.1:8000";

// 회원가입 폼 제출 시 실행될 이벤트 등록
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();              // 기본 폼 제출 동작(새로고침) 막기
    await handleRegister();          // 회원가입 처리 함수 실행
});

async function handleRegister() {
    // 입력된 사용자 정보 가져오기
    const name = document.getElementById('userName').value;
    const id = document.getElementById('userId').value;
    const password = document.getElementById('userPassword').value;
    const role = document.getElementById('userRole').value;

    // 필수 정보가 비어있으면 경고 발생
    if (!name || !id || !password) {
        alert("모든 칸을 입력해주세요.");
        return; // 함수 종료
    }

    // 서버로 보낼 데이터 객체(payload)
    const payload = {
        id: id,
        password: password,
        name: name,
        role: role
    };

    try {
        // 서버에 회원가입 요청 (POST)
        const res = await fetch(`${BASE_URL}/users/register`, {
            method: "POST",                        // POST 요청
            headers: { "Content-Type": "application/json" }, // JSON 형식으로 전달
            body: JSON.stringify(payload)          // 실제 보낼 데이터
        });
        
        // 서버가 보내준 JSON 데이터를 파싱
        const data = await res.json();
        
        if (res.ok) {
            // 회원가입 성공 시, 사용자 정보 localStorage에 저장
            localStorage.setItem('currentUserId', data.id);
            localStorage.setItem('currentUserName', name);
            
            // 로그인 페이지로 이동
            window.location.href = '/login';
        } else {
            // 서버에서 오류 메시지를 보냈을 때
            alert("오류 발생: " + JSON.stringify(data));
        }
    } catch (error) {
        // fetch 자체가 실패할 경우 (백엔드 꺼짐, 네트워크 문제 등)
        alert("서버 연결 실패! 백엔드가 켜져 있나요?");
        console.error(error);
    }
}
