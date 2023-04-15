## 账号登录
from nonebot import on_fullmatch
from . import config,image_check
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot.params import ArgPlainText
import httpx

a = on_fullmatch("账号登录",permission=SUPERUSER)

@a.handle()
async def _():
    await a.send(f"亲爱的:{config.account},正在登录....")
    logger.warning("正在登录....")
    if config.token_p:
        logger.success("正在尝试登录令牌登录....")
        d = await login(k=1,b=config.token_p)
        if d == True:
            await a.finish("登录成功")
        else: logger.error("令牌登录失败")
    await a.send("尝试验证码登录")
    await a.send(MessageSegment.image(await image_check.get_image()))
    
@a.got("key")
async def _(b: str = ArgPlainText("key")):
    if not b: await a.finish()
    logger.success("正在登录")
    if await login(0,b): await a.finish("登录成功")
    await a.finish("失败")
    

async def login(k,b):
    b = httpx.post("https://cloud.foxtail.cn/api/account/login",data={
        "account":config.account,
        "password":config.password,
        "model":k,
        "proving":b,
        "token":b
    },cookies=config.image_check)
    k = b.cookies
    d = b.json()
    if d["code"] == "10000":
        config.cookies_login = {"PHPSESSID":k["PHPSESSID"],"Token":k["Token"],"User":k["User"]} # 更新登录cookie
        config.conn_cookie.cursor().execute(f'UPDATE `login` SET `PHPSESSID` = "{k["PHPSESSID"]}"')
        config.conn_cookie.cursor().execute(f'UPDATE `login` SET `Token` = "{k["Token"]}"')
        config.conn_cookie.cursor().execute(f'UPDATE `login` SET `User` = "{k["User"]}"')
        config.conn_cookie.commit()
        logger.success("更新登录cookie")
        return True
    else: return False