import os
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

from common import env

LOG_NAME = env.LOG_NAME
LOG_DIR = env.LOG_DIR
LOG_LEVEL = env.LOG_LEVEL

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_logger(name: str = "beany"):
    """
    企业级 Logger:
    - 控制台输出
    - 每天自动切割日志文件
    - 格式规范
    """
    log = logging.getLogger(name)
    log.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    log.propagate = False  # 防止重复打印

    # ======================
    # 日志格式（企业级）
    # ======================
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ======================
    # 1. 控制台 Handler
    # ======================
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)

    # ======================
    # 2. 每天自动切分文件 Handler
    # ======================
    # file_handler = TimedRotatingFileHandler(
    #     filename=f"{LOG_DIR}/{LOG_NAME}.log",
    #     when="midnight",  # 每天0点切割
    #     interval=1,
    #     backupCount=15,  # 保留15天
    #     encoding="utf-8"
    # )
    # ======================
    # 2. 按大小拆分
    # ======================
    file_handler = RotatingFileHandler(
        filename=f"{LOG_DIR}/{LOG_NAME}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB 一个文件
        backupCount=10
    )

    file_handler.suffix = "%Y-%m-%d"  # 文件名格式：app-2025-11-15.log
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log


# 全局 logger
logger = get_logger()
