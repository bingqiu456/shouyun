from nonebot import on_command,on_fullmatch
from . import yiyan,group_1

a = on_fullmatch("兽云菜单",rule=group_1.group_check)
b = on_fullmatch("账号功能",rule=group_1.group_check)
c = on_fullmatch("功能操作",rule=group_1.group_check)
d = on_fullmatch("令牌功能",rule=group_1.group_check)
e = on_fullmatch("系统设置",rule=group_1.group_check)

@a.handle()
async def _():
    await a.finish(f"————兽云菜单————\n1.账号功能\n2.功能操作\n3.令牌功能\n4.系统设置\n—————————————\n{await yiyan.get_yiyan()}")

@b.handle()
async def _():
    await b.finish(f"————账号功能————\n1.账号登录\n2.账号注册\n3.获取验证码\n4.获取头像\n5.上传头像+图片\n6.个人资料+名字\n7.修改资料\n—————————————\n{await yiyan.get_yiyan()}")

@c.handle()
async def _():
    await c.finish(f"————功能操作————\n1.随机图片+名字+类型\n2.图片下载 uid/id xx\n—————————————\n{await yiyan.get_yiyan()}")

@d.handle()
async def _():
    await d.finish(f"————令牌功能————\n1.获取登录令牌\n2.修改登录令牌\n3.启用令牌\n4.停用令牌\n5.令牌列表\n6.申请令牌[key]\n7.启用key模式\n—————————————\n{await yiyan.get_yiyan()}")

@e.handle()
async def _():
    await e.finish(f"————系统设置————\n1.群[开/关] [群号]\n2.修改心跳包[秒数]\n3.检查更新\n4.关于作者\n—————————————\n{await yiyan.get_yiyan()}")