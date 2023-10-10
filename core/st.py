import json
import time
import re
from sub.custom import reply
from em.msgCode import msgCode
from utils.calculate import operatorCal
import utils.data as dataSource
from utils import strUtil

helpDic = ["help", "帮助"]
showDic = ["show", "查看", "info"]
listDic = ["list", "列表"]
lockDic = ["lock", "锁定"]


async def stFlow(msgStr, msgData):
    isLock = False
    userId = msgData["userId"]
    groupId = ""
    if msgData["groupId"]:
        groupId = msgData["groupId"]
        cardLock = await dataSource.getGroupItem(groupId, "cardLock")
        for ids in cardLock:
            lockedUser = re.split("_", ids)
            if userId == lockedUser:
                isLock = True

    # 判断是否存在 + - * / ，可能为修改
    if "-" in msgStr:
        # 包含 - 为创建/修改
        cmds = msgStr.split("-")
        if not len(cmds) == 2:
            return await reply(msgCode.ILLEGAL_FORMAT.name, msgData)
        # 规定单卡昵称不应大于18字
        cardName = cmds[0].strip()
        cardProp = cmds[1].strip()
        if len(cardName) > 18:
            return await reply(msgCode.CARD_NAME_TOO_LONG.name, msgData)

        # 判断是否存在同名卡，如是则为更新卡
        cardList = await dataSource.getUserItem(userId, "cardList")
        if cardName in cardList:
            return await remakeCard(cardName, cardList[cardName], cardProp, msgData)
        return await newCard(cardName, cardProp, msgData)
    # 按空格分隔，如第一个匹配二级指令 list show

    # 判断user所拥有的卡中是否存在msgStr的卡
    cardList = await dataSource.getUserItem(msgData["userId"], "cardList")
    if msgStr in cardList:
        if isLock:
            return await reply(msgCode.CARD_IN_GROUP_LOCKED.name, msgData)
        return await switchCard(msgStr, cardList, msgData)

    # 读取当前环境下的卡，是否存在
    characterInfo = await dataSource.getCurrentCharacter(userId, groupId)
    if not characterInfo:
        if not isLock:
            return await reply(msgCode.NO_CARD.name, msgData)

    # 判断 二级指令
    cmdSplit = re.split(" ", msgStr)
    if len(cmdSplit) >= 1:
        if cmdSplit[0] in helpDic:
            return await stHelp()
        if cmdSplit[0] in showDic:
            return await showCard(msgStr, msgData)
        if cmdSplit[0] in listDic:
            return await listCard(msgData)
    else:
        return await stHelp()

    # 是否存在 +-，且应存在角色卡，格式为 字符串[+-]数字
    m2 = re.match(r'^([\u4e00-\u9fa5]+)(\d+)$', msgStr)
    if re.match(r'^(.+)[+-](\d+)$', msgStr) or m2:
        # TODO 如果是锁定卡则更新锁定卡
        operator = ""
        if re.search("[+]", msgStr):
            operator = "+"
        if re.search("-", msgStr):
            operator = "-"
        if operator == "":
            s = [m2.group(1), m2.group(2)]
        else:
            s = msgStr.split(operator)
        return await updateCard(characterInfo['id'], s[0], operator, s[1], msgData)

    return await reply(msgCode.NO_COMMAND.name, msgData)


async def splitProp(card, cardProp):
    # 拆分属性键值对放在字典中
    regex = "(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)"
    parts = re.split(regex, cardProp)
    keyValueMap = {}
    for i in range(0, len(parts) - 1, 2):
        key = parts[i]
        value = int(parts[i + 1])
        keyValueMap[key] = value

    card["prop"] = keyValueMap
    return card


async def newCard(cardName, cardProp, msgData):
    card = {
        "name": cardName,
        "id": msgData["userId"] + "_" + str((int(time.time()) * 1000) // 1)
    }
    card = splitProp(card, cardProp)
    await dataSource.createCharacter(card["id"], card)
    cardList = dataSource.getUserItem(msgData["userId"], "cardList")
    cardList[cardName] = card["id"]
    await dataSource.saveUserItem(msgData["userId"], "cardList", cardList)
    # 切换全局卡为当前新卡
    await dataSource.saveUserItem(msgData["userId"], "currentCard", card["name"])

    return await reply(msgCode.SAVE_CARD_SUCCESS.name, msgData, cardName)


async def updateCard(cardId, propName, operator, value, msgData):
    cardInfo = await dataSource.getCharacter(cardId)
    if propName not in cardInfo['prop']:
        return await reply(msgCode.NOT_FOUND_CARD_PROP.name, msgData, cardInfo['name'], ext1=propName)
    oldPropValue = cardInfo['prop'][propName]
    if operator == "":
        propValue = int(value)
    else:
        propValue = await operatorCal(operator, int(oldPropValue), int(value))
    await dataSource.updateMultiCharacterProp(cardId, propName, propValue)
    return await reply(msgCode.UPDATE_CARD_SUCCESS.name, msgData, propName)


async def remakeCard(cardName, cardId, cardProp, msgData):
    newProp = {}
    prop = dataSource.getCharacter(cardId)["prop"]
    newProp = splitProp(newProp, cardProp)["prop"]
    for k, v in newProp.items():
        if k in prop:
            prop[k] = v
    await dataSource.saveCharacterItem(cardId, "prop", prop)
    return await reply(msgCode.UPDATE_CARD_SUCCESS.name, msgData, cardName)


async def switchCard(cardName, cardList, msgData):
    await dataSource.saveUserItem(msgData["userId"], "currentCardName", cardName)
    await dataSource.saveUserItem(msgData["userId"], "currentCard", cardList[cardName])
    return await reply(msgCode.SWITCH_CARD_SUCCESS.name, msgData, cardName)


async def showCard(msgStr, msgData):
    msgStr = await strUtil.replaceCmdByDic(msgStr, showDic)
    msgStr = msgStr.strip()
    cardInfo = await dataSource.getCurrentCharacter(msgData['userId'], msgData['groupId'])
    result = json.dumps(cardInfo, indent=4, ensure_ascii=False)
    # 如果为查看某个属性，查询是否存在该属性
    if not msgStr == "":
        if msgStr not in cardInfo['prop']:
            cardInfo['prop'][msgStr] = 0
        result = f"{msgStr}：{cardInfo['prop'][msgStr]}"
    return await reply(msgCode.SHOW_CARD_INFO.name, msgData, result, cardInfo['name'])


async def listCard(msgData):
    cardList = await dataSource.getUserItem(msgData['userId'], 'cardList')
    index = 1
    result = ""
    for key in cardList:
        result += f"{index}. {key}"
        if index < len(cardList):
            result += "\n"
        index += 1
    return result


async def stHelp():
    return
