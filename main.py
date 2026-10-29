import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Ocean Angler (Testing Build)",
    page_icon="🎣",
    layout="wide"
)

# 스크롤 및 브라우저 리사이징이 허용되도록 CSS 제한 해제
st.markdown("""
    <style>
        /* 기본 스크롤바 및 리사이징 허용 */
        html, body {
            overflow: auto !important;
            background-color: #0f172a !important;
        }
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
        overflow: auto; /* 스크롤 활성화 */
        background-color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        user-select: none;
    }
    
    #gameContainer {
        position: relative;
        width: 100%;
        height: 800px; /* 기본 높이 지정 및 스크롤 시 확인 가능 */
        background-color: #0f172a;
        overflow: hidden;
    }
    
    canvas {
        width: 100%;
        height: 100%;
        display: block;
        image-rendering: pixelated;
    }
    
    /* UI 레이아웃 */
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
        color: #38bdf8;
    }
    #gameDesc {
        font-size: 11px;
        color: #cbd5e1;
    }

    #messageOverlay {
        position: absolute;
        top: 15%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        pointer-events: none;
        z-index: 10;
        transition: opacity 0.1s linear;
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
        z-index: 20;
    }

    #notebookBtn { left: 20px; }
    #settingsBtn { right: 20px; }

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
    .closeBtn {
        cursor: pointer;
        font-size: 20px;
        color: #94a3b8;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas"></canvas>
    
    <div id="notebookBtn" class="topBtn">📓</div>
    <div id="settingsBtn" class="topBtn">⚙️</div>

    <div id="notebookModal" class="modal">
        <div class="modalHeader">
            <span>📖 Caught Fish Log</span>
            <span id="closeNotebook" class="closeBtn">&times;</span>
        </div>
        <ul id="caughtList" style="list-style:none; padding:0;">
            <li style="color: #94a3b8; text-align:center;">아직 잡은 물고기가 없습니다.</li>
        </ul>
    </div>

    <div id="settingsModal" class="modal">
        <div class="modalHeader">
            <span>⚙️ Settings (Testing Mode)</span>
            <span id="closeSettings" class="closeBtn">&times;</span>
        </div>
        <p style="font-size:13px; color:#cbd5e1;">브라우저 창 크기 조절 및 스크롤 기능이 활성화된 테스트 모드입니다.</p>
    </div>

    <div id="messageOverlay">
        <div id="statusText">Press SPACE or ENTER to Start Fishing!</div>
        <div id="caughtInfo"></div>
    </div>

    <div id="bottomLeftUI">
        <div id="gameTitle">OCEAN ANGLER (RESIZE/SCROLL TEST)</div>
        <div id="gameDesc">[Space/Enter] 낚시 시작 | [Space] 게이지 유지 | [ESC] 취소</div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('gameContainer');

// 창 크기가 변경될 때 캔버스 크기를 동적으로 반응하도록 설정 (리사이징 활성화)
function resizeCanvas() {
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// 스크롤 방지 이벤트 제거됨 (휠/터치 동작 가능)

let gameState = 'IDLE';
let waitTimer = 0;
let castTimer = 0;
let rodAngle = 0;
let spacePressed = false;

let messageTimer = 0;
const messageOverlay = document.getElementById('messageOverlay');
const caughtFishMap = new Map();

const FISH_LIST = [
    { name: "고등어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff" },
    { name: "광어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff" },
    { name: "참돔", rarity: "rare", rarityName: "희귀", difficulty: 1.3, color: "#3b82f6" },
    { name: "방어", rarity: "legendary", rarityName: "전설", difficulty: 1.6, color: "#eab308" }
];

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.code === 'Enter') {
        if (e.code === 'Space') spacePressed = true;
        if (gameState === 'IDLE' || gameState === 'RESULT') {
            startCasting();
        }
    } else if (e.code === 'Escape') {
        if (gameState === 'WAITING' || gameState === 'CASTING') {
            gameState = 'IDLE';
            showMessage("낚시를 취소했습니다.", "");
        }
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'Space') spacePressed = false;
});

const notebookBtn = document.getElementById('notebookBtn');
const settingsBtn = document.getElementById('settingsBtn');
const notebookModal = document.getElementById('notebookModal');
const settingsModal = document.getElementById('settingsModal');
const closeNotebook = document.getElementById('closeNotebook');
const closeSettings = document.getElementById('closeSettings');

notebookBtn.addEventListener('click', () => {
    notebookModal.style.display = 'block';
    settingsModal.style.display = 'none';
});

settingsBtn.addEventListener('click', () => {
    settingsModal.style.display = 'block';
    notebookModal.style.display = 'none';
});

closeNotebook.addEventListener('click', () => notebookModal.style.display = 'none');
closeSettings.addEventListener('click', () => settingsModal.style.display = 'none');

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
        if (waitTimer <= 0) initMiniGame();
    } else if (gameState === 'FISHING') {
        if (spacePressed) barPos += 1.8;
        else barPos -= 1.4;

        if (barPos < 0) barPos = 0;
        if (barPos > 100 - barSize) barPos = 100 - barSize;

        if (Math.random() < 0.03) fishTarget = Math.random() * 80 + 10;
        fishPos += (fishTarget - fishPos) * (0.02 * currentFish.difficulty);

        let barEnd = barPos + barSize;
        if (fishPos >= barPos && fishPos <= barEnd) catchProgress += 0.4;
        else catchProgress -= 0.3;

        if (catchProgress >= 100) {
            gameState = 'RESULT';
            showMessage("🎉 낚시 성공!", `✨ [${currentFish.rarityName}] ${currentFish.name}(을)를 낚았습니다!`);
        } else if (catchProgress <= 0) {
            gameState = 'RESULT';
            showMessage("❌ 놓쳤습니다...", "다시 하려면 Space/Enter를 누르세요.");
        }
    }
}

function drawPixelHatFisherman(x, y) {
    ctx.fillStyle = '#5c3d2e';
    ctx.fillRect(x - 40, y, 80, 20);
    ctx.fillStyle = '#1e3799';
    ctx.fillRect(x - 10, y - 25, 20, 25);
    ctx.fillStyle = '#f6b93b';
    ctx.beginPath();
    ctx.moveTo(x - 24, y - 22);
    ctx.lineTo(x + 24, y - 22);
    ctx.lineTo(x, y - 45);
    ctx.closePath();
    ctx.fill();

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

    ctx.restore();

    const globalTipX = handX + 55 * Math.cos(-rodAngle) - (-45) * Math.sin(-rodAngle);
    const globalTipY = handY + 55 * Math.sin(-rodAngle) + (-45) * Math.cos(-rodAngle);

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
    ctx.fillStyle = '#0f3057';
    ctx.fillRect(0, 0, w, h * 0.45);
    ctx.fillStyle = '#00587a';
    ctx.fillRect(0, h * 0.45, w, h * 0.55);
}

function drawUI() {
    if (gameState === 'FISHING') {
        const uiWidth = Math.min(450, canvas.width * 0.7);
        const uiX = (canvas.width - uiWidth) / 2;
        const uiY = canvas.height * 0.72;
        const uiHeight = 26;

        ctx.fillStyle = '#0f172a';
        ctx.fillRect(uiX - 6, uiY - 6, uiWidth + 12, uiHeight + 12);
        ctx.fillStyle = '#334155';
        ctx.fillRect(uiX, uiY, uiWidth, uiHeight);

        let renderBarX = uiX + (barPos / 100) * uiWidth;
        let renderBarW = (barSize / 100) * uiWidth;
        ctx.fillStyle = '#22c55e';
        ctx.fillRect(renderBarX, uiY, renderBarW, uiHeight);

        let renderFishX = uiX + (fishPos / 100) * uiWidth;
        ctx.fillStyle = currentFish.color;
        ctx.beginPath();
        ctx.arc(renderFishX, uiY + uiHeight / 2, 9, 0, Math.PI * 2);
        ctx.fill();

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
    drawPixelHatFisherman(canvas.width * 0.35, canvas.height * 0.50 + Math.sin(waveOffset) * 4);
    drawUI();
    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=True)
