import utils.data as dataSource
from flow import doFlow
import asyncio

# 初始化
# load_path()


# 入口
async def on_message(msg):
    msgData = {
        "msg": msg.replace(".", "").replace("。", ""),
        "username": "绪山美波里",
        "userId": "000000000",
        # "msgType": "private",
        "msgType": "group",
        "groupId": "114514",
        "groupName": "测试群",
        "isAdmin": False,
    }
    result = await doFlow(msgData)
    # 如果没有任何匹配的指令，则跳过
    if type(result) == bool:
        if not result:
            print("跳过拦截")
    return result


# TODO 定时备份到数据库 || init时同步检测数据更新

msgStr = ".st list"
print(asyncio.run(on_message(msgStr)))
