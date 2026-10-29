import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Ocean Angler",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit 여백 및 전체 검은색 배경 설정
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], .main, .block-container {
            padding: 0 !important;
            margin: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
            background-color: #000000 !important;
        }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stHeader"] {display: none;}
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
        margin: 0;
        padding: 0;
    }
    html, body {
        width: 100%;
        height: 100%;
        overflow: hidden;
        background-color: #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        user-select: none;
        touch-action: none;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* 캔버스 감싸는 컨테이너 */
    #gameContainer {
        position: relative;
        background-color: #0f172a;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.9);
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    canvas {
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
        font-size: 11px;
        color: #cbd5e1;
        max-width: 380px;
        line-height: 1.4;
    }

    /* 알림 메시지 (상대적 위치 지정) */
    #messageOverlay {
        position: absolute;
        top: 15%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        pointer-events: none;
        z-index: 10;
        transition: opacity 0.1s linear;
        opacity: 1;
        width: 90%;
    }
    #statusText {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
    }
    #caughtInfo {
        font-size: 20px;
        font-weight: 800;
        color: #fde047;
        margin-top: 6px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
    }

    /* 상단 공통 버튼 스타일 */
    .topBtn {
        position: absolute;
        top: 20px;
        width: 48px;
        height: 52px;
        background-color: #854d0e;
        border: 2px solid #fef08a;
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 26px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        z-index: 20;
        transition: transform 0.1s, background-color 0.1s;
    }
    .topBtn:hover {
        transform: scale(1.08);
        background-color: #a16207;
    }

    #notebookBtn { left: 20px; }
    #settingsBtn { right: 20px; }

    /* 모달 공통 스타일 */
    .modal {
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 360px;
        background-color: #1e293b;
        border: 3px solid #38bdf8;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.8);
        padding: 20px;
        color: white;
        z-index: 30;
    }
    .modalHeader {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .modalTitle {
        font-size: 18px;
        font-weight: bold;
        color: #38bdf8;
    }
    .closeBtn {
        cursor: pointer;
        font-size: 20px;
        font-weight: bold;
        color: #94a3b8;
    }
    .closeBtn:hover {
        color: #ffffff;
    }

    /* 도감 리스트 */
    #caughtList {
        list-style: none;
        padding: 0;
        margin: 0;
        max-height: 300px;
        overflow-y: auto;
    }
    #caughtList li {
        padding: 10px 14px;
        background-color: #334155;
        margin-bottom: 8px;
        border-radius: 6px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .rarityTag {
        font-size: 11px;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .rarity-common { background-color: #94a3b8; color: #0f172a; }
    .rarity-rare { background-color: #3b82f6; color: #ffffff; }
    .rarity-legendary { background-color: #eab308; color: #0f172a; }

    /* 설정 폼 */
    .settingRow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .settingRow label {
        font-size: 14px;
        color: #cbd5e1;
    }
    .settingRow select {
        background-color: #334155;
        color: white;
        border: 1px solid #475569;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 14px;
        outline: none;
        cursor: pointer;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas"></canvas>
    
    <!-- 버튼 UI -->
    <div id="notebookBtn" class="topBtn" title="Fish Logbook">📓</div>
    <div id="settingsBtn" class="topBtn" title="Settings">⚙️</div>

    <!-- 도감 팝업 -->
    <div id="notebookModal" class="modal">
        <div class="modalHeader">
            <span class="modalTitle">📖 Caught Fish Log</span>
            <span id="closeNotebook" class="closeBtn">&times;</span>
        </div>
        <ul id="caughtList">
            <li style="color: #94a3b8; justify-content: center;">아직 잡은 물고기가 없습니다.</li>
        </ul>
    </div>

    <!-- 설정 팝업 -->
    <div id="settingsModal" class="modal">
        <div class="modalHeader">
            <span class="modalTitle">⚙️ Settings</span>
            <span id="closeSettings" class="closeBtn">&times;</span>
        </div>
        <div class="settingRow">
            <label for="resolutionSelect">Screen Size:</label>
            <select id="resolutionSelect">
                <option value="1024x576">1. Small (1024x576)</option>
                <option value="1280x720">2. Normal (1280x720)</option>
                <option value="1600x900" selected>3. Medium (1600x900)</option>
                <option value="1920x1080">4. Large (1920x1080)</option>
                <option value="FULL">5. Full Window</option>
            </select>
        </div>
    </div>

    <!-- 중앙 상단 알림 메시지 -->
    <div id="messageOverlay">
        <div id="statusText">Press SPACE or ENTER to Start Fishing!</div>
        <div id="caughtInfo"></div>
    </div>

    <!-- 좌측 하단 타이틀 & 설명 -->
    <div id="bottomLeftUI">
        <div id="gameTitle">OCEAN ANGLER</div>
        <div id="gameDesc">
            [Space/Enter] 낚시 시작 | [Space] 꾹 눌러 게이지 유지 | [ESC] 대기 중 낚시 취소
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('gameContainer');
const resolutionSelect = document.getElementById('resolutionSelect');

// 해상도 조절 함수 (기본값: 3번째 1600x900)
function applyResolution(resKey) {
    if (resKey === 'FULL') {
        container.style.width = '100vw';
        container.style.height = '100vh';
    } else {
        const [w, h] = resKey.split('x').map(Number);
        // 브라우저 크기보다 커지지 않도록 비율 제한
        const maxW = window.innerWidth;
        const maxH = window.innerHeight;
        
        let targetW = w;
        let targetH = h;
        
        if (targetW > maxW || targetH > maxH) {
            const scale = Math.min(maxW / targetW, maxH / targetH);
            targetW *= scale;
            targetH *= scale;
        }

        container.style.width = targetW + 'px';
        container.style.height = targetH + 'px';
    }

    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
}

window.addEventListener('resize', () => applyResolution(resolutionSelect.value));
resolutionSelect.addEventListener('change', (e) => applyResolution(e.target.value));

// 초기 해상도 설정 적용 (3번째: 1600x900)
applyResolution('1600x900');

// 스크롤 및 터치 확대 방지
window.addEventListener('wheel', (e) => e.preventDefault(), { passive: false });
window.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });

// 게임 상태
let gameState = 'IDLE';
let waitTimer = 0;
let castTimer = 0;
let rodAngle = 0;
let spacePressed = false;

// 페이드아웃 변수
let messageTimer = 0;
const messageOverlay = document.getElementById('messageOverlay');

// 잡은 물고기 목록 Map
const caughtFishMap = new Map();

// 어종 데이터
const FISH_LIST = [
    { name: "고등어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff" },
    { name: "광어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff" },
    { name: "우럭", rarity: "common", rarityName: "일반", difficulty: 1.1, color: "#ffffff" },
    { name: "볼락", rarity: "common", rarityName: "일반", difficulty: 0.9, color: "#ffffff" },
    
    { name: "참돔", rarity: "rare", rarityName: "희귀", difficulty: 1.3, color: "#3b82f6" },
    { name: "오징어", rarity: "rare", rarityName: "희귀", difficulty: 1.2, color: "#3b82f6" },
    { name: "감성돔", rarity: "rare", rarityName: "희귀", difficulty: 1.4, color: "#3b82f6" },
    
    { name: "방어", rarity: "legendary", rarityName: "전설", difficulty: 1.6, color: "#eab308" },
    { name: "돗돔", rarity: "legendary", rarityName: "전설", difficulty: 1.8, color: "#eab308" }
];

// 키보드 이벤트
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.code === 'Enter') {
        if (e.code === 'Space') spacePressed = true;
        
        if (gameState === 'IDLE' || gameState === 'RESULT') {
            startCasting();
        }
        if (e.code === 'Space') e.preventDefault();
    } else if (e.code === 'Escape') {
        if (gameState === 'WAITING' || gameState === 'CASTING') {
            gameState = 'IDLE';
            showMessage("낚시를 취소했습니다.", "");
        }
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'Space') {
        spacePressed = false;
    }
});

// UI 모달 핸들러
const notebookBtn = document.getElementById('notebookBtn');
const settingsBtn = document.getElementById('settingsBtn');
const notebookModal = document.getElementById('notebookModal');
const settingsModal = document.getElementById('settingsModal');
const closeNotebook = document.getElementById('closeNotebook');
const closeSettings = document.getElementById('closeSettings');

notebookBtn.addEventListener('click', () => {
    updateNotebookUI();
    notebookModal.style.display = 'block';
    settingsModal.style.display = 'none';
});

settingsBtn.addEventListener('click', () => {
    settingsModal.style.display = 'block';
    notebookModal.style.display = 'none';
});

closeNotebook.addEventListener('click', () => notebookModal.style.display = 'none');
closeSettings.addEventListener('click', () => settingsModal.style.display = 'none');

function updateNotebookUI() {
    const listEl = document.getElementById('caughtList');
    listEl.innerHTML = '';
    
    if (caughtFishMap.size === 0) {
        listEl.innerHTML = '<li style="color: #94a3b8; justify-content: center;">아직 잡은 물고기가 없습니다.</li>';
        return;
    }

    caughtFishMap.forEach((data, fishName) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>🐟 ${fishName}</span>
            <span class="rarityTag rarity-${data.rarity}">${data.rarityName}</span>
        `;
        listEl.appendChild(li);
    });
}

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
    messageTimer = 0;
}

function startCasting() {
    gameState = 'CASTING';
    castTimer = 0;
    rodAngle = 0;
    showMessage("낚싯대를 던집니다!", "");
}

function startWaiting() {
    gameState = 'WAITING';
    waitTimer = 300;
    showMessage("기다리는 중... (ESC로 취소 가능)", "");
}

function initMiniGame() {
    gameState = 'FISHING';
    currentFish = FISH_LIST[Math.floor(Math.random() * FISH_LIST.length)];
    fishPos = 20;
    fishTarget = Math.random() * 80 + 10;
    barPos = 10;
    catchProgress = 30;
    showMessage(`신호가 왔다! [${currentFish.rarityName}] 등급 물고기!`, "Space 바를 눌러 게이지를 맞추세요!");
}

let waveOffset = 0;

function update() {
    waveOffset += 0.04;

    // 메시지 페이드아웃 (3초~7초)
    messageTimer++;
    if (messageTimer > 180) {
        if (messageTimer >= 420) {
            messageOverlay.style.opacity = '0';
        } else {
            let alpha = 1 - ((messageTimer - 180) / (420 - 180));
            messageOverlay.style.opacity = alpha.toString();
        }
    }

    if (gameState === 'CASTING') {
        castTimer += 0.08;
        rodAngle = Math.sin(castTimer) * (Math.PI / 2);
        
        if (castTimer >= Math.PI) {
            rodAngle = 0;
            startWaiting();
        }
    } else if (gameState === 'WAITING') {
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
            caughtFishMap.set(currentFish.name, currentFish);
            showMessage("🎉 낚시 성공!", `✨ [${currentFish.rarityName}] ${currentFish.name}(을)를 낚았습니다!`);
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

    // 삿갓
    ctx.fillStyle = '#f6b93b';
    ctx.beginPath();
    ctx.moveTo(x - 24, y - 22);
    ctx.lineTo(x + 24, y - 22);
    ctx.lineTo(x, y - 45);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(x - 24, y - 22, 48, 4);

    // 낚싯대 회전
    const handX = x + 5;
    const handY = y - 15;

    ctx.save();
    ctx.translate(handX, handY);
    ctx.rotate(-rodAngle);

    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(55, -45);
    ctx.stroke();

    const tipX = 55;
    const tipY = -45;

    ctx.restore();

    const globalTipX = handX + tipX * Math.cos(-rodAngle) - tipY * Math.sin(-rodAngle);
    const globalTipY = handY + tipX * Math.sin(-rodAngle) + tipY * Math.cos(-rodAngle);

    // 낚싯줄
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(globalTipX, globalTipY);
    
    if (gameState === 'WAITING' || gameState === 'FISHING') {
        ctx.lineTo(x + 180, y + 40);
    } else {
        ctx.lineTo(globalTipX, globalTipY + 30);
    }
    ctx.stroke();
}

function drawBackground() {
    const w = canvas.width;
    const h = canvas.height;

    // 수평선 비율 고정 (상단 45% 하늘/바다 경계)
    ctx.fillStyle = '#0f3057';
    ctx.fillRect(0, 0, w, h * 0.45);
    ctx.fillStyle = '#00587a';
    ctx.fillRect(0, h * 0.45, w, h * 0.55);

    // 파도
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
    for (let i = 0; i < w; i += 60) {
        let waveY = h * 0.47 + Math.sin(waveOffset + i) * 6;
        ctx.fillRect(i, waveY, 35, 4);
        let waveY2 = h * 0.68 + Math.cos(waveOffset + i) * 10;
        ctx.fillRect(i + 20, waveY2, 45, 4);
    }
}

function drawUI() {
    if (gameState === 'FISHING') {
        // 화면 해상도에 동적으로 수응하는 하단 UI 위치 설정
        const uiWidth = Math.min(450, canvas.width * 0.7);
        const uiX = (canvas.width - uiWidth) / 2;
        const uiY = canvas.height * 0.72; // 화면 하단에서 파묻히지 않는 최적 위치
        const uiHeight = 26;

        // 베이스 트랙
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(uiX - 6, uiY - 6, uiWidth + 12, uiHeight + 12);
        ctx.fillStyle = '#334155';
        ctx.fillRect(uiX, uiY, uiWidth, uiHeight);

        // 게이지 바 (녹색)
        let renderBarX = uiX + (barPos / 100) * uiWidth;
        let renderBarW = (barSize / 100) * uiWidth;
        ctx.fillStyle = '#22c55e';
        ctx.fillRect(renderBarX, uiY, renderBarW, uiHeight);
        ctx.strokeStyle = '#15803d';
        ctx.lineWidth = 2;
        ctx.strokeRect(renderBarX, uiY, renderBarW, uiHeight);

        // 물고기 아이콘 (등급별 색상)
        let renderFishX = uiX + (fishPos / 100) * uiWidth;
        ctx.fillStyle = currentFish.color;
        ctx.beginPath();
        ctx.arc(renderFishX, uiY + uiHeight / 2, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 2;
        ctx.stroke();

        // 잡기 진행도 바
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(uiX, uiY + uiHeight + 8, uiWidth, 7);
        ctx.fillStyle = '#eab308';
        ctx.fillRect(uiX, uiY + uiHeight + 8, (catchProgress / 100) * uiWidth, 7);
    }
}

function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    update();
    drawBackground();
    
    // 어부 위치 동적 계산 (화면 중앙 상단 바다 위)
    const boatX = canvas.width * 0.35;
    const boatY = canvas.height * 0.50 + Math.sin(waveOffset) * 4;
    drawPixelHatFisherman(boatX, boatY);
    
    drawUI();

    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=1000, scrolling=False)
