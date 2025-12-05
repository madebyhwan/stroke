const BASE_URL = "http://localhost:8000";

// 각 지표별 데이터 저장소
const chartData = {
    '혈압': {
        labels: [],
        data: [],
        color: '#0d9488',
        label: '수축기 혈압 (mmHg)'
    },
    '혈당': {
        labels: [],
        data: [],
        color: '#f59e0b',
        label: '혈당 (mg/dL)'
    },
    'BMI': {
        labels: [],
        data: [],
        color: '#8b5cf6',
        label: 'BMI (kg/m²)'
    },
    '위험도': {
        labels: [],
        data: [],
        color: '#ef4444',
        label: '위험도 점수'
    }
};

let currentChart = null;
let currentType = '혈압';

// 페이지 로드 시 초기화
window.addEventListener('DOMContentLoaded', async () => {
    const userId = localStorage.getItem('currentUserId');
    const userName = localStorage.getItem('currentUserName');
    
    // 로그인 시, 사이트 입장 가능
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
    
    // 건강 데이터 로드
    await loadHealthData(userId);
});

// 서버에서 건강 데이터 불러오기
async function loadHealthData(userId) {
    try {
        const response = await fetch(`${BASE_URL}/health/history/${userId}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error('데이터를 불러올 수 없습니다.');
        }

        const data = await response.json();
        
        // 로딩 숨기기
        document.getElementById('loadingSpinner').classList.add('hidden');
        
        if (!data || data.length === 0) {
            // 데이터가 없으면 메시지 표시
            document.getElementById('noDataMessage').classList.remove('hidden');
            lucide.createIcons();
        } else {
            // 데이터가 있으면 메인 컨텐츠 표시
            document.getElementById('mainContent').classList.remove('hidden');
            
            // 차트 데이터 업데이트
            updateChartData(data);
            
            // 최신 값으로 카드 업데이트
            updateCurrentValues(data[data.length - 1]);
            
            // 초기 차트 표시
            showChart('혈압');
        }
        
    } catch (error) {
        console.error('건강 데이터 로드 오류:', error);
        document.getElementById('loadingSpinner').classList.add('hidden');
        document.getElementById('noDataMessage').classList.remove('hidden');
        lucide.createIcons();
    }
}

// 서버 데이터를 차트 형식으로 변환
function updateChartData(healthData) {
    // 최근 10개 데이터만 사용 (너무 많으면 차트가 복잡해짐)
    const recentData = healthData.slice(-10);
    
    // 날짜 레이블 생성
    const labels = recentData.map(item => {
        const date = new Date(item.created_at);
        return `${date.getMonth() + 1}.${date.getDate()}`;
    });
    
    // 혈압 데이터 (수축기)
    chartData['혈압'].labels = labels;
    chartData['혈압'].data = recentData.map(item => item.systolic_bp);
    
    // 혈당 데이터
    chartData['혈당'].labels = labels;
    chartData['혈당'].data = recentData.map(item => item.glucose_level);
    
    // BMI 데이터 계산
    chartData['BMI'].labels = labels;
    chartData['BMI'].data = recentData.map(item => {
        const heightM = item.height_cm / 100;
        const bmi = item.weight_kg / (heightM * heightM);
        return parseFloat(bmi.toFixed(1));
    });
    
    // 위험도 데이터
    chartData['위험도'].labels = labels;
    chartData['위험도'].data = recentData.map(item => {
        // risk_score가 있으면 사용, 없으면 0
        return item.risk_score || 0;
    });
}

// 현재 값 카드 업데이트
function updateCurrentValues(latestData) {
    // 혈압
    const bpValue = `${latestData.systolic_bp}/${latestData.diastolic_bp}`;
    document.getElementById('value-혈압').textContent = bpValue;
    
    // 혈당
    document.getElementById('value-혈당').textContent = latestData.glucose_level;
    
    // BMI 계산
    const heightM = latestData.height_cm / 100;
    const bmi = (latestData.weight_kg / (heightM * heightM)).toFixed(1);
    document.getElementById('value-BMI').textContent = bmi;
    
    // 위험도
    const riskScore = latestData.risk_score || 0;
    const riskElement = document.getElementById('value-위험도');
    riskElement.textContent = riskScore;
    
    // 위험도에 따라 색상 변경
    riskElement.classList.remove('text-red-500', 'text-yellow-500', 'text-green-500');
    if (riskScore >= 70) {
        riskElement.classList.add('text-red-500');
    } else if (riskScore >= 40) {
        riskElement.classList.add('text-yellow-500');
    } else {
        riskElement.classList.add('text-green-500');
    }
}

// Chart.js 그래프 생성
function createChart(type) {
    const ctx = document.getElementById('healthChart').getContext('2d');
    const data = chartData[type];
    
    if (currentChart) {
        currentChart.destroy();
    }

    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: data.label,
                data: data.data,
                borderColor: data.color,
                backgroundColor: data.color + '20',
                borderWidth: 3,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: data.color,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 8,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: type === '위험도',
                    grid: {
                        color: '#f3f4f6',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        color: '#6b7280'
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        color: '#6b7280'
                    }
                }
            }
        }
    });
}

// 차트 전환 함수
function showChart(type) {
    currentType = type;
    document.getElementById('chartTitle').textContent = type;
    
    // 모든 카드의 선택 상태 초기화
    document.querySelectorAll('[id^="card-"]').forEach(card => {
        card.classList.remove('border-teal-500', 'bg-teal-50');
        card.classList.add('border-gray-100', 'bg-white');
    });
    
    // 선택된 카드 강조
    const selectedCard = document.getElementById(`card-${type}`);
    selectedCard.classList.remove('border-gray-100', 'bg-white');
    selectedCard.classList.add('border-teal-500', 'bg-teal-50');
    
    createChart(type);
}

// 새로고침 함수
async function refreshHealthData() {
    const userId = localStorage.getItem('currentUserId');
    if (userId) {
        // 로딩 표시
        document.getElementById('mainContent').classList.add('hidden');
        document.getElementById('loadingSpinner').classList.remove('hidden');
        
        // 데이터 다시 로드
        await loadHealthData(userId);
        
        // 아이콘 다시 초기화
        lucide.createIcons();
    }
}