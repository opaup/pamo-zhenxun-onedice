import json
import time
import re
from sub.custom import reply
from em.msgCode import msgCode
import utils.data as dataSource


def stFlow(msgStr, msgData):
    groupId = msgData["groupId"]
    userId = msgData["userId"]

    isLock = False
    groupInfo = {}
    if groupId == "":
        isLock = True
    else:
        groupInfo = dataSource.getGroupInfo(groupId)

    # 读取当前环境下的卡，是否存在
    characterInfo = dataSource.getCurrentCharacter(userId, groupId)

    # 判断是否存在 + - * / ，可能为修改

    if "-" in msgStr:
        # 包含 - 为创建/修改
        cmds = msgStr.split("-")
        if not len(cmds) == 2:
            return reply(msgCode.ILLEGAL_FORMAT.name, msgData)
        # 规定单卡昵称不应大于18字
        cardName = cmds[0].strip()
        cardProp = cmds[1].strip()
        if len(cardName) > 18:
            return reply(msgCode.CARD_NAME_TOO_LONG.name, msgData)

        # 判断是否存在同名卡，如是则为更新卡
        cardList = dataSource.getUserItem(userId, "cardList")
        if cardName in cardList:
            return updateCard(cardName, cardList[cardName], cardProp, msgData)
        return newCard(cardName, cardProp, msgData)
    # 按空格分隔，如第一个匹配二级指令 list show

    # 判断user所拥有的卡中是否存在msgStr的卡
    cardList = dataSource.getUserItem(msgData["userId"], "cardList")
    if msgStr in cardList:
        if isLock:
            return reply(msgCode.CARD_IN_GROUP_LOCKED.name, msgData)
        return switchCard(msgStr, cardList, msgData)

    if len(characterInfo) == 0:
        return reply(msgCode.NO_CARD.name, msgData)
    return reply(msgCode.NO_COMMAND.name, msgData)


def splitProp(card, cardProp):
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


def newCard(cardName, cardProp, msgData):
    card = {
        "name": cardName,
        "id": msgData["userId"] + "_" + str((int(time.time()) * 1000) // 1)
    }
    card = splitProp(card, cardProp)
    dataSource.createCharacter(card["id"], card)
    cardList = dataSource.getUserItem(msgData["userId"], "cardList")
    cardList[cardName] = card["id"]
    dataSource.saveUserItem(msgData["userId"], "cardList", cardList)
    # 切换全局卡为当前新卡
    dataSource.saveUserItem(msgData["userId"], "currentCard", card["name"])

    return reply(msgCode.SAVE_CARD_SUCCESS.name, msgData, cardName)


def updateCurrentCard():
    return


def updateCard(cardName, cardId, cardProp, msgData):
    newProp = {}
    prop = dataSource.getCharacter(cardId)["prop"]
    newProp = splitProp(newProp, cardProp)["prop"]
    for k, v in newProp.items():
        if k in prop:
            prop[k] = v
    dataSource.saveCharacterItem(cardId, "prop", prop)
    return reply(msgCode.UPDATE_CARD_SUCCESS.name, msgData, cardName)


def switchCard(cardName, cardList, msgData):
    dataSource.saveUserItem(msgData["userId"], "currentCardName", cardName)
    dataSource.saveUserItem(msgData["userId"], "currentCard", cardList[cardName])
    return reply(msgCode.SWITCH_CARD_SUCCESS.name, msgData, cardName)


def showCard():
    return


def listCard():
    return
