# 心跳包
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot import on_command
from . import config,login


@scheduler.scheduled_job('interval', seconds=config.time_login)
async def _():
    logger.warning("心跳:更新登录状态中")
    d = await login.login(k=1,b=config.token_p)
    if d:
        logger.success(f"更新登录状态成功...,已为你更新成功{config.ans}次")
        config.ans+=1
    else:
        logger.error("更新登录状态失败....")

a = on_command("修改心跳包")
@a.handle()
async def _(v: Message = CommandArg()):
    try: d = int(str(v))
    except: await a.finish()
    config.time_login = d
    await a.finish(f"修改心跳包成功,现在为{d}秒")
    