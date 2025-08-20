from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# --- 組態設定 ---
# 使用一個基礎的預設字體，不需要額外安裝字型檔案
# 如果您想使用自訂字體，可以將 .ttf 字型檔加入專案中
# 然後使用 font = ImageFont.truetype("字體路徑.ttf", 30)
FONT_SIZE_DEFAULT = 15 
BG_COLOR = (30, 30, 30) # 深灰色背景
TEXT_COLOR = (255, 255, 255) # 白色文字
OUTPUT_DIR = "assets" # 圖片輸出的資料夾
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 日期計算 ---
# 計時器 1: 從 2020-02-02 開始的天數
start_date = datetime(2020, 2, 2)
today = datetime.now()
days_since = (today - start_date).days
text1 = f"Launched:{days_since}days"

# 計時器 2: 距離下一個週年 (2月2日) 的倒數
next_anniversary_year = today.year if (today.month < 2 or (today.month == 2 and today.day <= 2)) else today.year + 1
next_anniversary_date = datetime(next_anniversary_year, 2, 2)
days_until = (next_anniversary_date - today).days
text2 = f"Next anniversary:{days_until}days"

# --- 圖片產生函式 ---
def create_image(text, filename, width=220, height=40):
    font = ImageFont.load_default(size=FONT_SIZE_DEFAULT)
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