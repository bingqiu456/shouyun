from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from . import config,group_1
import httpx

a = on_command("图片下载",rule=group_1.group_check)

@a.handle()
async def _(b: Message = CommandArg()):
    b,d,f = str(b).split(),{"uid":"0","id":"1"},{0:"私密",1:"公开",2:"特定",3:"图片不存在"}
    if len(b) != 2 or b[0] not in d: await a.finish()
    c = httpx.post(f"https://cloud.foxtail.cn/api/function/pictures?picture={b[1]}&model={d[b[0]]}",cookies=config.cookies_login).json()
    if c["code"] != "20600": await a.finish("拉取图片失败！")
    await a.finish(f"查询模式:{b[0]}\nid:{b[1]}\n名字:{c['name']}\n留言:{c['suggest']}\n访问状态:{f[c['power']]}\n"+MessageSegment.image(httpx.get(c["url"]).content))