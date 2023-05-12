## 令牌

from nonebot import on_command,on_fullmatch
from nonebot.params import CommandArg,ArgPlainText
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.permission import SUPERUSER
from . import group_1,config,image_check
from nonebot.log import logger
import httpx

a = on_command("启用令牌",rule=group_1.group_check,permission=SUPERUSER)
b = on_command("停用令牌",rule=group_1.group_check,permission=SUPERUSER)
c = on_command("令牌列表",rule=group_1.group_check,permission=SUPERUSER)
d = on_command("申请令牌",rule=group_1.group_check,permission=SUPERUSER)
qy_key = on_fullmatch("启用key模式",rule=group_1.group_check,permission=SUPERUSER)
e = on_command("修改令牌权限",rule=group_1.group_check,permission=SUPERUSER)

@e.handle()
async def _(a: Message = CommandArg()):
    d = str(a).split()
    if len(d) < 5: await e.finish()
    for i in range(1,len(d)):
        if not d[i].isdigit(): await e.finish()
    t = httpx.post("https://cloud.foxtail.cn/api/account/token/power",data={
        "upload":d[1],
        "download":d[2],
        "modify":d[3],
        "delete":d[4],
        "token":d[0]
    },cookies=config.cookies_login).json()
    if t["code"] != "03400": await e.finish(t["msg"])
    await e.finish(f"令牌:{d[0]}修改成功")

@qy_key.handle()
async def _():
    await qy_key.send(MessageSegment.image(await image_check.get_image()))
    await qy_key.send("请输入验证码")

@qy_key.got("key")
async def _(c: str = ArgPlainText("key")):
    if not c: await qy_key.finish()
    t = httpx.post("https://cloud.foxtail.cn/api/account/token/pattern",cookies=config.cookies_login,data={
        "password":config.password,
        "proving":c,
    }).json()
    if t["code"] == "03100": await qy_key.finish("启用key模式成功！")
    else: await qy_key.finish(t["msg"])

@a.handle()
async def _(v: Message = CommandArg()):
    v = str(v).strip()
    if not v: await a.finish()
    d = httpx.post("https://cloud.foxtail.cn/api/account/token/state",data={
        "token":v,
        "state":1
    },cookies=config.cookies_login).json()
    if d["code"] != "03300": await a.finish(d["msg"])
    else: await a.finish(f"启用令牌:{v} 成功")

@b.handle()
async def _(v: Message = CommandArg()):
    v = str(v).strip()
    if not v: await a.finish()
    d = httpx.post("https://cloud.foxtail.cn/api/account/token/state",data={
        "token":v,
        "state":0
    },cookies=config.cookies_login).json()
    if d["code"] != "03300": await a.finish(d["msg"])
    else: await a.finish(f"停用令牌:{v} 成功")

@c.handle()
async def _():
    f = httpx.post("https://cloud.foxtail.cn/api/account/token/list",cookies=config.cookies_login).json()
    d = ""
    for i in range(len(f['list'])):
        d+=f"{i+1}.{f['list'][i]['secret']}\n" 
    await c.send(f"一共查询到{len(f['list'])}个令牌\n"+ d + "详细请回复数字")

@c.got("key")
async def _(v: str = ArgPlainText("key")):
    f = httpx.post("https://cloud.foxtail.cn/api/account/token/list",cookies=config.cookies_login).json()
    if not v.isdigit(): await c.finish()
    v,t = int(v),{"1":"开","0":"关"}
    if v > len(f['list']): await c.finish()
    await c.finish(f"令牌名字:{f['list'][v-1]['secret']}\n目前状态:{t[f['list'][v-1]['state']]}\n上传权限:{t[f['list'][v-1]['modify_upload']]}\n下载权限:{t[f['list'][v-1]['modify_download']]}\n修改权限:{t[f['list'][v-1]['modify_modify']]}\n删除权限:{t[f['list'][v-1]['modify_delete']]}")


@d.handle()
async def _(v:Message = CommandArg()):
    v = str(v).strip()
    global key
    key = v
    if not v: await d.finish()
    await d.send("请发送验证码上的文字")
    await d.send(MessageSegment.image(await image_check.get_image()))

@d.got("key")
async def _(a: str = ArgPlainText("key")):
    e = httpx.post("https://cloud.foxtail.cn/api/account/token/claim",data={
        "key":key,
        "proving":a,
    },cookies=config.cookies_login).json()
    if e["code"] != "03000": await d.finish(f"申请失败，原因:{e['msg']}")
    config.conn_lp.cursor().execute(f'insert into `lp` (`lp`,`key`) values("{e["token"]}","{key}")')
    config.conn_lp.commit()
    logger.success(f"新令牌:{e['token']} key:{key}")
    await d.finish("申请令牌成功！")