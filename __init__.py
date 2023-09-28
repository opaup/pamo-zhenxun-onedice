import utils.data as dataSource
from flow import doFlow

# 初始化
# load_path()


# 入口
def on_message(msg):
    msgData = {
        "msg": msg.replace(".", "").replace("。", ""),
        "username": "绪山美波里",
        "userId": "000000000",
        # "msgType": "private",
        "msgType": "group",
        "groupId": "114514",
        "groupName": "测试群",
    }
    result = doFlow(msgData)
    # 如果没有任何匹配的指令，则跳过
    if type(result) == bool:
        if not result:
            print("跳过拦截")
    return result


# TODO 定时备份到数据库 || init时同步检测数据更新

msgStr = ".sc2d3/3d4"
print(on_message(msgStr))

