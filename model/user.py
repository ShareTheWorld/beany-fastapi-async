import uuid

from pydantic import EmailStr, BaseModel, AnyHttpUrl
from sqlmodel import SQLModel, Field

import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

from store.postgres import BaseModel


class User(BaseModel, table=True):
    """用户表"""
    __tablename__ = "user"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="id")
    name: str = Field(default="", nullable=False, description="昵称")
    email: str = Field(default="", nullable=False, description="邮箱")
    phone: str = Field(default="", nullable=False, description="手机号")
    avatar: str = Field(default="", nullable=False, description="头像")
    create_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, description="创建时间")
    update_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, description="更新时间")


class LoginReq(SQLModel):
    account: str = Field(..., description="账号：邮箱或者手机号")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
