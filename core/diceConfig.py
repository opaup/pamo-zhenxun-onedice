# 更改房规
# 定义格式： group 字段名 value -> 椒盐value
# dice on/off
# dice set value
# dice isNotice on/off
# dice mode coc/dnd/其他
# dice rule x
import re
from sub.custom import reply
from em.msgCode import msgCode
from utils.calculate import operatorCal
import utils.data as dataSource


async def diceFlow(msgStr, msgData):
    # isAdmin
    split = re.split(" ", msgStr)
    if len(split) <= 0:
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)
    cmd = split[0]
    if cmd == "on" or cmd == "off":
        return await onOff(msgStr, msgData)
    if cmd == "set":
        msgStr = re.sub("set", "", msgStr, count=1).strip()
        return await setDiceType(msgStr, msgData)
    if cmd == "isNotice":
        msgStr = re.sub("isNotice", "", msgStr, count=1).strip()
        return await setIsNotice(msgStr, msgData)
    if cmd == "mode":
        msgStr = re.sub("mode", "", msgStr, count=1).strip()
        return await setMode(msgStr, msgData)
    if cmd == "rule":
        msgStr = re.sub("rule", "", msgStr, count=1).strip()
        return await setRule(msgStr, msgData)
    if cmd == "help":
        msgStr = re.sub("help", "", msgStr, count=1).strip()
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)

    return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)


async def onOff(msgStr, msgData):
    if msgStr == "on":
        await dataSource.updateGroupItem(msgData['groupId'], 'onOff', msgStr)
        return await reply(key=msgCode.DICE_SET_ON.name, msgData=msgData)
    if msgStr == "off":
        await dataSource.updateGroupItem(msgData['groupId'], 'onOff', msgStr)
        return await reply(key=msgCode.DICE_SET_OFF.name, msgData=msgData)
    return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)


async def setDiceType(msgStr, msgData):
    if not msgStr.isdigit():
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)
    await dataSource.updateGroupItem(msgData['groupId'], 'diceType', msgStr)
    result = msgStr
    return await reply(key=msgCode.DICE_SET_DICETYPE.name, msgData=msgData, result=result)


async def setIsNotice(msgStr, msgData):
    if msgStr == "on":
        await dataSource.updateGroupItem(msgData['groupId'], 'isNotice', msgStr)
        return await reply(key=msgCode.DICE_SET_ISNOTICE_ON.name, msgData=msgData)
    if msgStr == "off":
        await dataSource.updateGroupItem(msgData['groupId'], 'isNotice', msgStr)
        return await reply(key=msgCode.DICE_SET_ISNOTICE_OFF.name, msgData=msgData)
    return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)


async def setMode(msgStr, msgData):
    diceMode = ["coc"]
    if msgStr not in diceMode:
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)
    await dataSource.updateGroupItem(msgData['groupId'], 'diceMode', msgStr)
    result = msgStr
    return await reply(key=msgCode.DICE_SET_DICETYPE.name, msgData=msgData, result=result)


async def setRule(msgStr, msgData):
    if not type(msgStr) == int:
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)

    return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)


async def setSecret(msgStr, msgData):
    if msgStr == "on":
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)
    if msgStr == "off":
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)

    return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)
