import asyncio
from ..core.rd import rdSplit, doRd
from ..sub.custom import reply
from ..utils import data as dataSource
from ..em.msgCode import msgCode
import nonebot
from nonebot.adapters.onebot.v11 import Bot


async def rh(msgStr, msgData, bot):
    if not msgData['msgType'] == 'group':
        return await reply(key=msgCode.RH_NOT_IN_GROUP.name, msgData=msgData)
    cardInfo = await dataSource.getCurrentCharacter(msgData['userId'], msgData['groupId'])
    if cardInfo:
        pcname = cardInfo['name']
    else:
        pcname = msgData['username']

    ext1 = f"{msgData['groupName']}({msgData['groupId']})"
    split = await rdSplit(msgStr, msgData)
    result = await doRd(split['a1'], split['a2'], split['b1'], split['b2'],
                        split['operator'], split['diceType'], split['extMsg'])
    await bot.send_group_msg(group_id=msgData['groupId'],
                             message=await reply(key=msgCode.RH_TO_GROUP.name, msgData=msgData, result=result,
                                                 pcname=pcname, ext1=ext1))
    await asyncio.sleep(2)
    await bot.send_private_msg(user_id=msgData['userId'],
                               message=await reply(key=msgCode.RH_TO_PRIVATE.name, msgData=msgData, result=result,
                                                   pcname=pcname, ext1=ext1))
    # print(await reply(key=msgCode.RH_TO_GROUP.name, msgData=msgData, result=result,
    #                   pcname=pcname, ext1=ext1))
    # print(await reply(key=msgCode.RH_TO_PRIVATE.name, msgData=msgData, result=result,
    #                   pcname=pcname, ext1=ext1))
    return True
