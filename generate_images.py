from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import logging

# --- 日志记录设置 ---
# 判断运行环境
run_env = "github" if os.getenv("CI") else "local"
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True) # 确保 logs 文件夹存在

# 设置日志文件名和格式
log_filename = f"{run_env}-{datetime.now().strftime('%Y-%m-%d')}.log"
log_filepath = os.path.join(log_dir, log_filename)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filepath, 'a', 'utf-8'), # 写入文件
        logging.StreamHandler() # 同时在控制台输出
    ]
)
# --- 日志记录设置结束 ---


# 基礎配置
assets_path = os.path.join(os.path.dirname(__file__), 'assets')
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'msyh.ttc')
base_date = datetime(2020, 2, 2)
IMAGE_WIDTH = 225  # 統一圖片寬度
IMAGE_HEIGHT = 80  # 統一圖片高度


def create_count_image(title, days, filename):
    logging.info(f"开始生成图片: {filename}，标题: {title}，天数: {days}")
    try:
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
        
        output_path = os.path.join(assets_path, filename)
        img.save(output_path)
        logging.info(f"图片已成功保存到: {output_path}")
    except Exception as e:
        logging.error(f"生成图片 {filename} 时发生错误: {e}", exc_info=True)


# 計算天數差
def day_diff(target):
    return (datetime.now() - target).days

# 每日自動生成
if __name__ == '__main__':
    logging.info("="*30)
    logging.info(f"脚本启动，当前运行环境: {run_env}")
    
    logging.info("开始计算日期...")
    days_since = (datetime.now() - base_date).days
    next_anniversary = base_date.replace(year=datetime.now().year)
    if next_anniversary < datetime.now():
        next_anniversary = next_anniversary.replace(year=datetime.now().year + 1)
    days_remaining = (next_anniversary - datetime.now()).days
    anniversary_year = next_anniversary.year - base_date.year
    logging.info(f"服务器已运行 {days_since} 天")
    logging.info(f"距离 {anniversary_year} 周年还剩 {days_remaining} 天")
    
    create_count_image('服务器已运行了', f'{days_since} 天', 'days_since.png')
    create_count_image(f'距离{anniversary_year}周年剩余', f'{days_remaining} 天', 'countdown.png')
    
    logging.info("所有图片生成完成。")
    logging.info("="*30)