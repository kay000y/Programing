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
        max-width: 440px;
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

    /* 상단 좌측 버튼 배치 (도감 -> 인벤토리 -> 상점) */
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
    #inventoryBtn { top: 82px; left: 20px; }
    #shopBtn { top: 144px; left: 20px; }
    #settingsBtn { top: 20px; right: 20px; }

    /* 장착 낚싯대 소형 퀵 뷰 버튼 (인벤토리 오른쪽) */
    #equippedRodQuickBtn {
        position: absolute;
        top: 88px;
        left: 76px;
        height: 40px;
        padding: 0 10px;
        background-color: #1e293b;
        border: 2px solid #cbd5e1;
        border-radius: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: bold;
        color: #f8fafc;
        cursor: pointer;
        z-index: 20;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    #equippedRodQuickBtn:hover {
        border-color: #38bdf8;
        background-color: #334155;
    }

    /* 돈 표시 바 */
    #moneyBar {
        position: absolute;
        top: 20px;
        left: 78px;
        height: 52px;
        min-width: 140px;
        background-color: #1e293b;
        border: 2px solid #eab308;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 16px;
        color: #fde047;
        font-weight: 800;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        z-index: 20;
    }

    /* 모달 공통 레이아웃 */
    .modal {
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 440px;
        background-color: #1e293b;
        border: 3px solid #38bdf8;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.8);
        padding: 20px;
        color: white;
        z-index: 30;
    }

    #notebookModal {
        width: 520px;
        max-height: 600px;
    }

    #shopModal {
        width: 680px;
        max-height: 640px;
    }

    /* 개편된 대형 인벤토리 모달 (`680px`) */
    #inventoryModal {
        width: 680px;
        max-height: 660px;
    }

    .modalHeader {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    .modalTitle {
        font-size: 20px;
        font-weight: bold;
        color: #38bdf8;
    }
    .closeBtn {
        cursor: pointer;
        font-size: 22px;
        font-weight: bold;
        color: #94a3b8;
    }
    .closeBtn:hover {
        color: #ffffff;
    }

    /* 도감 헤더 박스 */
    #rarityRateBox {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        text-align: center;
    }
    .rateInfoCard {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
    }
    .ratePriceText {
        font-size: 13px;
        font-weight: 800;
        color: #fde047;
    }

    /* 상점 레이아웃 */
    #shopLayoutGrid {
        display: grid;
        grid-template-columns: 320px 1fr;
        gap: 16px;
        margin-top: 10px;
    }
    #sellFishSection {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        display: flex;
        flex-direction: column;
    }
    .sectionHeaderTitle {
        font-size: 14px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 8px;
    }
    #categoryGrid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: repeat(3, 42px);
        gap: 8px;
        margin-top: 12px;
    }
    .categoryBtn {
        background-color: #334155;
        color: #cbd5e1;
        border: 1px solid #475569;
        border-radius: 6px;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        transition: all 0.1s;
    }
    .categoryBtn:hover {
        background-color: #475569;
        color: #ffffff;
    }
    .categoryBtn.active {
        background-color: #38bdf8;
        color: #0f172a;
        border-color: #38bdf8;
    }

    #shopRightPanel {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    #itemPreviewBox {
        height: 140px;
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }
    #previewIcon { font-size: 48px; margin-bottom: 6px; }
    #previewName { font-size: 14px; font-weight: bold; color: #fde047; }
    #previewDesc { font-size: 11px; color: #94a3b8; margin-top: 2px; }

    #itemBuyBox {
        flex: 1;
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        max-height: 230px;
        overflow-y: auto;
    }

    /* === 인벤토리(가방) 전용 3분할 레이아웃 (상단 대형 1개 + 하단 소형 2개) === */
    #invTopBox {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        height: 220px;
        margin-bottom: 14px;
        display: flex;
        flex-direction: column;
    }

    /* 잡은 물고기 5열 바둑판 그리드 */
    #invFishGrid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        overflow-y: auto;
        padding-right: 4px;
        max-height: 170px;
    }
    .fishCard {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 6px;
        padding: 8px 4px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        gap: 4px;
    }
    .fishCardName {
        font-size: 12px;
        font-weight: bold;
        color: #f8fafc;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }

    #invBottomGrid {
        display: grid;
        grid-template-columns: 240px 1fr;
        gap: 14px;
        height: 220px;
    }
    #invCategoryBox {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        display: flex;
        flex-direction: column;
    }
    #invCategoryButtons {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 6px;
    }
    #invEquipSelectBox {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        display: flex;
        flex-direction: column;
    }

    .itemList {
        list-style: none;
        padding: 0;
        margin: 0;
        max-height: 300px;
        overflow-y: auto;
    }
    .itemList li {
        padding: 10px 14px;
        background-color: #334155;
        margin-bottom: 8px;
        border-radius: 6px;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .bookItem { padding: 12px 16px !important; }
    .bookFishName { font-size: 15px; font-weight: bold; color: #f8fafc; display: flex; align-items: center; gap: 8px; }
    .bookFishName.unknown { color: #64748b; }

    /* 등급 뱃지 */
    .badgeGroup { display: flex; gap: 4px; }
    .rarityBadge { font-size: 11px; padding: 3px 7px; border-radius: 4px; font-weight: bold; opacity: 0.25; filter: grayscale(80%); }
    .rarityBadge.active { opacity: 1.0; filter: grayscale(0%); }
    
    .badge-common { background-color: #94a3b8; color: #0f172a; }
    .badge-rare { background-color: #3b82f6; color: #ffffff; }
    .badge-legendary { background-color: #eab308; color: #0f172a; }

    /* 버튼 스타일 */
    .actionBtn {
        background-color: #10b981;
        color: white;
        border: none;
        padding: 5px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.1s;
    }
    .actionBtn:hover { background-color: #059669; }
    .actionBtn:disabled { background-color: #64748b; cursor: not-allowed; }

    .equipBtn { background-color: #3b82f6; }
    .equipBtn:hover { background-color: #2563eb; }

    .sellAllBtn {
        width: 100%;
        background-color: #ef4444;
        color: white;
        border: none;
        padding: 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 8px;
    }
    .sellAllBtn:hover { background-color: #dc2626; }

    .settingRow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .settingRow label { font-size: 14px; color: #cbd5e1; }
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
    
    <!-- 좌측 상단 버튼들 (도감 -> 인벤토리 -> 상점 순서) -->
    <div id="notebookBtn" class="topBtn" title="도감">📖</div>
    <div id="inventoryBtn" class="topBtn" title="인벤토리">🎒</div>
    <div id="shopBtn" class="topBtn" title="상점">🏪</div>
    
    <!-- 장착 낚싯대 소형 퀵 뷰 (인벤토리 오른쪽) -->
    <div id="equippedRodQuickBtn" title="현재 장착 중인 낚싯대">
        <span>🎣</span>
        <span id="quickRodName">나무 낚싯대</span>
    </div>

    <!-- 간결한 돈 표시 UI -->
    <div id="moneyBar"><span id="moneyText">0</span> &nbsp;$</div>

    <!-- 우측 상단 설정 버튼 -->
    <div id="settingsBtn" class="topBtn" title="Settings">⚙️</div>

    <!-- 1. 도감 모달 -->
    <div id="notebookModal" class="modal">
        <div class="modalHeader">
            <span class="modalTitle">📘 물고기 도감</span>
            <span id="closeNotebook" class="closeBtn">&times;</span>
        </div>
        
        <div id="rarityRateBox">
            <div class="rateInfoCard">
                <span class="rarityBadge badge-common active">일반 (45%)</span>
                <span class="ratePriceText">10 $</span>
            </div>
            <div class="rateInfoCard">
                <span class="rarityBadge badge-rare active">희귀 (35%)</span>
                <span class="ratePriceText">50 $</span>
            </div>
            <div class="rateInfoCard">
                <span class="rarityBadge badge-legendary active">전설 (20%)</span>
                <span class="ratePriceText">100 $</span>
            </div>
        </div>

        <ul id="logbookList" class="itemList" style="max-height: 380px;">
            <!-- JS 렌더링 -->
        </ul>
    </div>

    <!-- 2. 상점 모달 -->
    <div id="shopModal" class="modal">
        <div class="modalHeader">
            <span class="modalTitle">🏪 상점</span>
            <span id="closeShop" class="closeBtn">&times;</span>
        </div>

        <div id="shopLayoutGrid">
            <div>
                <div id="sellFishSection">
                    <div class="sectionHeaderTitle">🐟 Sell Fish</div>
                    <ul id="shopFishList" class="itemList" style="max-height: 160px; min-height: 140px;">
                        <li style="color: #94a3b8; justify-content: center;">보유 중인 물고기가 없습니다.</li>
                    </ul>
                    <button id="sellAllBtn" class="sellAllBtn">Sell All (Shift + E)</button>
                </div>

                <div id="categoryGrid">
                    <button class="categoryBtn active" onclick="selectShopCategory('rod')">🎣 낚싯대</button>
                    <button class="categoryBtn" onclick="selectShopCategory('bobber')">🎈 낚시찌</button>
                    <button class="categoryBtn" onclick="selectShopCategory('boat')">⛵ 배</button>
                    <button class="categoryBtn" onclick="selectShopCategory('bait')">🪱 미끼</button>
                    <button class="categoryBtn" onclick="selectShopCategory('etc1')">❓ ??</button>
                    <button class="categoryBtn" onclick="selectShopCategory('etc2')">❓ ??</button>
                </div>
            </div>

            <div id="shopRightPanel">
                <div id="itemPreviewBox">
                    <div id="previewIcon">🎣</div>
                    <div id="previewName">나무 낚싯대</div>
                    <div id="previewDesc">기본으로 지급되는 평범한 나무 낚싯대입니다.</div>
                </div>

                <div id="itemBuyBox">
                    <div class="sectionHeaderTitle" id="categoryTitleText">🎣 낚싯대 상점</div>
                    <ul id="categoryItemList" class="itemList" style="max-height: 160px;">
                        <!-- JS 생성 -->
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- 3. 개편된 인벤토리 모달 (상단 큰 칸 1개 + 하단 작은 칸 2개) -->
    <div id="inventoryModal" class="modal">
        <div class="modalHeader">
            <span class="modalTitle">🎒 인벤토리</span>
            <span id="closeInventory" class="closeBtn">&times;</span>
        </div>

        <!-- 위쪽 큰 칸: 잡은 물고기 (5열 그리드) -->
        <div id="invTopBox">
            <div class="sectionHeaderTitle">🐟 소지 물고기</div>
            <div id="invFishGrid">
                <!-- JS에서 5열 그리드로 생성 -->
            </div>
        </div>

        <!-- 아래쪽 작은 칸 2개 (좌측: 장비 종류 버튼 | 우측: 보유 장비 선택 칸) -->
        <div id="invBottomGrid">
            <!-- 하단 좌측: 장비 카테고리 셀렉터 -->
            <div id="invCategoryBox">
                <div class="sectionHeaderTitle">⚙️ 장비 종류</div>
                <div id="invCategoryButtons">
                    <button class="categoryBtn active" onclick="selectInvCategory('rod')">🎣 낚싯대</button>
                    <button class="categoryBtn" onclick="selectInvCategory('bobber')">🎈 낚시찌</button>
                    <button class="categoryBtn" onclick="selectInvCategory('boat')">⛵ 배</button>
                    <button class="categoryBtn" onclick="selectInvCategory('bait')">🪱 미끼</button>
                </div>
            </div>

            <!-- 하단 우측: 현재 보유 장비 목록 및 선택/사용 칸 -->
            <div id="invEquipSelectBox">
                <div class="sectionHeaderTitle" id="invEquipTitleText">🎣 보유 낚싯대</div>
                <ul id="invEquipItemList" class="itemList" style="max-height: 150px;">
                    <!-- JS 생성 -->
                </ul>
            </div>
        </div>
    </div>

    <!-- 4. 설정 모달 -->
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

    <!-- 상단 중앙 상태 메시지 -->
    <div id="messageOverlay">
        <div id="statusText">Press SPACE or ENTER to Start Fishing!</div>
        <div id="caughtInfo"></div>
    </div>

    <!-- 좌측 하단 조작 설명 -->
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

// 전체 어종 DB
const ALL_FISH_DATABASE = [
    { id: 1, name: "고등어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff", price: 10 },
    { id: 2, name: "광어", rarity: "common", rarityName: "일반", difficulty: 1.0, color: "#ffffff", price: 10 },
    { id: 3, name: "우럭", rarity: "common", rarityName: "일반", difficulty: 1.1, color: "#ffffff", price: 10 },
    { id: 4, name: "볼락", rarity: "common", rarityName: "일반", difficulty: 0.9, color: "#ffffff", price: 10 },
    { id: 5, name: "참돔", rarity: "rare", rarityName: "희귀", difficulty: 1.3, color: "#3b82f6", price: 50 },
    { id: 6, name: "오징어", rarity: "rare", rarityName: "희귀", difficulty: 1.2, color: "#3b82f6", price: 50 },
    { id: 7, name: "감성돔", rarity: "rare", rarityName: "희귀", difficulty: 1.4, color: "#3b82f6", price: 50 },
    { id: 8, name: "방어", rarity: "legendary", rarityName: "전설", difficulty: 1.6, color: "#eab308", price: 100 },
    { id: 9, name: "돗돔", rarity: "legendary", rarityName: "전설", difficulty: 1.8, color: "#eab308", price: 100 }
];

// 재화 및 데이터
let playerMoney = 0;
const bookRecords = new Map();
let inventoryFish = [];
let nextFishId = 1;

let currentShopCategory = 'rod';
let currentInvCategory = 'rod';
let equippedRodId = "wood";

// 통합 장비 데이터베이스
const SHOP_ITEMS = {
    rod: [
        { id: "wood", name: "나무 낚싯대", price: 0, icon: "🎣", desc: "기본 지급되는 단단한 나무 낚싯대", bought: true },
        { id: "stone", name: "돌 낚싯대", price: 100, icon: "🎣", desc: "묵직하고 튼튼한 돌 재질 낚싯대", bought: false },
        { id: "iron", name: "철 낚싯대", price: 10000, icon: "🎣", desc: "세련되고 유연한 정밀 철제 낚싯대", bought: false },
        { id: "gold", name: "금 낚싯대", price: 1000000, icon: "🎣", desc: "황금빛으로 빛나는 최고급 전설의 낚싯대", bought: false }
    ],
    bobber: [
        { id: "b1", name: "빨간 찌", price: 50, icon: "🎈", desc: "기본 선명한 빨간색 낚시찌", bought: false },
        { id: "b2", name: "형광 찌", price: 500, icon: "💡", desc: "야간에도 잘 보이는 형광 낚시찌", bought: false }
    ],
    boat: [
        { id: "bt1", name: "목선", price: 0, icon: "⛵", desc: "작고 오래된 소형 나무 배", bought: true },
        { id: "bt2", name: "모터보트", price: 50000, icon: "🚤", desc: "바다를 빠르게 가르는 모터보트", bought: false }
    ],
    bait: [
        { id: "ba1", name: "지렁이 미끼", price: 5, icon: "🪱", desc: "일반 물고기 반응을 돕는 미끼", bought: false },
        { id: "ba2", name: "새우 미끼", price: 20, icon: "🦐", desc: "희귀 물고기가 좋아하는 싱싱한 새우", bought: false }
    ],
    etc1: [
        { id: "e1", name: "준비 중인 아이템", price: 99999, icon: "❓", desc: "다음 업데이트에 추가될 예정입니다.", bought: false }
    ],
    etc2: [
        { id: "e2", name: "준비 중인 아이템", price: 99999, icon: "❓", desc: "다음 업데이트에 추가될 예정입니다.", bought: false }
    ]
};

function updateMoneyUI() {
    document.getElementById('moneyText').innerText = playerMoney.toLocaleString();
}

function updateEquippedRodUI() {
    const rod = SHOP_ITEMS.rod.find(r => r.id === equippedRodId);
    if (rod) {
        document.getElementById('quickRodName').innerText = rod.name;
    }
}

function sellFish(index) {
    if (index >= 0 && index < inventoryFish.length) {
        const item = inventoryFish[index];
        playerMoney += item.price;
        inventoryFish.splice(index, 1);
        updateMoneyUI();
        updateShopUI();
        updateInventoryUI();
    }
}

function sellTopFish() {
    if (inventoryFish.length > 0) {
        sellFish(0);
    }
}

function sellAllFish() {
    if (inventoryFish.length > 0) {
        let total = 0;
        inventoryFish.forEach(item => total += item.price);
        playerMoney += total;
        inventoryFish = [];
        updateMoneyUI();
        updateShopUI();
        updateInventoryUI();
    }
}

function buyShopItem(category, itemId) {
    const item = SHOP_ITEMS[category].find(i => i.id === itemId);
    if (item && !item.bought && playerMoney >= item.price) {
        playerMoney -= item.price;
        item.bought = true;
        if (category === 'rod') {
            equippedRodId = item.id;
            updateEquippedRodUI();
        }
        updateMoneyUI();
        updateShopUI();
        updateInventoryUI();
    }
}

function equipRod(rodId) {
    const rod = SHOP_ITEMS.rod.find(r => r.id === rodId);
    if (rod && rod.bought) {
        equippedRodId = rod.id;
        updateEquippedRodUI();
        updateShopUI();
        updateInventoryUI();
    }
}

// 게임 내부 상태
let gameState = 'IDLE';
let waitTimer = 0;
let castTimer = 0;
let resultCooldown = 0;
let rodAngle = 0;
let spacePressed = false;

let messageTimer = 0;
const messageOverlay = document.getElementById('messageOverlay');

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

    const pool = ALL_FISH_DATABASE.filter(f => f.rarity === rarity);
    return pool[Math.floor(Math.random() * pool.length)];
}

// 키보드 조작
window.addEventListener('keydown', (e) => {
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

// UI 모달 컨트롤
const notebookBtn = document.getElementById('notebookBtn');
const shopBtn = document.getElementById('shopBtn');
const inventoryBtn = document.getElementById('inventoryBtn');
const settingsBtn = document.getElementById('settingsBtn');
const equippedRodQuickBtn = document.getElementById('equippedRodQuickBtn');

const notebookModal = document.getElementById('notebookModal');
const shopModal = document.getElementById('shopModal');
const inventoryModal = document.getElementById('inventoryModal');
const settingsModal = document.getElementById('settingsModal');

const closeNotebook = document.getElementById('closeNotebook');
const closeShop = document.getElementById('closeShop');
const closeInventory = document.getElementById('closeInventory');
const closeSettings = document.getElementById('closeSettings');
const sellAllBtn = document.getElementById('sellAllBtn');

function hideAllModals() {
    notebookModal.style.display = 'none';
    shopModal.style.display = 'none';
    inventoryModal.style.display = 'none';
    settingsModal.style.display = 'none';
}

notebookBtn.addEventListener('click', () => {
    hideAllModals();
    updateNotebookUI();
    notebookModal.style.display = 'block';
});

shopBtn.addEventListener('click', () => {
    hideAllModals();
    updateShopUI();
    shopModal.style.display = 'block';
});

inventoryBtn.addEventListener('click', () => {
    hideAllModals();
    updateInventoryUI();
    inventoryModal.style.display = 'block';
});

equippedRodQuickBtn.addEventListener('click', () => {
    hideAllModals();
    currentInvCategory = 'rod';
    updateInventoryUI();
    inventoryModal.style.display = 'block';
});

settingsBtn.addEventListener('click', () => {
    hideAllModals();
    settingsModal.style.display = 'block';
});

closeNotebook.addEventListener('click', hideAllModals);
closeShop.addEventListener('click', hideAllModals);
closeInventory.addEventListener('click', hideAllModals);
closeSettings.addEventListener('click', hideAllModals);
sellAllBtn.addEventListener('click', sellAllFish);

// 상점 카테고리 선택
function selectShopCategory(catKey) {
    currentShopCategory = catKey;
    const btns = document.querySelectorAll('#categoryGrid .categoryBtn');
    btns.forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');
    updateShopUI();
}

// 인벤토리 카테고리 선택
function selectInvCategory(catKey) {
    currentInvCategory = catKey;
    const btns = document.querySelectorAll('#invCategoryButtons .categoryBtn');
    btns.forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');
    updateInventoryUI();
}

function setPreviewItem(item) {
    document.getElementById('previewIcon').innerText = item.icon;
    document.getElementById('previewName').innerText = item.name;
    document.getElementById('previewDesc').innerText = item.desc;
}

// UI 업데이트 로직들
function updateNotebookUI() {
    const listEl = document.getElementById('logbookList');
    listEl.innerHTML = '';
    
    ALL_FISH_DATABASE.forEach((fish) => {
        const caughtRarities = bookRecords.get(fish.id);
        const isDiscovered = caughtRarities && caughtRarities.size > 0;
        
        const numStr = fish.id < 10 ? `0${fish.id}` : `${fish.id}`;
        const displayName = isDiscovered ? fish.name : "???";

        const commonActive = caughtRarities && caughtRarities.has('common') ? 'active' : '';
        const rareActive = caughtRarities && caughtRarities.has('rare') ? 'active' : '';
        const legendaryActive = caughtRarities && caughtRarities.has('legendary') ? 'active' : '';

        const li = document.createElement('li');
        li.className = "bookItem";
        li.innerHTML = `
            <div class="bookFishName ${isDiscovered ? '' : 'unknown'}">
                <span style="color: #38bdf8; font-size: 13px;">#${numStr}</span>
                <span>${displayName}</span>
            </div>
            <div class="badgeGroup">
                <span class="rarityBadge badge-common ${commonActive}">일반</span>
                <span class="rarityBadge badge-rare ${rareActive}">희귀</span>
                <span class="rarityBadge badge-legendary ${legendaryActive}">전설</span>
            </div>
        `;
        listEl.appendChild(li);
    });
}

function updateShopUI() {
    const shopListEl = document.getElementById('shopFishList');
    shopListEl.innerHTML = '';

    if (inventoryFish.length === 0) {
        shopListEl.innerHTML = '<li style="color: #94a3b8; justify-content: center;">보유 중인 물고기가 없습니다.</li>';
    } else {
        inventoryFish.forEach((item, idx) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>🐟 ${item.name} (${item.price}$)</span>
                <button class="actionBtn" onclick="sellFish(${idx})">Sell (${item.price}$)</button>
            `;
            shopListEl.appendChild(li);
        });
    }

    const catTitles = {
        rod: "🎣 낚싯대 상점",
        bobber: "🎈 낚시찌 상점",
        boat: "⛵ 배 상점",
        bait: "🪱 미끼 상점",
        etc1: "❓ 준비 중인 상점",
        etc2: "❓ 준비 중인 상점"
    };

    document.getElementById('categoryTitleText').innerText = catTitles[currentShopCategory];
    const categoryItemList = document.getElementById('categoryItemList');
    categoryItemList.innerHTML = '';

    const items = SHOP_ITEMS[currentShopCategory] || [];
    if (items.length > 0) setPreviewItem(items[0]);

    items.forEach((item) => {
        const li = document.createElement('li');
        li.onmouseenter = () => setPreviewItem(item);

        let btnHtml = '';
        if (item.bought) {
            btnHtml = `<span style="color: #22c55e; font-weight: bold; font-size: 12px;">Owned</span>`;
        } else {
            const canAfford = playerMoney >= item.price;
            btnHtml = `<button class="actionBtn" ${canAfford ? '' : 'disabled'} onclick="buyShopItem('${currentShopCategory}', '${item.id}')">Buy (${item.price.toLocaleString()}$)</button>`;
        }

        li.innerHTML = `
            <span>${item.icon} ${item.name}</span>
            ${btnHtml}
        `;
        categoryItemList.appendChild(li);
    });
}

// 개편된 인벤토리 UI 렌더링 (상단 5열 그리드 물고기 + 하단 보유 장비)
function updateInventoryUI() {
    // 1. 상단 소지 물고기 5열 바둑판 그리드
    const invFishGrid = document.getElementById('invFishGrid');
    invFishGrid.innerHTML = '';

    if (inventoryFish.length === 0) {
        invFishGrid.innerHTML = '<div style="grid-column: span 5; color: #94a3b8; text-align: center; padding: 30px 0;">가방에 물고기가 없습니다.</div>';
    } else {
        inventoryFish.forEach((item) => {
            const div = document.createElement('div');
            div.className = "fishCard";
            div.innerHTML = `
                <div style="font-size: 24px;">🐟</div>
                <div class="fishCardName">${item.name}</div>
                <span class="rarityBadge badge-${item.rarity} active">${item.rarityName}</span>
            `;
            invFishGrid.appendChild(div);
        });
    }

    // 2. 하단 우측 보유 장비 선택 칸
    const catTitles = {
        rod: "🎣 보유 낚싯대",
        bobber: "🎈 보유 낚시찌",
        boat: "⛵ 보유 배",
        bait: "🪱 보유 미끼"
    };
    document.getElementById('invEquipTitleText').innerText = catTitles[currentInvCategory] || "⚙️ 보유 장비";

    const invEquipItemList = document.getElementById('invEquipItemList');
    invEquipItemList.innerHTML = '';

    const ownedItems = (SHOP_ITEMS[currentInvCategory] || []).filter(i => i.bought);

    if (ownedItems.length === 0) {
        invEquipItemList.innerHTML = '<li style="color: #94a3b8; justify-content: center;">보유 중인 장비가 없습니다.</li>';
    } else {
        ownedItems.forEach((item) => {
            const li = document.createElement('li');
            let btnHtml = '';

            if (currentInvCategory === 'rod') {
                const isEquipped = item.id === equippedRodId;
                btnHtml = isEquipped 
                    ? `<span style="color: #38bdf8; font-weight: bold; font-size: 12px;">Equipped</span>`
                    : `<button class="actionBtn equipBtn" onclick="equipRod('${item.id}')">Equip</button>`;
            } else {
                btnHtml = `<span style="color: #22c55e; font-weight: bold; font-size: 12px;">Owned</span>`;
            }

            li.innerHTML = `
                <span>${item.icon} ${item.name}</span>
                ${btnHtml}
            `;
            invEquipItemList.appendChild(li);
        });
    }
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
            
            if (!bookRecords.has(currentFish.id)) {
                bookRecords.set(currentFish.id, new Set());
            }
            bookRecords.get(currentFish.id).add(currentFish.rarity);

            inventoryFish.unshift({
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

    let rodColor = '#cbd5e1';
    if (equippedRodId === 'stone') rodColor = '#94a3b8';
    else if (equippedRodId === 'iron') rodColor = '#38bdf8';
    else if (equippedRodId === 'gold') rodColor = '#eab308';

    ctx.strokeStyle = rodColor;
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

// 초기 UI 업데이트
updateMoneyUI();
updateEquippedRodUI();

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=1000, scrolling=False)
