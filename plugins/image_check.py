## 图片验证码
from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import MessageSegment
from . import config,group_1
import httpx

a = on_fullmatch("获取图片验证码",rule=group_1.group_check)

@a.handle()
async def _():
    await a.send("以下为你的验证码")
    await a.finish(MessageSegment.image(await get_image()))

async def get_image():
    # 获取图片的验证码
    a = httpx.get("https://cloud.foxtail.cn/api/check",cookies=config.cookies_login)
    if not config.cookies_login:
        config.cookies_login["PHPSESSID"] = a.cookies["PHPSESSID"]
    return a.content