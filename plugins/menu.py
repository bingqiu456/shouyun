from nonebot import on_command
from . import yiyan

a = on_command("兽云菜单")

@a.handle()
async def _():
    await a.finish(f"————兽云菜单————\n1.账号登录\n2.账号注册\n3.获取验证码\n4.获取登录令牌\n5.修改登录令牌\n—————————————\n{await yiyan.get_yiyan()}")