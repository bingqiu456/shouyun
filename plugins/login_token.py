## 登录令牌查询
from nonebot import on_fullmatch
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from . import config
import httpx

a = on_fullmatch("获取登录令牌",permission=SUPERUSER)
b = on_fullmatch("修改登录令牌",permission=SUPERUSER)

async def login_t(url):
    b = httpx.get(url,cookies=config.cookies_login)
    c = b.json()
    if c["code"] == "11101":
        config.cookies_login = {} # 清除cookie
        logger.error("cookie错误 请重新登录")
        return "登录失效，请重新登录"
    elif c["code"] == "12101":
        return "未申请令牌...."
    else:
        config.conn_login_token.cursor().execute(f'UPDATE `Token` SET `login_token` = "{c["token"]}"')
        config.conn_login_token.commit()
        logger.success(f"令牌目前为:{c['token']}")
        config.token_p = c["token"]
        return "获取(更新)令牌成功 已写入缓存"

@a.handle()
async def _():
    await a.finish(await login_t("https://cloud.foxtail.cn/api/account/tkquery"))

@b.handle()
async def _():
    await b.finish(await login_t("https://cloud.foxtail.cn/api/account/tkapply"))