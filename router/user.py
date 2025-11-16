from fastapi import APIRouter

from common import ResponseModel
from common import UserDep, DbDep
from common import logger
from model.user import LoginReq
from service import user_service

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/login")
async def login(db: DbDep, req: LoginReq):
    data = await user_service.login(db, req)
    return ResponseModel.success(data)


@router.get("/me")
async def me(user: UserDep):
    return ResponseModel.success(user)
