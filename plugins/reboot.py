from nonebot.permission import SUPERUSER
from nonebot import on_fullmatch
import os
from . import group_1

a = on_fullmatch("重启机器",rule=group_1.group_check)

@a.handle()
async def _():
    await a.send("正在结束进程....\n本重启会停用...")
    os.system("cd data && reboot.bat")

