from datetime import datetime, timedelta
from typing import Any
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader, select_autoescape
import aiosmtplib
from fastapi.logger import logger
from sqlmodel.ext.asyncio.session import AsyncSession

from common import env
from common import DbDep

from model.captcha import CaptchaSendCodeReq, Captcha, Channel, Scene, Status
from util.utils import generate_captcha
from dao import captcha_dao

# 异步 Jinja2 环境
env_jinja = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html", "xml"]), enable_async=True)


async def verify_account_captcha(db: AsyncSession, account: str, code: str) -> bool:
    """
    验证验证码是否正确
    :param db:
    :param account: 账号：邮箱/手机
    :param code: 验证码
    :return:
    """
    captcha = await captcha_dao.get_by_account_and_code(db, account, code)
    assert captcha, "验证码错误"
    assert not captcha.used, "验证码已被使用"
    await captcha_dao.update(db, captcha.id, used=True, user_at=datetime.now())
    assert captcha.expire_at > datetime.now(), "验证码已过期"
    assert captcha.status == Status.sent, "未发送此验证码"
    return True


async def send_code(db: DbDep, req: CaptchaSendCodeReq):
    """
    发送验证码
    :param db:
    :param req:
    :return:
    """
    code = generate_captcha()
    channel = Channel.email if '@' in req.account else Channel.sms
    captcha = Captcha(
        account=req.account,
        channel=channel,
        scene=Scene.auth,
        code=code,
        expire_at=datetime.now() + timedelta(minutes=5),
        status=Status.pending,
    )
    captcha = await captcha_dao.insert(db, captcha)
    try:
        if channel == Channel.email:
            await send_email_code(req.account, code)
        else:
            await send_sms_code(req.account, code)
        await captcha_dao.update(db, captcha.id, status=Status.sent)
        return {"data": True}
    except Exception as e:
        await captcha_dao.update(db, captcha.id, status=Status.failed, remark=str(e))
        return {"data": False}


async def send_sms_code(phone: str, code: str):
    """
    发送手机验证码
    :param phone: 手机号
    :param code: 验证码
    :return:
    """
    logger.info(f"✅ phone sent successfully to {phone},{code}")
    pass


async def send_email_code(email_to: str, code: str):
    """
    发送邮箱验证码
    :param email_to: 目的邮箱
    :param code: 验证码
    :return:
    """
    context = {
        "title": "Beany AI",
        "code": code,
        "expires_minutes": 5,
        "support_email": "beany@qq.com",
        "current_year": datetime.now().year,
    }

    html_content = await render_email_template("captcha_email.html", context)
    subject = "Authentication captcha"

    await send_email(email_to=email_to, subject=subject, html_content=html_content)


async def render_email_template(template_name: str, context: dict[str, Any]) -> str:
    """
    渲染一个html
    :param template_name:模板名字
    :param context: 模板中的参数
    :return:
    """
    template = env_jinja.get_template(template_name)
    return await template.render_async(context)


async def send_email(email_to: str, subject: str = "", html_content: str = "") -> None:
    """
    发送邮件
    :param email_to: 目的地址
    :param subject: 主题
    :param html_content: 邮件内容
    :return:
    """
    message = EmailMessage()
    message["From"] = f"{env.SMTP_USER} <{env.SMTP_EMAIL}>"
    message["To"] = email_to
    message["Subject"] = subject
    message.set_content(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=env.SMTP_HOST,
            port=env.SMTP_PORT,
            start_tls=env.SMTP_TLS,
            use_tls=env.SMTP_SSL,
            username=env.SMTP_EMAIL,
            password=env.SMTP_PASSWORD,
        )
        logger.info(f"✅ Email sent successfully to {email_to}")
    except Exception as e:
        logger.error(f"❌ Failed to send email to {email_to}: {e}")
        raise
