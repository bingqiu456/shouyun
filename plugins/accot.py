### 账号注册
from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import GroupMessageEvent,PrivateMessageEvent,MessageSegment
from nonebot.params import ArgPlainText
from nonebot.log import logger
from . import config,image_check
import httpx

acc = on_fullmatch("账号注册")
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
