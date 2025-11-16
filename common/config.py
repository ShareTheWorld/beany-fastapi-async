# config.py
import secrets
from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", )
    """FastAPI 应用配置"""
    # 应用基本信息
    APP_NAME: str = None
    APP_ENV: str = None
    DEBUG: bool = None
    SECRET_KEY: str = None
    ROOT_PATH: str = None

    DATABASE_URL: str = None

    # CORS 设置
    CORS_ORIGINS: List[str] = ['*']

    # 日志
    LOG_DIR: str = None
    LOG_NAME: str = None
    LOG_LEVEL: str = None

    SMTP_HOST: str = None
    SMTP_USER: str = None
    SMTP_PASSWORD: str = None
    SMTP_EMAIL: str = None
    SMTP_TLS: bool = None
    SMTP_SSL: bool = None
    SMTP_PORT: int = None

env = Env()