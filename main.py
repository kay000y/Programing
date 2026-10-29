import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="한국 바다 도트 낚시 게임",
    page_icon="🎣",
    layout="centered"
)

st.title("🎣바다 낚시")
st.caption("Enter 키 또는 Space 바를 눌러 낚시를 시작하세요! 낚시 미니게임 중에는 Space 바를 누르고 있어 게이지를 조절하세요.")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #111;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: 'Courier New', Courier, monospace;
        user-select: none;
    }
    #gameContainer {
        position: relative;
        width: 600px;
        height: 400px;
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
        border-radius: 8px;
        overflow: hidden;
    }
    canvas {
        background-color: #1b4965;
        image-rendering: pixelated;
    }
    #uiOverlay {
        position: absolute;
        top: 10px;
        left: 10px;
        color: white;
        text-shadow: 2px 2px #000;
        font-weight: bold;
        font-size: 14px;
        pointer-events: none;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="600" height="400"></canvas>
    <div id="uiOverlay">
        <div id="statusText">Press SPACE or ENTER to Fish!</div>
        <div id="caughtInfo" style="margin-top: 5px; color: #ffeaa7;"></div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 게임 상태: 'IDLE', 'WAITING', 'FISHING', 'RESULT'
let gameState = 'IDLE';
let waitTimer = 0;
let messageTimer = 0;

// 입력 처리
let spacePressed = false;

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.code === 'Enter') {
        if (e.code === 'Space') spacePressed = true;
        
        if (gameState === 'IDLE' || gameState === 'RESULT') {
            startFishing();
        }
        // 스페이스바로 페이지가 스크롤되는 것을 방지
        if (e.code === 'Space') e.preventDefault();
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'Space') {
        spacePressed = false;
    }
});

// 한국 해양 어종 데이터
const FISH_LIST = [
    { name: "고등어", difficulty: 1.2, color: "#48dbfb" },
    { name: "광어", difficulty: 1.0, color: "#c8d6e5" },
    { name: "우럭", difficulty: 1.1, color: "#8395a7" },
    { name: "참돔", difficulty: 1.8, color: "#ff9ff3" },
    { name: "감성돔", difficulty: 2.0, color: "#54a0ff" },
    { name: "방어", difficulty: 2.2, color: "#feca57" },
    { name: "오징어", difficulty: 1.5, color: "#ff6b6b" },
    { name: "볼락", difficulty: 0.9, color: "#ff9f43" }
];

let currentFish = null;
let fishPos = 50;       // 0 ~ 100 (오른쪽 방향)
let fishTarget = 50;
let barPos = 10;        // 0 ~ 100
let barSize = 25;       // 게이지 바 크기
let catchProgress = 30; // 0 ~ 100 (100이면 잡음, 0이면 놓침)
let lastCaughtFish = "";

function startFishing() {
    gameState = 'WAITING';
    waitTimer = 300; // 약 5초 (60fps 기준 300프레임)
    document.getElementById('statusText').innerText = "낚싯대를 던졌습니다... 기다리는 중...";
    document.getElementById('caughtInfo').innerText = "";
}

function initMiniGame() {
    gameState = 'FISHING';
    currentFish = FISH_LIST[Math.floor(Math.random() * FISH_LIST.length)];
    fishPos = 20;
    fishTarget = Math.random() * 80 + 10;
    barPos = 10;
    catchProgress = 30;
    document.getElementById('statusText').innerText = `신호가 왔다! [${currentFish.name}] (Space 연타/눌러서 게이지 유지!)`;
}

// 배경파도 및 배 애니메이션 변수
let waveOffset = 0;
let boatYOffset = 0;

function update() {
    waveOffset += 0.05;
    boatYOffset = Math.sin(waveOffset) * 3;

    if (gameState === 'WAITING') {
        waitTimer--;
        if (waitTimer <= 0) {
            initMiniGame();
        }
    } else if (gameState === 'FISHING') {
        // 게이지 바 이동 (Space 누르면 오른쪽, 떼면 왼쪽)
        if (spacePressed) {
            barPos += 1.8;
        } else {
            barPos -= 1.4;
        }

        // 바 경계 제한
        if (barPos < 0) barPos = 0;
        if (barPos > 100 - barSize) barPos = 100 - barSize;

        // 물고기 랜덤 이동 (스타듀밸리 방식)
        if (Math.random() < 0.03) {
            fishTarget = Math.random() * 80 + 10;
        }
        fishPos += (fishTarget - fishPos) * (0.02 * currentFish.difficulty);

        // 게이지 바 안에 물고기가 들어왔는지 확인
        let barEnd = barPos + barSize;
        if (fishPos >= barPos && fishPos <= barEnd) {
            catchProgress += 0.4;
        } else {
            catchProgress -= 0.3;
        }

        // 범위 제한 및 승패 판정
        if (catchProgress >= 100) {
            gameState = 'RESULT';
            lastCaughtFish = currentFish.name;
            document.getElementById('statusText').innerText = "🎉 낚시 성공! 다시 하려면 Space/Enter 누르세요.";
            document.getElementById('caughtInfo').innerText = `✨ [${lastCaughtFish}] (을)를 낚았습니다!`;
        } else if (catchProgress <= 0) {
            gameState = 'RESULT';
            document.getElementById('statusText').innerText = "❌ 놓쳤습니다... 다시 하려면 Space/Enter 누르세요.";
            document.getElementById('caughtInfo').innerText = "";
        }
    }
}

function drawPixelHatFisherman(x, y) {
    // 삿갓/모자로 얼굴을 가린 어부 도트 (Pixel Art)
    // 배 내부
    ctx.fillStyle = '#5c3d2e';
    ctx.fillRect(x - 30, y, 60, 15);
    ctx.fillStyle = '#3d2314';
    ctx.fillRect(x - 25, y + 15, 50, 8);

    // 어부 몸통 (파란 우의)
    ctx.fillStyle = '#1e3799';
    ctx.fillRect(x - 8, y - 20, 16, 20);

    // 삿갓 (얼굴을 완전히 가림)
    ctx.fillStyle = '#f6b93b';
    ctx.beginPath();
    ctx.moveTo(x - 18, y - 18);
    ctx.lineTo(x + 18, y - 18);
    ctx.lineTo(x, y - 35);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(x - 18, y - 18, 36, 3); // 삿갓 챙 테두리

    // 낚싯대
    ctx.strokeStyle = '#d2dae2';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x + 5, y - 10);
    ctx.lineTo(x + 45, y - 45);
    ctx.stroke();

    // 낚싯줄
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x + 45, y - 45);
    
    if (gameState === 'WAITING' || gameState === 'FISHING') {
        ctx.lineTo(x + 120, y + 20); // 바다 속으로 내려간 줄
    } else {
        ctx.lineTo(x + 45, y + 10);
    }
    ctx.stroke();
}

function drawBackground() {
    // 바다 배경 (지평선 구분을 위한 그라데이션 표현)
    ctx.fillStyle = '#0f3057';
    ctx.fillRect(0, 0, canvas.width, 150);
    ctx.fillStyle = '#00587a';
    ctx.fillRect(0, 150, canvas.width, 250);

    // 파도 효과
    ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
    for (let i = 0; i < canvas.width; i += 40) {
        let waveY = 160 + Math.sin(waveOffset + i) * 5;
        ctx.fillRect(i, waveY, 20, 3);
        let waveY2 = 280 + Math.cos(waveOffset + i) * 8;
        ctx.fillRect(i + 15, waveY2, 25, 3);
    }
}

function drawUI() {
    if (gameState === 'FISHING') {
        // 스타듀밸리 스타일 UI 바 (가로형)
        const uiX = 150;
        const uiY = 320;
        const uiWidth = 300;
        const uiHeight = 24;

        // 베이스 트랙 배경
        ctx.fillStyle = '#222';
        ctx.fillRect(uiX - 4, uiY - 4, uiWidth + 8, uiHeight + 8);
        ctx.fillStyle = '#444';
        ctx.fillRect(uiX, uiY, uiWidth, uiHeight);

        // 녹색 녹색 게이지 바 (플레이어 컨트롤)
        let renderBarX = uiX + (barPos / 100) * uiWidth;
        let renderBarW = (barSize / 100) * uiWidth;
        ctx.fillStyle = '#2ecc71';
        ctx.fillRect(renderBarX, uiY, renderBarW, uiHeight);
        ctx.strokeStyle = '#27ae60';
        ctx.strokeRect(renderBarX, uiY, renderBarW, uiHeight);

        // 물고기 표시
        let renderFishX = uiX + (fishPos / 100) * uiWidth;
        ctx.fillStyle = currentFish.color;
        ctx.beginPath();
        ctx.arc(renderFishX, uiY + uiHeight / 2, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.stroke();

        // 잡기 진행도 바 (하단 진행 상태)
        ctx.fillStyle = '#555';
        ctx.fillRect(uiX, uiY + uiHeight + 8, uiWidth, 6);
        ctx.fillStyle = '#f1c40f';
        ctx.fillRect(uiX, uiY + uiHeight + 8, (catchProgress / 100) * uiWidth, 6);
    }
}

function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    update();
    drawBackground();
    drawPixelHatFisherman(200, 230 + boatYOffset);
    drawUI();

    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=430)
