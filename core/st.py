import json
from sub.custom import reply
from em.msgCode import msgCode
import utils.data as dataSource


def stFlow(cmdStr, userId, groupId):
    isPrivate = False
    groupInfo = {}
    if groupId == "":
        isPrivate = True
    else:
        groupInfo = dataSource.getGroupInfo(groupId)
    characterInfo = dataSource.getCurrentCharacter(userId, groupId)

    if "-" in cmdStr:
        # 包含 - 为创建
        # 规定单卡昵称不应大于18字

        return
    # 按空格分隔，如第一个匹配二级指令 list show

    # 判断user所拥有的卡中是否存在cmdStr的卡

    return reply(msgCode.NO_ACHIEVE_CMD.name)
