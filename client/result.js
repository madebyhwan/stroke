// 페이지 로드 시 결과 표시
window.addEventListener('DOMContentLoaded', () => {
    const riskLevel = localStorage.getItem('riskLevel');
    
    if (!riskLevel) {
        alert('결과 데이터가 없습니다.');
        window.location.href = 'index.html';
        return;
    }
    
    const riskDisplay = document.getElementById('riskDisplay');
    riskDisplay.textContent = riskLevel;
    riskDisplay.className = `text-4xl font-bold my-3 risk-${riskLevel}`;
});
