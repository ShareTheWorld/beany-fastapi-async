from fastapi import APIRouter

from router import captcha
from router import user

api_router = APIRouter()
api_router.include_router(captcha.router)
api_router.include_router(user.router)


