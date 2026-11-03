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
        max-width: 420px;
        line-height: 1.4;
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

    /* 버튼 공통 스타일 */
    .topBtn {
        position: absolute;
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

    #notebookBtn { top: 20px; left: 20px; }
    #shopBtn { top: 82px; left: 20px; } /* 노트 바로 아래 */
    #settingsBtn { top: 20px; right: 20px; }

    /* 돈 표시 직사각형 UI */
    #moneyBar {
        position: absolute;
        top: 20px;
        left: 78px;
        height: 52px;
        min-width: 150px;
        background-color: #1e293b;
        border: 2px solid #eab308;
        border-radius: 8px;
        display: flex;
        align-items: center;
        padding: 0 14px;
        color: #fde047;
        font-weight: 800;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        z-index: 20;
    }

    .modal {
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 420px;
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
        margin-bottom: 12px;
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

    #rarityRateBox {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 12px;
        font-size: 12px;
        display: flex;
        justify-content: space-around;
        text-align: center;
    }
    .rateItem {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .itemList {
        list-style: none;
        padding: 0;
        margin: 0;
        max-height: 250px;
        overflow-y: auto;
    }
    .itemList li {
        padding: 8px 12px;
        background-color: #334155;
        margin-bottom: 8px;
        border-radius: 6px;
        font-size: 13px;
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

    /* 상점 탭 & 버튼 스타일 */
    .shopSectionTitle {
        font-size: 13px;
        font-weight: bold;
        color: #cbd5e1;
        margin: 12px 0 6px 0;
    }
    .actionBtn {
        background-color: #10b981;
        color: white;
        border: none;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.1s;
    }
    .actionBtn:hover { background-color: #059669; }
    .actionBtn:disabled { background-color: #64748b; cursor: not-allowed; }

    .sellAllBtn {
        width: 100%;
        background-color: #ef4444;
        color: white;
        border: none;
        padding: 8px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 6px;
        margin-bottom: 12px;
    }
    .sellAllBtn:hover { background-color: #dc2626; }

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
    
    <!-- 좌측 상단 버튼 및 돈 UI -->
    <div id="notebookBtn" class="topBtn" title="Fish Logbook">📓</div>
    <div id="shopBtn" class="topBtn" title="Shop">✉️</div>
    <div id="moneyBar">💰 <span id="moneyText" style="margin-left: 6px;">0</span> $</div>

    <!-- 우측 상단 설정 버튼 -->
    <div id="settingsBtn" class="topBtn" title="Settings">⚙️</div>

    <!-- 도감 팝업 -->
    <div id="notebookModal" class="modal">
        <div class="modalHeader">
            <span class="modalTitle">📖 Caught Fish Log</span>
            <span id="closeNotebook" class="closeBtn">&times;</span>
        </div>
        
        <div id="rarityRateBox">
            <div class="rateItem">
                <span class="rarityTag rarity-common">일반 (10$)</span>
                <span style="color: #cbd5e1;">45%</span>
            </div>
            <div class="rateItem">
                <span class="rarityTag rarity-rare">희귀 (50$)</span>
                <span style="color: #cbd5e1;">35%</span>
            </div>
            <div class="rateItem">
                <span class="rarityTag rarity-legendary">전설 (100$)</span>
                <span style="color: #cbd5e1;">20%</span>
            </div>
        </div>

        <ul id="caughtList" class="itemList">
            <li style="color: #94a3b8; justify-content: center;">아직 잡은 물고기가 없습니다.</li>
        </ul>
    </div>

    <!-- 상점 팝업 -->
    <div id="shopModal" class="modal">
        <div class="modalHeader">
            <span class="modalTitle">🏪 Ocean Shop</span>
            <span id="closeShop" class="closeBtn">&times;</span>
        </div>

        <!-- 물고기 판매 섹션 -->
        <div class="shopSectionTitle">🐟 Sell Fish [E: 맨 위 물고기 판매 | Shift+E: 전체 판매]</div>
        <ul id="shopFishList" class="itemList" style="max-height: 140px;">
            <li style="color: #94a3b8; justify-content: center;">보유 중인 물고기가 없습니다.</li>
        </ul>
        <button id="sellAllBtn" class="sellAllBtn">Sell All Fish (Shift + E)</button>

        <!-- 낚싯대 구매 섹션 -->
        <div class="shopSectionTitle" style="border-top: 1px solid #334155; padding-top: 10px;">🎣 Fishing Rods</div>
        <ul id="rodList" class="itemList" style="max-height: 140px;">
            <!-- JavaScript에서 생성 -->
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

    <div id="messageOverlay">
        <div id="statusText">Press SPACE or ENTER to Start Fishing!</div>
        <div id="caughtInfo"></div>
    </div>

    <div id="bottomLeftUI">
        <div id="gameTitle">OCEAN ANGLER</div>
        <div id="gameDesc">
            [Space/Enter] 낚시 시작 | [Space] 게이지 유지 | [ESC] 취소 | [E] 위 물고기 판매 | [Shift+E] 전체 판매
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('gameContainer');
const resolutionSelect = document.getElementById('resolutionSelect');

function applyResolution(resKey) {
    if (resKey === 'FULL') {
        container.style.width = '100vw';
        container.style.height = '100vh';
    } else {
        const [w, h] = resKey.split('x').map(Number);
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

applyResolution('1600x900');

window.addEventListener('wheel', (e) => e.preventDefault(), { passive: false });
window.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });

// 게임 경제 및 인벤토리 변수
let playerMoney = 0;
let inventory = []; // 잡은 물고기 목록 [{ id, name, rarity, rarityName, price }]
let nextFishId = 1;
let equippedRodId = "wood";

const RODS = [
    { id: "wood", name: "나무 낚싯대", price: 0, bought: true },
    { id: "stone", name: "돌 낚싯대", price: 100, bought: false },
    { id: "iron", name: "철 낚싯대", price: 10000, bought: false },
    { id: "gold", name: "금 낚싯대", price: 1000000, bought: false }
];

function updateMoneyUI() {
    document.getElementById('moneyText').innerText = playerMoney.toLocaleString();
}

function sellFish(index) {
    if (index >= 0 && index < inventory.length) {
        const item = inventory[index];
        playerMoney += item.price;
        inventory.splice(index, 1);
        updateMoneyUI();
        updateShopUI();
        updateNotebookUI();
    }
}

function sellTopFish() {
    if (inventory.length > 0) {
        sellFish(0);
    }
}

function sellAllFish() {
    if (inventory.length > 0) {
        let total = 0;
        inventory.forEach(item => total += item.price);
        playerMoney += total;
        inventory = [];
        updateMoneyUI();
        updateShopUI();
        updateNotebookUI();
    }
}

function buyRod(rodId) {
    const rod = RODS.find(r => r.id === rodId);
    if (rod && !rod.bought && playerMoney >= rod.price) {
        playerMoney -= rod.price;
        rod.bought = true;
        equippedRodId = rod.id;
        updateMoneyUI();
        updateShopUI();
    }
}

// 게임 상태
let gameState = 'IDLE';
let waitTimer = 0;
let castTimer = 0;
let resultCooldown = 0;
let rodAngle = 0;
let spacePressed = false;

let messageTimer = 0;
const messageOverlay = document.getElementById('messageOverlay');

const FISH_BY_RARITY = {
    common: [
        { name: "고등어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff", price: 10 },
        { name: "광어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff", price: 10 },
        { name: "우럭", rarity: "common", rarityName: "일반", difficulty: 1.1, color: "#ffffff", price: 10 },
        { name: "볼락", rarity: "common", rarityName: "일반", difficulty: 0.9, color: "#ffffff", price: 10 }
    ],
    rare: [
        { name: "참돔", rarity: "rare", rarityName: "희귀", difficulty: 1.3, color: "#3b82f6", price: 50 },
        { name: "오징어", rarity: "rare", rarityName: "희귀", difficulty: 1.2, color: "#3b82f6", price: 50 },
        { name: "감성돔", rarity: "rare", rarityName: "희귀", difficulty: 1.4, color: "#3b82f6", price: 50 }
    ],
    legendary: [
        { name: "방어", rarity: "legendary", rarityName: "전설", difficulty: 1.6, color: "#eab308", price: 100 },
        { name: "돗돔", rarity: "legendary", rarityName: "전설", difficulty: 1.8, color: "#eab308", price: 100 }
    ]
};

function getRandomFish() {
    const rand = Math.random();
    let rarity = 'common';
    
    if (rand < 0.45) {
        rarity = 'common';
    } else if (rand < 0.80) {
        rarity = 'rare';
    } else {
        rarity = 'legendary';
    }

    const pool = FISH_BY_RARITY[rarity];
    return pool[Math.floor(Math.random() * pool.length)];
}

// 키보드 입력
window.addEventListener('keydown', (e) => {
    // E 및 Shift+E 단축키 처리 (물고기 판매)
    if (e.code === 'KeyE') {
        if (e.shiftKey) {
            sellAllFish();
        } else {
            sellTopFish();
        }
        return;
    }

    if (e.code === 'Space' || e.code === 'Enter') {
        if (e.code === 'Space') spacePressed = true;
        
        if (gameState === 'IDLE' || (gameState === 'RESULT' && resultCooldown <= 0)) {
            startCasting();
        }
        if (e.code === 'Space') e.preventDefault();
    } else if (e.code === 'Escape') {
        if (gameState === 'WAITING' || gameState === 'CASTING') {
            gameState = 'IDLE';
            showMessage("Press SPACE or ENTER to Start Fishing!", "");
        }
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'Space') {
        spacePressed = false;
    }
});

// UI 모달 연결
const notebookBtn = document.getElementById('notebookBtn');
const shopBtn = document.getElementById('shopBtn');
const settingsBtn = document.getElementById('settingsBtn');

const notebookModal = document.getElementById('notebookModal');
const shopModal = document.getElementById('shopModal');
const settingsModal = document.getElementById('settingsModal');

const closeNotebook = document.getElementById('closeNotebook');
const closeShop = document.getElementById('closeShop');
const closeSettings = document.getElementById('closeSettings');
const sellAllBtn = document.getElementById('sellAllBtn');

notebookBtn.addEventListener('click', () => {
    updateNotebookUI();
    notebookModal.style.display = 'block';
    shopModal.style.display = 'none';
    settingsModal.style.display = 'none';
});

shopBtn.addEventListener('click', () => {
    updateShopUI();
    shopModal.style.display = 'block';
    notebookModal.style.display = 'none';
    settingsModal.style.display = 'none';
});

settingsBtn.addEventListener('click', () => {
    settingsModal.style.display = 'block';
    notebookModal.style.display = 'none';
    shopModal.style.display = 'none';
});

closeNotebook.addEventListener('click', () => notebookModal.style.display = 'none');
closeShop.addEventListener('click', () => shopModal.style.display = 'none');
closeSettings.addEventListener('click', () => settingsModal.style.display = 'none');
sellAllBtn.addEventListener('click', sellAllFish);

function updateNotebookUI() {
    const listEl = document.getElementById('caughtList');
    listEl.innerHTML = '';
    
    if (inventory.length === 0) {
        listEl.innerHTML = '<li style="color: #94a3b8; justify-content: center;">아직 잡은 물고기가 없습니다.</li>';
        return;
    }

    inventory.forEach((item) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>🐟 ${item.name} (${item.price}$)</span>
            <span class="rarityTag rarity-${item.rarity}">${item.rarityName}</span>
        `;
        listEl.appendChild(li);
    });
}

function updateShopUI() {
    // 1. 물고기 판매 목록
    const shopListEl = document.getElementById('shopFishList');
    shopListEl.innerHTML = '';

    if (inventory.length === 0) {
        shopListEl.innerHTML = '<li style="color: #94a3b8; justify-content: center;">보유 중인 물고기가 없습니다.</li>';
    } else {
        inventory.forEach((item, idx) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>🐟 ${item.name} (${item.price}$)</span>
                <button class="actionBtn" onclick="sellFish(${idx})">Sell (${item.price}$)</button>
            `;
            shopListEl.appendChild(li);
        });
    }

    // 2. 낚싯대 구매 목록
    const rodListEl = document.getElementById('rodList');
    rodListEl.innerHTML = '';

    RODS.forEach((rod) => {
        const li = document.createElement('li');
        let btnHtml = '';
        if (rod.bought) {
            btnHtml = `<span style="color: #22c55e; font-weight: bold; font-size: 12px;">Owned</span>`;
        } else {
            const canAfford = playerMoney >= rod.price;
            btnHtml = `<button class="actionBtn" ${canAfford ? '' : 'disabled'} onclick="buyRod('${rod.id}')">Buy (${rod.price.toLocaleString()}$)</button>`;
        }

        li.innerHTML = `
            <span>🎣 ${rod.name}</span>
            ${btnHtml}
        `;
        rodListEl.appendChild(li);
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
    currentFish = getRandomFish();
    fishPos = 20;
    fishTarget = Math.random() * 80 + 10;
    barPos = 10;
    catchProgress = 30;
    showMessage(`신호가 왔다! [${currentFish.rarityName}] 등급 물고기!`, "Space 바를 눌러 게이지를 맞추세요!");
}

let waveOffset = 0;

function update() {
    waveOffset += 0.04;

    if (gameState === 'RESULT' && resultCooldown > 0) {
        resultCooldown--;
    }

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
            resultCooldown = 90;
            
            // 인벤토리에 추가
            inventory.unshift({
                id: nextFishId++,
                name: currentFish.name,
                rarity: currentFish.rarity,
                rarityName: currentFish.rarityName,
                price: currentFish.price
            });

            showMessage("🎉 낚시 성공!", `✨ [${currentFish.rarityName}] ${currentFish.name}(을)를 낚았습니다! (+${currentFish.price}$)`);
        } else if (catchProgress <= 0) {
            gameState = 'RESULT';
            resultCooldown = 90;
            showMessage("❌ 놓쳤습니다...", "잠시 후 Space/Enter를 눌러 다시 시도하세요.");
        }
    }
}

function drawPixelHatFisherman(x, y) {
    ctx.fillStyle = '#5c3d2e';
    ctx.fillRect(x - 40, y, 80, 20);
    ctx.fillStyle = '#3d2314';
    ctx.fillRect(x - 30, y + 20, 60, 10);

    ctx.fillStyle = '#1e3799';
    ctx.fillRect(x - 10, y - 25, 20, 25);

    ctx.fillStyle = '#f6b93b';
    ctx.beginPath();
    ctx.moveTo(x - 24, y - 22);
    ctx.lineTo(x + 24, y - 22);
    ctx.lineTo(x, y - 45);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(x - 24, y - 22, 48, 4);

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
        ctx.strokeStyle = '#15803d';
        ctx.lineWidth = 2;
        ctx.strokeRect(renderBarX, uiY, renderBarW, uiHeight);

        let renderFishX = uiX + (fishPos / 100) * uiWidth;
        ctx.fillStyle = currentFish.color;
        ctx.beginPath();
        ctx.arc(renderFishX, uiY + uiHeight / 2, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 2;
        ctx.stroke();

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
