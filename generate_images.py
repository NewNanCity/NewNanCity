from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# 基礎配置
assets_path = os.path.join(os.path.dirname(__file__), 'assets')
font_path = 'msyh.ttc'  # 微軟雅黑字體

base_date = datetime(2020, 2, 2)

def create_count_image(text, subtext, filename):
    img = Image.new('RGB', (400, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    
    # 主文字
    main_font = ImageFont.truetype(font_path, 48)
    d.text((10,50), text, font=main_font, fill=(255,255,0))
    
    # 副文字
    sub_font = ImageFont.truetype(font_path, 24)
    d.text((10,120), subtext, font=sub_font, fill=(255,255,255))
    
    img.save(os.path.join(assets_path, filename))

# 計算天數差
def day_diff(target):
    return (datetime.now() - target).days

# 每日自動生成
if __name__ == '__main__':
    days_since = day_diff(base_date)
    next_anniversary = base_date.replace(year=datetime.now().year + 1)
    days_remaining = (next_anniversary - datetime.now()).days
    
    create_count_image(f'已運行 {days_since} 天', 'days since', 'days_since.png')
    create_count_image(f'剩餘 {days_remaining} 天', 'days remaining', 'countdown.png')

# 在文件末尾添加
print(f"[{datetime.now().isoformat()}] 圖片生成完成")