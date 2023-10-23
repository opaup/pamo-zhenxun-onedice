# -*- coding:utf8 -*-
# @Author: opaup
from . import data as dataSource


async def getGroupName(groupId, bot):
    """
    通过groupId获取groupName
    """
    groupInfo = await bot.get_group_info(group_id=groupId)
    group_name = groupInfo['group_name']
    return group_name if group_name else "None"


async def getPcName(idStr="", msgData=None, bot=None, groupId=""):
    """
    获取user的pcname
    如未指定id，则默认为发送者的pcname(必须有msgData)
    如未指定group，则默认为消息来源group
    如未指定bot，则不存在角色卡时默认传回id
    """
    if idStr == "":
        if msgData is None:
            return ""
        idStr = msgData.userId
    if groupId == "":
        if msgData is None:
            groupId = ""
        else:
            groupId = msgData.groupId
    idStr = str(idStr)
    groupId = str(groupId)
    # 再判断一次
    if groupId == "":
        cardInfo = await dataSource.getCurrentCharacter(idStr, groupId)
    else:
        cardInfo = await dataSource.getCurrentCharacter(idStr)

    if not cardInfo == {}:
        pcname = cardInfo['name']
    else:
        if bot is None:
            pcname = idStr
        else:
            userInfo = await bot.get_stranger_info(user_id=int(idStr))
            pcname = userInfo['nickname']
    return pcname
