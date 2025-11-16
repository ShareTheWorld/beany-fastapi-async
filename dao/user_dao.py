from typing import Any, Coroutine, Sequence

from sqlmodel import select, or_
from sqlmodel.ext.asyncio.session import AsyncSession

from dao.base_dao import BaseDao
from model.user import User


class UserDao(BaseDao[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_account(self, session: AsyncSession, account: str) -> User | None:
        statement = select(User).where(or_(User.email == account, User.phone == account)).limit(1)
        result = await session.exec(statement)
        return result.first()
