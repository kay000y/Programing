import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Ocean Angler: Korean Seas",
    page_icon="🎣",
    layout="wide"
)

# Streamlit 기본 여백 제거 스타일링
st.markdown("""
    <style>
        .block-container {
            padding: 0rem !important;
        }
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {
        box-sizing: border-box;
    }
    body, html {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background-color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        user-select: none;
    }
    #gameContainer {
        position: relative;
        width: 100vw;
        height: 100vh;
    }
    canvas {
        width: 100%;
        height: 100%;
        display: block;
        image-rendering: pixelated;
    }
    
    /* 좌측 하단 타이틀 & 설명 UI */
    #bottomLeftUI {
        position: absolute;
        bottom: 20px;
        left: 20px;
        color: #ffffff;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
        pointer-events: none;
        z-index: 10;
    }
    #gameTitle {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #38bdf8;
        margin-bottom: 4px;
    }
    #gameDesc {
        font-size: 12px;
        color: #cbd5e1;
        max-width: 380px;
        line-height: 1.4;
    }

    /* 알림 메시지 (페이드아웃) */
    #messageOverlay {
        position: absolute;
        top: 25%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        pointer-events: none;
        z-index: 10;
        transition: opacity 0.1s linear;
        opacity: 1;
    }
    #statusText {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
    }
    #caughtInfo {
        font-size: 22px;
        font-weight: 800;
        color: #fde047;
        margin-top: 6px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
    }

    /* 좌측 상단 노트 아이콘 */
    #notebookBtn {
        position: absolute;
        top: 20px;
        left: 20px;
        width: 44px;
        height: 48px;
        background-color: #854d0e;
        border: 2px solid #fef08a;
        border-radius: 6px;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        z-index: 20;
        transition: transform 0.1s;
    }
    #notebookBtn:hover {
        transform: scale(1.08);
        background-color: #a16207;
    }

    /* 중앙 도감 팝업 모달 */
    #notebookModal {
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 360px;
        max-height: 480px;
        background-color: #1e293b;
        border: 3px solid #38bdf8;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7);
        padding: 20px;
        color: white;
        z-index: 30;
    }
    #notebookHeader {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    #notebookTitle {
        font-size: 18px;
        font-weight: bold;
        color: #38bdf8;
    }
    #closeBtn {
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
        color: #94a3b8;
    }
    #closeBtn:hover {
        color: #ffffff;
    }
    #caughtList {
        list-style: none;
        padding: 0;
        margin: 0;
        max-height: 360px;
        overflow-y: auto;
    }
    #caughtList li {
        padding: 8px 12px;
        background-color: #334155;
        margin-bottom: 8px;
        border-radius: 6px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas"></canvas>
    
    <!-- 좌측 상단 노트 버튼 -->
    <div id="notebookBtn" title="Fish Logbook">📓</div>

    <!-- 중앙 도감 팝업 -->
    <div id="notebookModal">
        <div id="notebookHeader">
            <span id="notebookTitle">📖 Caught Fish Log</span>
            <span id="closeBtn">&times;</span>
        </div>
        <ul id="caughtList">
            <li style="color: #94a3b8; justify-content: center;">아직 잡은 물고기가 없습니다.</li>
        </ul>
    </div>

    <!-- 중앙 상단 알림 메시지 (페이드아웃 대상) -->
    <div id="messageOverlay">
        <div id="statusText">Press SPACE or ENTER to Start Fishing!</div>
        <div id="caughtInfo"></div>
    </div>

    <!-- 좌측 하단 타이틀 & 설명 -->
    <div id="bottomLeftUI">
        <div id="gameTitle">OCEAN ANGLER: KOREAN SEAS</div>
        <div id="gameDesc">
            [Space/Enter] 낚시 시작 | [Space] 꾹 눌러 게이지 오른쪽 이동 / 떼면 왼쪽 이동
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// 게임 상태: 'IDLE', 'WAITING', 'FISHING', 'RESULT'
let gameState = 'IDLE';
let waitTimer = 0;
let spacePressed = false;

// 페이드아웃 관련 변수
let messageTimer = 0; // 프레임 단위 (60fps)
const messageOverlay = document.getElementById('messageOverlay');

// 잡은 물고기 기록 목록 (중복 제거용 Set)
const caughtFishSet = new Set();

// 입력 처리
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.code === 'Enter') {
        if (e.code === 'Space') spacePressed = true;
        
        if (gameState === 'IDLE' || gameState === 'RESULT') {
            startFishing();
        }
        if (e.code === 'Space') e.preventDefault();
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'Space') {
        spacePressed = false;
    }
});

// 노트 팝업 열기/닫기
const notebookBtn = document.getElementById('notebookBtn');
const notebookModal = document.getElementById('notebookModal');
const closeBtn = document.getElementById('closeBtn');

notebookBtn.addEventListener('click', () => {
    updateNotebookUI();
    notebookModal.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    notebookModal.style.display = 'none';
});

function updateNotebookUI() {
    const listEl = document.getElementById('caughtList');
    listEl.innerHTML = '';
    
    if (caughtFishSet.size === 0) {
        listEl.innerHTML = '<li style="color: #94a3b8; justify-content: center;">아직 잡은 물고기가 없습니다.</li>';
        return;
    }

    caughtFishSet.forEach(fishName => {
        const li = document.createElement('li');
        li.innerHTML = `<span>🐟 ${fishName}</span><span style="color:#38bdf8; font-size:12px;">Caught</span>`;
        listEl.appendChild(li);
    });
}

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
let fishPos = 50;
let fishTarget = 50;
let barPos = 10;
let barSize = 25;
let catchProgress = 30;

function showMessage(status, caught = "") {
    document.getElementById('statusText').innerText = status;
    document.getElementById('caughtInfo').innerText = caught;
    messageOverlay.style.opacity = '1';
    messageTimer = 0; // 타이머 리셋
}

function startFishing() {
    gameState = 'WAITING';
    waitTimer = 300; // 약 5초
    showMessage("낚싯대를 던졌습니다... 기다리는 중...", "");
}

function initMiniGame() {
    gameState = 'FISHING';
    currentFish = FISH_LIST[Math.floor(Math.random() * FISH_LIST.length)];
    fishPos = 20;
    fishTarget = Math.random() * 80 + 10;
    barPos = 10;
    catchProgress = 30;
    showMessage(`신호가 왔다! [${currentFish.name}]`, "Space 바를 연타하거나 눌러 게이지를 조절하세요!");
}

let waveOffset = 0;

function update() {
    waveOffset += 0.04;

    // 페이드아웃 로직 (3초 후 투명해지기 시작 ~ 7초 후 완전 소멸)
    // 60fps 기준: 3초 = 180프레임, 7초 = 420프레임
    messageTimer++;
    if (messageTimer > 180) {
        if (messageTimer >= 420) {
            messageOverlay.style.opacity = '0';
        } else {
            let alpha = 1 - ((messageTimer - 180) / (420 - 180));
            messageOverlay.style.opacity = alpha.toString();
        }
    }

    if (gameState === 'WAITING') {
        waitTimer--;
        if (waitTimer <= 0) {
            initMiniGame();
        }
    } else if (gameState === 'FISHING') {
        if (spacePressed) {
            barPos += 1.8;
        } else {
            barPos -= 1.4;
        }

        if (barPos < 0) barPos = 0;
        if (barPos > 100 - barSize) barPos = 100 - barSize;

        if (Math.random() < 0.03) {
            fishTarget = Math.random() * 80 + 10;
        }
        fishPos += (fishTarget - fishPos) * (0.02 * currentFish.difficulty);

        let barEnd = barPos + barSize;
        if (fishPos >= barPos && fishPos <= barEnd) {
            catchProgress += 0.4;
        } else {
            catchProgress -= 0.3;
        }

        if (catchProgress >= 100) {
            gameState = 'RESULT';
            caughtFishSet.add(currentFish.name);
            showMessage("🎉 낚시 성공!", `✨ [${currentFish.name}] (을)를 낚았습니다!`);
        } else if (catchProgress <= 0) {
            gameState = 'RESULT';
            showMessage("❌ 놓쳤습니다...", "다시 하려면 Space/Enter를 누르세요.");
        }
    }
}

function drawPixelHatFisherman(x, y) {
    // 배
    ctx.fillStyle = '#5c3d2e';
    ctx.fillRect(x - 40, y, 80, 20);
    ctx.fillStyle = '#3d2314';
    ctx.fillRect(x - 30, y + 20, 60, 10);

    // 어부 몸통
    ctx.fillStyle = '#1e3799';
    ctx.fillRect(x - 10, y - 25, 20, 25);

    // 삿갓 (얼굴 전체 가림)
    ctx.fillStyle = '#f6b93b';
    ctx.beginPath();
    ctx.moveTo(x - 24, y - 22);
    ctx.lineTo(x + 24, y - 22);
    ctx.lineTo(x, y - 45);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(x - 24, y - 22, 48, 4);

    // 낚싯대
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(x + 5, y - 15);
    ctx.lineTo(x + 60, y - 60);
    ctx.stroke();

    // 낚싯줄
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(x + 60, y - 60);
    
    if (gameState === 'WAITING' || gameState === 'FISHING') {
        ctx.lineTo(x + 180, y + 40);
    } else {
        ctx.lineTo(x + 60, y + 20);
    }
    ctx.stroke();
}

function drawBackground() {
    const w = canvas.width;
    const h = canvas.height;

    // 바다 배경
    ctx.fillStyle = '#0f3057';
    ctx.fillRect(0, 0, w, h * 0.4);
    ctx.fillStyle = '#00587a';
    ctx.fillRect(0, h * 0.4, w, h * 0.6);

    // 파도
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
    for (let i = 0; i < w; i += 60) {
        let waveY = h * 0.42 + Math.sin(waveOffset + i) * 6;
        ctx.fillRect(i, waveY, 35, 4);
        let waveY2 = h * 0.7 + Math.cos(waveOffset + i) * 10;
        ctx.fillRect(i + 20, waveY2, 45, 4);
    }
}

function drawUI() {
    if (gameState === 'FISHING') {
        const uiWidth = Math.min(400, canvas.width * 0.6);
        const uiX = (canvas.width - uiWidth) / 2;
        const uiY = canvas.height * 0.75;
        const uiHeight = 28;

        // 베이스 트랙
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(uiX - 6, uiY - 6, uiWidth + 12, uiHeight + 12);
        ctx.fillStyle = '#334155';
        ctx.fillRect(uiX, uiY, uiWidth, uiHeight);

        // 게이지 바
        let renderBarX = uiX + (barPos / 100) * uiWidth;
        let renderBarW = (barSize / 100) * uiWidth;
        ctx.fillStyle = '#22c55e';
        ctx.fillRect(renderBarX, uiY, renderBarW, uiHeight);
        ctx.strokeStyle = '#15803d';
        ctx.lineWidth = 2;
        ctx.strokeRect(renderBarX, uiY, renderBarW, uiHeight);

        // 물고기 아이콘
        let renderFishX = uiX + (fishPos / 100) * uiWidth;
        ctx.fillStyle = currentFish.color;
        ctx.beginPath();
        ctx.arc(renderFishX, uiY + uiHeight / 2, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        // 잡기 진행도 바
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(uiX, uiY + uiHeight + 10, uiWidth, 8);
        ctx.fillStyle = '#eab308';
        ctx.fillRect(uiX, uiY + uiHeight + 10, (catchProgress / 100) * uiWidth, 8);
    }
}

function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    update();
    drawBackground();
    
    // 화면 중앙 부근에 배와 어부 배치
    const boatX = canvas.width * 0.35;
    const boatY = canvas.height * 0.52 + Math.sin(waveOffset) * 5;
    drawPixelHatFisherman(boatX, boatY);
    
    drawUI();

    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=800, scrolling=False)
