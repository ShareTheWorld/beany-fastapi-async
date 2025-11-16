from datetime import datetime, timedelta, timezone
import random
import string
from datetime import timedelta
from typing import Any

import jwt

from common import env


def generate_captcha(length=6) -> str:
    """生成随机数字验证码"""
    return ''.join(random.choices(string.digits, k=length))


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
