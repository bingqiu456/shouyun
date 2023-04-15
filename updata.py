import httpx
from nonebot.log import logger

mirr = "blog.bingyue.top"
# 更新源 cdn.bingyue.top

a = httpx.get(f"https://{mirr}/shouyun/1.json").json()
logger.success(f"正在为你下载最新版本:{a['ver']}")
logger.success("有bug请反馈 github.com/bingqiu456/shouyun")
for i in a["files"]:
    logger.warning(f"下载:{i}中....")
    b = httpx.get(f"https://{mirr}/shouyun/files/{i}").content
    with open(f"plugins/{i}","wb") as f:
        f.write(b)
        f.close()
    logger.success(f"下载{i}完成")

for i in a["db"]:
    logger.warning(f"下载:{i}中....")
    b = httpx.get(f"https://{mirr}/shouyun/data/{i}").content
    with open(f"data/{i}","wb") as f:
        f.write(b)
        f.close()
    logger.success(f"下载{i}完成")