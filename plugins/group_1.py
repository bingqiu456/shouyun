from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent
from nonebot.log import logger
from nonebot.params import CommandArg
from . import config

a = on_command("群开机")
@a.handle()
async def _(event:GroupMessageEvent,v: Message = CommandArg()):
    try: group = int(str(v).strip())
    except: group = event.group_id
    if await turn_group(group):
        await a.finish(f"本群{group}开启成功")
    else:
        await a.finish(f"本群已经开启了{group}")

b = on_command("群关机")
@b.handle()
async def _(event:GroupMessageEvent,v: Message = CommandArg()):
    try: group = int(str(v).strip())
    except: group = event.group_id
    if await off_group(group): await b.finish(f"关闭本群{group}成功")
    else: await b.finish(f"本群已经关闭了{group}")

async def group_check(event: GroupMessageEvent):
    return event.group_id in config.group_tf

async def turn_group(id):
    if id in config.group_tf:
        logger.warning(f"该群{id}已开启")
        return False
    config.conn_group_tf.cursor().execute(f"insert into `group` (`group`) values({id})")
    config.conn_group_tf.commit()
    config.group_tf.append(id)
    logger.success(f"本群开启成功{id}")
    return True

async def off_group(id):
    if id not in config.group_tf:
        logger.error(f"该群{id}不存在！")
        return False
    config.conn_group_tf.cursor().execute(f"DELETE FROM `group` WHERE `group` = {id}")
    config.conn_group_tf.commit()
    config.group_tf.remove(id)
    logger.success(f"关闭本群成功{id}")
    return True