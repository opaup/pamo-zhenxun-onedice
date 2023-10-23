import asyncio
from ..core.rd import rdSplit, doRd
from ..sub.custom import reply
from ..utils import data as dataSource
from ..em.msgCode import msgCode
import nonebot
from nonebot.adapters.onebot.v11 import Bot
from ..core.aspect import check_from_group, log_recoder


@check_from_group
async def rh(msgStr, msgData, bot):
    cardInfo = await dataSource.getCurrentCharacter(msgData.userId, msgData.groupId)
    if cardInfo:
        pcname = cardInfo['name']
    else:
        pcname = msgData.username

    ext1 = f"{msgData.groupName}({msgData.groupId})"
    split = await rdSplit(msgStr, msgData)
    result = await doRd(split['a1'], split['a2'], split['b1'], split['b2'],
                        split['operator'], split['diceType'], split['extMsg'])
    msgData.sender = "self"
    await sendGroup(msgStr, msgData, result, pcname, ext1, bot)
    await asyncio.sleep(2)
    await sendPrivate(msgStr, msgData, result, pcname, ext1, bot)
    # print(await reply(key=msgCode.RH_TO_GROUP.name, msgData=msgData, result=result,
    #                   pcname=pcname, ext1=ext1))
    # print(await reply(key=msgCode.RH_TO_PRIVATE.name, msgData=msgData, result=result,
    #                   pcname=pcname, ext1=ext1))
    return True


@log_recoder
async def sendGroup(msgStr, msgData, result, pcname, ext1, bot):
    resultMsg = await reply(key=msgCode.RH_TO_GROUP.name, msgData=msgData, result=result,
                            pcname=pcname, ext1=ext1)
    await bot.send_group_msg(group_id=msgData.groupId,
                             message=resultMsg)
    return resultMsg


@log_recoder
async def sendPrivate(msgStr, msgData, result, pcname, ext1, bot):
    resultMsg = await reply(key=msgCode.RH_TO_PRIVATE.name, msgData=msgData, result=result,
                            pcname=pcname, ext1=ext1)
    await bot.send_private_msg(user_id=msgData.userId,
                               message=resultMsg)
    return resultMsg
