from datetime import timedelta

from common.deps import DbDep
from dao import user_dao
from model.user import LoginReq, User
from service import captcha_service
from util import utils


async def login(db: DbDep, req: LoginReq):
    """
    用户登录接口，如果不存在，会自动注册
    如果不允许自动注册，可以在最开始加校验，发送验证码的时候也校验用户是否存在
    :param db:
    :param req:
    :return:
    """
    await captcha_service.verify_account_captcha(db, req.account, req.code)
    user = await user_dao.get_by_account(db, account=req.account)
    if not user:
        name = req.account[0].upper()
        email = req.account if '@' in req.account else ""
        phone = req.account if '@' not in req.account else ""
        user = User(name=name, email=email, phone=phone)
        user = await user_dao.insert(db, user)
    token = utils.create_access_token(user.id, timedelta(days=8))
    return {"access_token": token, "token_type": "bearer"}
