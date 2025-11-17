from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

from store.postgres import BaseModel

# -------------------- 泛型 BaseDao --------------------
T = TypeVar("T", bound=BaseModel)


class BaseDao(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    # --------------------- 创建 ---------------------
    async def insert(self, session: AsyncSession, obj: T) -> T:
        now = datetime.now()
        if not getattr(obj, "create_at", None):
            obj.create_at = now
        obj.update_at = now
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def insert_dict(self, session: AsyncSession, data: Dict[str, Any]) -> T:
        obj = self.model(**data)
        return await self.insert(session, obj)

    # --------------------- 查询单条通过id ---------------------
    async def get_by_id(self, session: AsyncSession, id: Any) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)
        result = await session.exec(stmt)
        return result.first()

    # --------------------- 查询单条通过指定条件 ---------------------
    async def get(self, session: AsyncSession, **filters) -> Optional[T]:
        stmt = select(self.model).filter_by(**filters).limit(1)
        result = await session.exec(stmt)
        return result.first()

    # --------------------- 查询多条 ---------------------
    async def select(self, session: AsyncSession, filters: Optional[Dict[str, Any]] = None,
                     limit: Optional[int] = None, offset: Optional[int] = None, ) -> list[T]:
        stmt = select(self.model)
        if filters:
            for key, value in filters.items():
                stmt = stmt.where(getattr(self.model, key) == value)
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = await session.exec(stmt)
        return result.scalar().all()

    # --------------------- 通过指定条件判断是否存在 ---------------------
    async def exists(self, session: AsyncSession, **filters) -> bool:
        obj = await self.get(session, **filters)
        return obj is not None

    # -------------------- 通过指定条件统计条数 -----------------------
    async def count(self, session: AsyncSession, **filters) -> int:
        stmt = select(self.model).filter_by(**filters)
        result = await session.exec(stmt)
        return len(result.all())

    # --------------------- 更新字段 ---------------------
    async def update(self, session: AsyncSession, id: Any, **fields: Any) -> Optional[T]:
        obj = await self.get_by_id(session, id)
        if not obj:
            return None

        for key, value in fields.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        obj.update_at = datetime.now()
        session.add(obj)

        await session.commit()
        await session.refresh(obj)
        return obj

    # --------------------- 删除 ---------------------
    async def delete(self, session: AsyncSession, id: int) -> bool:
        obj = await self.get_by_id(session, id)
        if not obj:
            return False
        await session.delete(obj)
        await session.commit()
        return True
