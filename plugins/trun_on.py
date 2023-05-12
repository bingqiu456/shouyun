from nonebot.log import logger
import httpx

verison = "1.0" # 版本信息
mirr = "cdn.bingyue.top" # 更新源
# 另外的更新源 blog.bingyue.top

logger.success("兽云nonebot2 插件启动成功")
logger.success(f"当前版本为{verison} 正式版")
logger.success("如有问题可以来https://github.com/bingqiu456/shouyun 来反馈")
logger.warning("正在检查更新，请勿退出")

a = httpx.get(url=f"https://{mirr}/shouyun/1.json").json()
if a["ver"] == verison:
    logger.success("暂无新版本更新")
else:
    logger.warning(f"检测到新版本:{a['ver']}\n更新日志\n{a['log']}")

logger.success(" ╰(*°▽*)╯ 祝你使用愉快")
