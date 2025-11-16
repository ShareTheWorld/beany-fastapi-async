from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from common import ResponseModel
from common import DbDep
from model.captcha import CaptchaSendCodeReq
from service import captcha_service
from store.postgres import get_db

router = APIRouter(prefix="/captcha", tags=["captcha"])


@router.post("/send_code")
async def send_code(db: DbDep, req: CaptchaSendCodeReq):
    res = await captcha_service.send_code(db, req)
    return ResponseModel.success(res)
