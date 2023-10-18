# -*- coding:utf8 -*-
# @Author: opaup
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message, MessageEvent
from . import data as dataSource

async def getGroupName(groupId, bot):
    """
    通过groupId获取groupName
    """
    groupInfo = await bot.get_group_info(group_id=groupId)
    group_name = groupInfo['group_name']
    return group_name if group_name else "None"


async def getPcName(idStr="", msgData=None, bot=None):
    """
    获取user的pcname
    如未指定id，则默认为发送者的pcname
    如未指定bot，则不存在角色卡时默认传回id
    """
    if idStr == "":
        idStr = msgData['userId']
    cardInfo = await dataSource.getCurrentCharacter(idStr, msgData['groupId'])
    if not cardInfo == {}:
        pcname = cardInfo['name']
    else:
        if bot is not None:
            userInfo = await bot.get_stranger_info(user_id=int(idStr))
            pcname = userInfo['nickname']
        else:
            pcname = idStr
    return pcname
