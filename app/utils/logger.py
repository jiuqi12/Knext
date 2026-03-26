# 统一日志处理
import logging
import sys
from datetime import datetime
from pathlib import Path

# 确保 logs 目录存在
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# 创建 logger
logger = logging.getLogger("Knext")
logger.setLevel(logging.DEBUG)

# 避免重复添加 handler
if not logger.handlers:
    # 创建 console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # 创建 file handler
    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # 创建 formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


# 便捷函数
def get_logger(name: str = "Knext") -> logging.Logger:
    """获取指定名称的 logger"""
    return logging.getLogger(name)
