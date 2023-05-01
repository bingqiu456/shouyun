# 随机图片
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.log import logger
from . import config
import httpx

a = on_command("随机图片")

@a.handle()
async def _(b: Message = CommandArg()):
    b,lx = str(b).split(),{"设定":"0","毛图":"1","插画":"2"}

    if len(b) < 2: await a.finish()
    if b[1] not in lx: await a.finish()

    c = httpx.get(f"https://cloud.foxtail.cn/api/function/random?name={b[0]}&type={b[1]}").json()
    if c["code"] != "20900": await a.finish("图片拉取失败")
    else: await a.finish(f'发图人:{c["picture"]["account"]}\n名字:{c["picture"]["name"]}\nid:{c["picture"]["id"]}\nuid:{c["picture"]["picture"]}\n上传时间:{c["picture"]["time"]}'+MessageSegment.image(await get_image(c["picture"]["picture"])))

async def get_image(id):
    h =  httpx.get(url=f"https://cloud.foxtail.cn/api/function/pictures?picture={id}&model=0",cookies=config.cookies_login).json()
    if h["code"] == "20600": return h["url"]
    else:
        logger.error("图片拉取失败，疑似cookie失效")
        return "图片拉取失败！"