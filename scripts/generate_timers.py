import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests  # 引入 requests 函式庫來下載檔案

# --- 組態設定 ---
# 使用開源的思源黑體來支援中文
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC-Regular.otf"
FONT_PATH = "scripts/NotoSansSC-Regular.otf"
FONT_SIZE_DEFAULT = 18  # 調整字體大小以獲得更好的可讀性
BG_COLOR = (30, 30, 30)  # 深灰色背景
TEXT_COLOR = (255, 255, 255)  # 白色文字
OUTPUT_DIR = "assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 字體下載 ---
# 檢查字體檔案是否存在，如果不存在，就從網路上下載
if not os.path.exists(FONT_PATH):
    print(f"Downloading font from {FONT_URL}...")
    try:
        response = requests.get(FONT_URL)
        response.raise_for_status()  # 如果下載失敗會拋出錯誤
        with open(FONT_PATH, "wb") as f:
            f.write(response.content)
        print("Font downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading font: {e}")
        FONT_PATH = None  # 標記字體路徑為空，以使用後備方案

# --- 日期計算 ---
start_date = datetime(2020, 2, 2)
today = datetime.now()
days_since = (today - start_date).days
text1 = f"We have been running for: {days_since} days"


next_anniversary_year = today.year if (today.month < 2 or (today.month == 2 and today.day <= 2)) else today.year + 1
next_anniversary_date = datetime(next_anniversary_year, 2, 2)
days_until = (next_anniversary_date - today).days
text2 = f"Days until next anniversary: {days_until} days"


# --- 圖片產生函式 ---
def create_image(text, filename, width=240, height=40):  # 加寬圖片以容納中文
    # 載入下載好的字體，如果下載失敗則使用後備的預設字體
    try:
        if FONT_PATH and os.path.exists(FONT_PATH):
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE_DEFAULT)
        else:
            print("警告：中文字體不存在，將使用預設字體 (中文無法顯示)。")
            font = ImageFont.load_default(size=15)
    except IOError:
        print(f"無法從 {FONT_PATH} 載入字體，將使用預設字體。")
        font = ImageFont.load_default(size=15)

    image = Image.new('RGB', (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(image)

    # 計算文字位置使其置中
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((width - text_width) / 2, (height - text_height) / 2)

    draw.text(position, text, font=font, fill=TEXT_COLOR)

    filepath = os.path.join(OUTPUT_DIR, filename)
    image.save(filepath)
    print(f"Generated image: {filepath}")

# --- 主程式執行 ---
create_image(text1, "days_since.png")
create_image(text2, "countdown.png")