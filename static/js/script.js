// Flash 메시지 3초 뒤 자동 삭제
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = 0;
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });

    // Lucide 아이콘 초기화
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// 뒤로가기 버튼 기능
function goBack() {
    window.history.back();
}

// API 호출 헬퍼 함수
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        
        // 204 No Content는 정상 응답으로 처리
        if (response.status === 204) {
            return null;
        }
        
        if (!response.ok) {
            // 에러 응답 처리
            let errorMessage = '요청 실패';
            try {
                const error = await response.json();
                errorMessage = error.detail || errorMessage;
            } catch (e) {
                // JSON 파싱 실패 시 상태 텍스트 사용
                errorMessage = response.statusText || errorMessage;
            }
            throw new Error(errorMessage);
        }
        
        // 정상 응답 JSON 파싱 (body가 없으면 null 반환)
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        return null;
    } catch (error) {
        console.error('API 호출 오류:', error);
        throw error;
    }
}

// 로딩 스피너 표시/숨김
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner mx-auto"></div>';
    }
}

function hideLoading(elementId, content = '') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = content;
    }
}

// 폼 유효성 검사
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red-500');
        } else {
            input.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}

// 알림 메시지 표시
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg alert-dismissible ${
        type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
    }`;
    alertDiv.innerHTML = `
        <div class="flex items-center gap-2">
            <i data-lucide="${type === 'success' ? 'check-circle' : 'alert-circle'}" class="w-5 h-5"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(alertDiv);
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    setTimeout(() => {
        alertDiv.style.transition = "opacity 0.5s ease";
        alertDiv.style.opacity = 0;
        setTimeout(() => alertDiv.remove(), 500);
    }, 3000);
}

// 날짜 포맷팅
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 로컬 스토리지 헬퍼
const storage = {
    set: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },
    get: (key) => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    },
    remove: (key) => {
        localStorage.removeItem(key);
    },
    clear: () => {
        localStorage.clear();
    }
};
