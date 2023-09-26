import utils.data as dataSource
from flow import doFlow

# 初始化
# load_path()


# 入口
def on_message(msg):
    dataSource.refreshUser()
    msg = msg.replace(".", "").replace("。", "")
    result = doFlow(msg)
    # 如果没有任何匹配的指令，则跳过
    if type(result) == bool:
        if not result:
            print("跳过拦截")
    return result


# TODO 定时备份到数据库 || init时同步检测数据更新


print(on_message(".r2d"))

