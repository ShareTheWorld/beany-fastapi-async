from typing import Any, Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

from common import logger


class ResponseModel(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None

    @staticmethod
    def success(data: Any = None):
        return {"code": 200, "msg": "success", "data": data}

    @staticmethod
    def error(code: int = -1, msg: str = "error"):
        return {"code": code, "msg": msg, "data": None}


class BizException(Exception):
    def __init__(self, code=-1, msg=''):
        super().__init__(f"code:{code}, msg:{msg}")
        self.code = code
        self.msg = msg


headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
}


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    捕获Pydantic校验错误（请求参数错误）
    """
    logger.exception(f"Unhandled exception: {exc}")
    error = exc.errors()[0]  # 取第一个错误
    msg = error.get("msg")  # 直接取 msg
    return JSONResponse(status_code=200, content=ResponseModel.error(-1, msg), headers=headers)


async def biz_exception_handler(request: Request, exc: BizException):
    """
    处理自定义业务异常
    """
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=200, content=ResponseModel.error(exc.code, exc.msg), headers=headers)


async def global_exception_handler(request: Request, exc: Exception):
    """
    处理全局异常
    """
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=200, content=ResponseModel.error(-1, str(exc)), headers=headers)
