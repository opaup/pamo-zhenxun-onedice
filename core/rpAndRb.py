# coc/dnd 模式 dice set coc/ dice set dnd，默认coc
# coc ->diceType=100 +-d10 -> 两个roll(10)-1（一个十位一个个位）
# dnd -> d20*n
from sub.custom import reply
from em.msgCode import msgCode
from utils.calculate import operatorCal
import utils.dice as dice
import utils.data as dataSource
import re


# 惩罚
async def rp(msgStr, msgData):
    if msgStr == "" or not re.match(r'^\d$', msgStr):
        return await reply(key=msgCode.RP_OR_RB_FORMAT_FAIL.name, msgData=msgData)
    else:
        msgStr = int(msgStr)
    diceMode = await dataSource.getGroupItem(msgData["groupId"], "diceMode")
    if diceMode == "coc":
        return await cocRp(msgStr, msgData)
    if diceMode == "dnd":
        return await cocRb(msgStr, msgData)
    return


# 奖励
async def rb(msgStr, msgData):
    if msgStr == "" or not re.match(r'^\d$', msgStr):
        return
    else:
        msgStr = int(msgStr)
    diceMode = await dataSource.getGroupItem(msgData["groupId"], "diceMode")
    if diceMode == "coc":
        return await cocRb(msgStr, msgData)
    if diceMode == "dnd":
        return await cocRb(msgStr, msgData)
    return


async def cocRp(time, msgData):
    unit = await dice.roll(10)-1
    decade = 0
    allDecade = []
    for i in range(time):
        d = await dice.roll(10)-1
        allDecade.append(str(d))
        if d > decade:
            decade = d

    resultNum = str(decade) + str(unit)
    allDecade = ", ".join(allDecade)
    result = f"{resultNum}({allDecade})"
    return await reply(msgCode.RD_RESULT.name, msgData, result)


async def cocRb(time, msgData):
    unit = await dice.roll(10)-1
    decade = 9
    allDecade = []
    for i in range(time):
        d = await dice.roll(10)-1
        allDecade.append(str(d))
        if d < decade:
            decade = d

    resultNum = str(decade) + str(unit)
    allDecade = ", ".join(allDecade)
    result = f"{resultNum}({allDecade})"
    return await reply(msgCode.RD_RESULT.name, msgData, result)


async def dndRp(time, msgData):
    return


async def dndRb(time, msgData):
    return
