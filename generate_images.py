from datetime import datetime, date
from zoneinfo import ZoneInfo # 引入时区库
from PIL import Image, ImageDraw, ImageFont
import os
import logging

# --- 时区设置 ---
# 设定我们想要使用的时区为香港时间
HKT = ZoneInfo("Asia/Hong_Kong")
# 获取当前准确的香港时间
now_hkt = datetime.now(HKT)
# --- 时区设置结束 ---

# --- 日志记录设置 ---
run_env = "github" if os.getenv("CI") else "local"
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

# 使用香港时间的日期来命名日志文件
log_filename = f"{run_env}-{now_hkt.strftime('%Y-%m-%d')}.log"
log_filepath = os.path.join(log_dir, log_filename)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filepath, 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)
# --- 日志记录设置结束 ---

# 基础配置
assets_path = os.path.join(os.path.dirname(__file__), 'assets')
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'msyh.ttc')
base_date_val = date(2020, 2, 2) # 使用 date 对象进行日期计算
IMAGE_WIDTH = 225
IMAGE_HEIGHT = 80

def create_count_image(title, days, filename):
    logging.info(f"开始生成图片: {filename}，标题: {title}，天数: {days}")
    try:
        img = Image.new('RGB', (IMAGE_WIDTH, 100), color='#0d1117')
        d = ImageDraw.Draw(img)
        
        title_font = ImageFont.truetype(font_path, 30)
        title_bbox = title_font.getbbox(title)
        d.text(
            ((IMAGE_WIDTH - (title_bbox[2]-title_bbox[0]))/2, 15),
            title,
            font=title_font,
            fill=(255,215,0) if 'countdown' in filename else (0,128,128)
        )
        
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

# 每日自動生成
if __name__ == '__main__':
    logging.info("="*30)
    logging.info(f"脚本启动，当前运行环境: {run_env}")
    logging.info(f"使用香港时间: {now_hkt.isoformat()}") # 记录当前准确的香港时间
    
    logging.info("开始基于香港日期进行计算...")
    today_hkt = now_hkt.date() # 获取香港日期的“日期”部分

    # 计算已运行天数
    days_since = (today_hkt - base_date_val).days

    # 计算距离下一个周年纪念日的天数
    anniversary_this_year = base_date_val.replace(year=today_hkt.year)
    if anniversary_this_year < today_hkt:
        # 如果今年的纪念日已经过去，则计算明年的
        next_anniversary_date = anniversary_this_year.replace(year=today_hkt.year + 1)
    else:
        next_anniversary_date = anniversary_this_year
        
    days_remaining = (next_anniversary_date - today_hkt).days
    anniversary_year = next_anniversary_date.year - base_date_val.year
    
    logging.info(f"服务器已运行 {days_since} 天")
    logging.info(f"距离 {anniversary_year} 周年还剩 {days_remaining} 天")
    
    create_count_image('服务器已运行了', f'{days_since} 天', 'days_since.png')
    create_count_image(f'距离{anniversary_year}周年剩余', f'{days_remaining} 天', 'countdown.png')
    
    logging.info("所有图片生成完成。")
    logging.info("="*30)