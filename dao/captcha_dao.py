from datetime import datetime
from typing import Optional, Dict, Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from dao.base_dao import BaseDao
from model.captcha import Captcha


class CaptchaDao(BaseDao[Captcha]):
    def __init__(self):
        super().__init__(Captcha)

    async def get_by_account_and_code(self, session: AsyncSession, account: str, code: str) -> Captcha | None:
        statement = select(Captcha).where(
            Captcha.account == account,
            Captcha.code == code,
        ).order_by(Captcha.id.desc()).limit(1)
        result = await session.exec(statement)
        return result.first()



