## 图片验证码
from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import MessageSegment
from . import config
import httpx

a = on_fullmatch("获取图片验证码")

@a.handle()
async def _():
    await a.send("以下为你的验证码")
    await a.finish(MessageSegment.image(await get_image()))

async def get_image():
    # 获取图片的验证码
    a = httpx.get("https://cloud.foxtail.cn/api/check")
    config.image_check["PHPSESSID"] = a.cookies["PHPSESSID"]
    return a.content