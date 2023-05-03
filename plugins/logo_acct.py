# 用户头像
from nonebot import on_fullmatch,on_command
from nonebot.adapters.onebot.v11 import MessageSegment,Message
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from . import config,group_1
import httpx

a = on_fullmatch("获取头像")
b = on_command("上传头像",permission=SUPERUSER,rule=group_1.group_check)

@a.handle()
async def _():
    await a.finish(f"用户{config.account}\n"+MessageSegment.image(f"https://cloud.foxtail.cn/api/account/obtainhead?account={config.account}"))

@b.handle()
async def _(c: Message = CommandArg()):
    if not c: await b.finish()
    if c[0].type != "image": await b.finish

    conn_image_qq = httpx.get(url=c[0].data["url"]).content
    k = {'file': (f'logo.png',conn_image_qq, 'image/png')}
    updata_image = httpx.post(url="https://cloud.foxtail.cn/api/account/addhead",cookies=config.cookies_login,files=k).json()
    if updata_image["code"] == "11101": await b.finish("登录过期，请重新登录")
    elif updata_image["code"] == "10200": await b.finish("头像上传成功")
    logger.error("头像上传发生错误")
    await b.finish("头像上传发生错误")
