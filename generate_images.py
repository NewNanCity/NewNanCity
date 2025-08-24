from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# 基礎配置
assets_path = os.path.join(os.path.dirname(__file__), 'assets')
# 修改这里，指向项目中的字体文件
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'msyh.ttc')
base_date = datetime(2020, 2, 2)
IMAGE_WIDTH = 225  # 統一圖片寬度
IMAGE_HEIGHT = 80  # 統一圖片高度


def create_count_image(title, days, filename):
    # 使用类似GitHub深色模式的背景色
    img = Image.new('RGB', (IMAGE_WIDTH, 100), color='#0d1117')
    d = ImageDraw.Draw(img)
    
    # 標題繪製
    title_font = ImageFont.truetype(font_path, 30)
    title_bbox = title_font.getbbox(title)
    d.text(
        ((IMAGE_WIDTH - (title_bbox[2]-title_bbox[0]))/2, 15),
        title,
        font=title_font,
        fill=(255,215,0) if 'countdown' in filename else (0,128,128)
    )
    
    # 天數繪製
    days_font = ImageFont.truetype(font_path, 20)
    days_bbox = days_font.getbbox(days)
    d.text(
        ((IMAGE_WIDTH - (days_bbox[2]-days_bbox[0]))/2, 60),
        days,
        font=days_font,
        fill=(255,255,255)
    )
    
    img.save(os.path.join(assets_path, filename))

# 計算天數差
def day_diff(target):
    return (datetime.now() - target).days

# 每日自動生成
if __name__ == '__main__':
    days_since = (datetime.now() - base_date).days
    next_date = base_date.replace(year=datetime.now().year + 1)
    days_remaining = (next_date - datetime.now()).days
    
    create_count_image('服务器已运行了', f'{days_since} 天', 'days_since.png')
    create_count_image('距离六周年剩余', f'{days_remaining} 天', 'countdown.png')



# 在文件末尾添加
print(f"[{datetime.now().isoformat()}] 圖片生成完成")