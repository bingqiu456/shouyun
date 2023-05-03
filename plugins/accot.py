### 账号注册 以及个人资料
from nonebot import on_fullmatch,on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Message,MessageSegment
from nonebot.params import ArgPlainText,CommandArg
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from . import config,image_check,group_1
import httpx

acc = on_fullmatch("账号注册",rule=group_1.group_check)
info = on_command("个人资料",rule=group_1.group_check)
xg_info = on_command("修改资料",permission=SUPERUSER,rule=group_1.group_check)

global tyu
tyu = []

@xg_info.handle()
async def _():
    tyu.clear()
    await xg_info.send("请输入修改的账号全称")

@xg_info.got("w")
async def _(a:str = ArgPlainText("w")):
    if not a: await xg_info.finish()
    tyu.append(a)
    await xg_info.send("请输入个性签名")

@xg_info.got("f")
async def _(a: str = ArgPlainText("f")):
    if not a: await xg_info.finish()
    tyu.append(a)
    await xg_info.send("输入你的qq号")

@xg_info.got("key")
async def _(a: str = ArgPlainText("key")):
    if not a: await xg_info.finish()
    tyu.append(int(a))
    k = httpx.post("https://cloud.foxtail.cn/api/account/modify",data={"name":tyu[0],"signature":tyu[1],"qq":str(tyu[2])},cookies=config.cookies_login)
    print(k)
    if a["code"] != "10500": await xg_info.finish(a["msg"])
    else: await xg_info.finish("修改个人信息已经完成")


@info.handle()
async def _(a: Message = CommandArg()):
    accto = config.account if not a else str(a)
    b = httpx.get(f"https://cloud.foxtail.cn/api/account/personal?account={accto}").json()
    if b["code"] != "10600": await info.finish(f"拉取个人资料{str(a)}失败....")
    else: await info.finish(f'查找用户:{accto}\n账号全称:{b["data"]["name"]}\n个性签名:{b["data"]["signature"]}\nQQ:{b["data"]["qq"]}')

global ans
ans = {}

@acc.handle()
async def _(event: GroupMessageEvent):
    ans[event.get_user_id()] = [0,0,0]
    logger.success(f"{event.get_user_id()},注册账号...")
    await acc.send("发送你注册的账号昵称")

@acc.got("k")
async def _(event: GroupMessageEvent, a: str = ArgPlainText("k")):
    if not a: await acc.finish()
    ans[event.get_user_id()][0] = a
    await acc.send("发送你的密码")

@acc.got("key")
async def _(event:GroupMessageEvent,a:str = ArgPlainText("key")):
    if not a: await acc.finish()
    ans[event.get_user_id()][1] = a
    await acc.send("发送你的邮箱")

@acc.got("keyy")
async def _(event:GroupMessageEvent,a:str = ArgPlainText("keyy")):
    if not a: await acc.finish()
    ans[event.get_user_id()][2] = a
    await acc.send("请输入图片验证码,如果取消可以直接回复空")
    await acc.send(MessageSegment.image(await image_check.get_image()))

@acc.got("ww")
async def _(event:GroupMessageEvent,a:str = ArgPlainText("ww")):
    await acc.send(await acct(ans[event.get_user_id()],a))
    ans.pop(event.get_user_id())
    await acc.finish()

async def acct(a:list,b:str):
    c = httpx.post("https://cloud.foxtail.cn/api/account/register",data={
        "account":a[0],
        "password":a[1],
        "mailbox":a[2],
        "proving":b
    },cookies=config.image_check)
    d = c.json()
    logger.warning("账号注册已提交申请....")
    if(d["code"]=="10100"):
        return f"账号注册成功\n账号名字:{a[0]}\n账号密码:{a[1]}\n邮箱:{a[2]}"
    else:
        return f"注册失败,{d['msg']}"
