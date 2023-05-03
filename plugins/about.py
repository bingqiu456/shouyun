from nonebot import on_fullmatch
from . import group_1,trun_on
import asyncio,httpx
from nonebot.permission import SUPERUSER

a = on_fullmatch("检查更新",rule=group_1.group_check)
b = on_fullmatch("关于作者",rule=group_1.group_check)

@a.handle()
async def _():
    await a.send("正在检查更新...")
    await asyncio.sleep(2)
    v = httpx.get("https://cdn.bingyue.top/shouyun/1.json").json()
    if v["ver"] == trun_on.verison:
        await a.finish(f"当前版本为:{trun_on.verison}\n已经是最新版本")
    else:
        await a.finish(f"当前版本:{trun_on.verison}\n最新版:{v['ver']}\n更新内容:\n{v['log']}\n请手动到updata更新")

@b.handle()
async def _():
    await b.finish("作者qq:35***19417\n本项目为兽云&nonebot2\n作者博客:blog.bingyue.top")