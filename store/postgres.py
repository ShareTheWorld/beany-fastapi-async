from datetime import datetime
from typing import AsyncGenerator, Any

from pydantic import field_serializer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import SQLModel, Field

from common.config import env

engine = create_async_engine(env.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class BaseModel(SQLModel):
    """带时间戳序列化的基础模型"""
    id: Any
    create_at: datetime = Field(default_factory=datetime.now, nullable=False)
    update_at: datetime = Field(default_factory=datetime.now, nullable=False)

    @field_serializer("create_at", "update_at")
    def serialize_datetime(self, dt: datetime, _info):
        """自动将 datetime 序列化为秒级时间戳"""
        return int(dt.timestamp())


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
