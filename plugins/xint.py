# 心跳包
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
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

    