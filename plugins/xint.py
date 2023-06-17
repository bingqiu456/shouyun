# 心跳包
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot import on_command
from . import config,login,group_1



#@scheduler.scheduled_job('interval', seconds=config.time_login)
async def eveny_day():
    logger.warning("心跳:更新登录状态中")
    d = await login.login(k=1,b=config.token_p)
    if d:
        logger.success(f"更新登录状态成功...,已为你更新成功{config.ans}次")
        config.ans+=1
    else:
        logger.error("更新登录状态失败....")
if config.time_login_bool:
    logger.success("心跳包已开启")
    scheduler.add_job(eveny_day, "interval", seconds = config.time_login,id = "shouyun")
else:
    logger.success("心跳包未开启")
    
a = on_command("修改心跳包",rule=group_1.group_check,permission=SUPERUSER)
@a.handle()
async def _(v: Message = CommandArg()):
    try: d = int(str(v))
    except: await a.finish()
    config.time_login = d
    scheduler.remove_job(job_id="shouyun")
    scheduler.add_job(eveny_day, "interval", seconds = config.time_login,id="shouyun")
    await a.finish(f"修改心跳包成功,现在为{d}秒")
    