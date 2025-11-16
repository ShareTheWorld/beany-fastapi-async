from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Enum as SqlEnum

from store.postgres import BaseModel


class Channel:
    email = "email"
    sms = "sms"


class Scene:
    auth = "auth"
    general = "general"


class Status:
    pending = "pending"
    sent = "sent"
    failed = "failed"


class Captcha(BaseModel, table=True):
    __tablename__ = "captcha"

    id: int = Field(nullable=False, default=None, primary_key=True)
    account: str = Field(nullable=False, default='')
    channel: str = Field(nullable=False, default='')
    scene: str = Field(nullable=False, default='')
    code: str = Field(nullable=False, default='')
    expire_at: datetime = Field(nullable=False)
    used: bool = Field(nullable=False, default=False)
    used_at: datetime = Field(nullable=False, default=None)
    status: str = Field(nullable=False, default=Status.pending)
    remark: Optional[str] = Field(nullable=False, default='', max_length=255)


class CaptchaSendCodeReq(SQLModel):
    account: Optional[str] = Field(..., description="账号：邮箱或者手机号")
