from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from common import env
from dao import user_dao
from model.user import User
from store.postgres import get_db

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{env.ROOT_PATH}/user/login")


async def get_current_user(db=Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    payload = jwt.decode(token, env.SECRET_KEY, algorithms=["HS256"])
    user = await user_dao.get_by_id(db, payload['sub'])
    assert user, "User not found"
    return user


UserDep = Annotated[User, Depends(get_current_user)]
DbDep = Annotated[AsyncSession, Depends(get_db)]
