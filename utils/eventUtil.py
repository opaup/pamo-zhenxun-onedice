# -*- coding:utf8 -*-
# @Author: opaup
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message, MessageEvent


async def getGroupName(groupId, bot):
    """
    通过groupId获取groupName
    """
    groupInfo = await bot.get_group_info(group_id=groupId)
    group_name = groupInfo['group_name']
    return group_name if group_name else "None"
