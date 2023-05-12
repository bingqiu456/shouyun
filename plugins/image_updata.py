import httpx,aiofiles,ast
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent,Bot,MessageSegment
from nonebot.permission import SUPERUSER
from . import config,group_1

a = on_command("上传图片",rule=group_1.group_check)
b = on_command("同意审核",permission=SUPERUSER,rule=group_1.group_check)
c = on_command("拒绝审核",permission=SUPERUSER,rule=group_1.group_check)

async def cha_id(id):
    q = config.conn_shenhe.cursor().execute(f"SELECT * from `sh` WHERE id={id};").fetchone()
    if not q: return False
    else: return q[2]

@b.handle()
async def _(c: Message = CommandArg()):
    try: id = int(str(c).strip())
    except: await b.finish()
    d = await cha_id(id)
    if not d: await b.finish("此id不存在，或者已经被同意拒绝")
    else:
        z = ast.literal_eval(d)
        o = httpx.get(z[4]).content
        y = {"设定":"0","毛图":"1","插画":"2"} # 图片类型
        p = {"私密":"0","公开":"1","特定":"2"}
        e = await image_get(z[0],z[0],y[z[1]],o,z[2],p[z[3]])
        if e["code"] == "20000":
            config.conn_shenhe.cursor().execute(f"DELETE FROM `sh` WHERE id = {id};")
            config.conn_shenhe.commit()
            await b.finish(f"同意投稿成功\nuid:{e['picture']}\nsid:{e['id']}")
        else:
            await b.finish(e['msg'])

@c.handle()
async def _(d:Message = CommandArg()):
    try: id = int(str(d).strip())
    except: await c.finish()
    d = await cha_id(id)
    if not d: await c.finish("此id不存在，或者已经被同意拒绝")
    config.conn_shenhe.cursor().execute(f"DELETE FROM `sh` WHERE id = {id};")
    config.conn_shenhe.commit()
    await c.finish("拒绝审核成功！")


@a.handle()
async def _(bot:Bot,event: GroupMessageEvent,c: Message = CommandArg()):
    o = httpx.get(url=list(c)[-1].data["url"]).content # 获取图片链接
    url = list(c)[-1].data["url"]
    y = {"设定":"0","毛图":"1","插画":"2"} # 图片类型
    z = str(c).split()
    p = {"私密":"0","公开":"1","特定":"2"}
    if len(z) != 5: await a.finish()
    if await SUPERUSER(bot,event):
        d = await image_get(z[0],z[0],y[z[1]],o,z[2],p[z[3]])
        if d["code"] == "20000":
            await a.finish(f"投稿成功！！\nsid:{d['id']}\nuid:{d['picture']}")
        else:
            await a.finish(d['msg'])
    else:
        z[4] = url
        id = await id_add()
        config.conn_shenhe.cursor().execute(f'insert into `sh` (`id`,`qq`,`msg`) values({int(id)},{int(event.get_user_id())},"{str(z)}")')
        config.conn_shenhe.commit()
        await bot.call_api("send_group_msg",**{
            "group_id":config.admin.group_shenhe,
            "message":f"图片id:{id}\n图片名字:{z[0]}\n上传类型:{z[1]}\n留言内容:{z[2]}\n权限类型:{z[3]}\n图片:{MessageSegment.image(o)}\n发送 同意审核/拒绝审核{id}"
        })
        await a.finish(f"已成功发往审核群,审核id{id}")

async def id_add():
    async with aiofiles.open("data/id","r+",encoding="utf_8") as f:
        k = int(await f.read())+1
        await f.close()
    async with aiofiles.open("data/id","w+",encoding="utf_8") as b:
        await b.write(str(k))
        await b.close()
    return k

async def image_get(qq,name,power,url,su,po):
    data={}
    data["name"]=name
    data["suggest"] = su
    data["type"]=str(power)
    data["power"]=str(po)
    files ={'file': (f'foxLS{qq}{name}.png',url, 'image/png')}
    res = httpx.post(url="https://cloud.foxtail.cn/api/function/upload",data=data,files=files,cookies=config.cookies_login).json()
    return res