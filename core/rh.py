import nonebot.adapters.onebot.v11.bot as bot
from core.rd import rdSplit, doRd
from sub.custom import reply
import utils.data as dataSource
from em.msgCode import msgCode


async def rh(msgStr, msgData):
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
    # await bot.Bot.send_msg(message_type='group', group_id=msgData['groupId'],
    #                        message=reply(key=msgCode.RH_TO_GROUP.name, msgData=msgData, result=result,
    #                                      pcname=pcname, ext1=ext1))

    # await bot.Bot.send_msg(message_type='private', user_id=msgData['userId'],
    #                        message=reply(key=msgCode.RH_TO_PRIVATE.name, msgData=msgData, result=result,
    #                                      pcname=pcname, ext1=ext1))
    print(await reply(key=msgCode.RH_TO_GROUP.name, msgData=msgData, result=result,
                      pcname=pcname, ext1=ext1))
    print(await reply(key=msgCode.RH_TO_PRIVATE.name, msgData=msgData, result=result,
                      pcname=pcname, ext1=ext1))
    return True
