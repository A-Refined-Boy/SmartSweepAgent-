"""
日志管理
"""

import logging
import sys
from multiprocessing.util import DEFAULT_LOGGING_FORMAT

from utils.path_tool import get_abs_path
import os
from datetime import datetime

#日志保存的根目录
LOG_ROOT = get_abs_path('logs')

#确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

#日志的格式配置
DEFAULT_LOGGING_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
)

#获取日志器的函数
def get_logger(

        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file = None,
)->logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #避免重复添加Handler
    if logger.handlers:
        return logger

    #控制台的Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOGGING_FORMAT)
    #将控制台的Handler添加到日志器中
    logger.addHandler(console_handler)

    #文件Handler
    if not log_file:
        #日志文件的存放路径
        log_file = os.path.join(LOG_ROOT, f'{name}_{datetime.now().strftime("%Y-%m-%d")}.log')      #时间只显示（年、月、日）

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOGGING_FORMAT)

    #将文件Handler添加到日志器中
    logger.addHandler(file_handler)

    #返回日志器
    return logger

#快捷获取日志器
logger = get_logger()





