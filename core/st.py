import json
import time
import re
from ..sub.custom import reply
from ..em.msgCode import msgCode
from ..utils.calculate import operatorCal
from ..utils import cqUtil, eventUtil
from ..utils import data as dataSource
from ..core.aspect import log_recoder

helpDic = ["help", "帮助"]
showDic = ["show", "查看", "info"]
listDic = ["list", "列表"]
lockDic = ["lock", "锁定"]
unlockDic = ["unlock"]
removeDic = ["rm", "删除"]


@log_recoder
async def stFlow(msgStr, msgData):
    isLock = False
    userId = msgData.userId
    groupId = ""
    if msgData.groupId:
        groupId = msgData.groupId
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
        if re.search(r'([a-zA-Z\u4e00-\u9fff]+)(\d+)', msgStr):
            return await newCard(cardName, cardProp, msgData)
    # 按空格分隔，如第一个匹配二级指令 list show

    # 判断user所拥有的卡中是否存在msgStr的卡
    cardList = await dataSource.getUserItem(msgData.userId, "cardList")
    if msgStr in cardList:
        if isLock:
            return await reply(msgCode.CARD_LOCKED_BY_THIS_GROUP.name, msgData)
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
            return stHelp()
        if cmdSplit[0] in showDic:
            return await showCard(msgStr, msgData)
        if cmdSplit[0] in listDic:
            return await listCard(msgData)
        if cmdSplit[0] in lockDic:
            return await lockCard(msgData)
        if cmdSplit[0] in removeDic:
            return await removeCard(msgStr, msgData)
        if cmdSplit[0] in unlockDic:
            return await unlockCard(msgStr, msgData)
    else:
        return stHelp()

    # 是否存在 +-，且应存在角色卡，格式为 字符串[+-]数字
    m2 = re.match(r'^([\u4e00-\u9fa5a-zA-Z]+)(\d+)$', msgStr)
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
        "id": msgData.userId + "_" + str((int(time.time()) * 1000) // 1),
        "status": 0,  # 0正常 -1删除
        "locked": []
    }
    card = await splitProp(card, cardProp)
    await dataSource.createCharacter(card["id"], card)
    cardList = await dataSource.getUserItem(msgData.userId, "cardList")
    cardList[cardName] = card["id"]
    await dataSource.updateUserItem(msgData.userId, "cardList", cardList)
    # 切换全局卡为当前新卡
    await dataSource.updateUserItem(msgData.userId, "currentCard", card["id"])
    await dataSource.updateUserItem(msgData.userId, "currentCardName", card["name"])

    return await reply(msgCode.SAVE_CARD_SUCCESS.name, msgData, cardName)


async def updateCard(cardId, propName, operator, value, msgData):
    cardInfo = await dataSource.getCharacter(cardId)
    if propName not in cardInfo['prop']:
        # 如果不存在该属性，则新建一个属性
        if operator == "":
            cardInfo['prop'][propName] = value
            await dataSource.updateCharacterItem(cardId, prop, cardInfo['prop'])
            return await reply(msgCode.UPDATE_CARD_SUCCESS.name, msgData, propName)
        return await reply(msgCode.NOT_FOUND_CARD_PROP.name, msgData, cardInfo['name'], ext1=propName)
    oldPropValue = cardInfo['prop'][propName]
    if operator == "":
        propValue = int(value)
    else:
        propValue = await operatorCal(operator, int(oldPropValue), int(value))
    await dataSource.updateCharacterProp(cardId, propName, propValue)
    return await reply(msgCode.UPDATE_CARD_SUCCESS.name, msgData, propName)


async def remakeCard(cardName, cardId, cardProp, msgData):
    newProp = {}
    prop = await dataSource.getCharacter(cardId)["prop"]
    newProp = splitProp(newProp, cardProp)["prop"]
    for k, v in newProp.items():
        if k in prop:
            prop[k] = v
    await dataSource.updateCharacterItem(cardId, "prop", prop)
    return await reply(msgCode.UPDATE_CARD_SUCCESS.name, msgData, cardName)


async def switchCard(cardName, cardList, msgData):
    await dataSource.updateUserItem(msgData.userId, "currentCardName", cardName)
    await dataSource.updateUserItem(msgData.userId, "currentCard", cardList[cardName])
    return await reply(msgCode.SWITCH_CARD_SUCCESS.name, msgData, cardName)


async def showCard(msgStr, msgData):
    show_pattern = r'\b({})\b'.format('|'.join(showDic))
    msgStr = re.sub(show_pattern, "", msgStr, count=1).strip()
    msgStr = msgStr.strip()
    cardInfo = await dataSource.getCurrentCharacter(msgData.userId, msgData.groupId)
    result = json.dumps(cardInfo, indent=4, ensure_ascii=False)
    # 如果为查看某个属性，查询是否存在该属性
    if not msgStr == "":
        if msgStr not in cardInfo['prop']:
            cardInfo['prop'][msgStr] = 0
        result = f"{msgStr}：{cardInfo['prop'][msgStr]}"
    return await reply(msgCode.SHOW_CARD_INFO.name, msgData, result, cardInfo['name'])


async def listCard(msgData):
    cardList = await dataSource.getUserItem(msgData.userId, 'cardList')
    index = 1
    result = ""
    for key in cardList:
        result += f"{index}. {key}"
        if index < len(cardList):
            result += "\n"
        index += 1
    return await reply(msgCode.SHOW_CARD_LIST.name, msgData, result)


async def removeCard(msgStr, msgData):
    """
    # 获取userInfo
    # 查找msgStr的card，不存在返回
    # 不能删除当前角色/不能删除有锁定群聊的角色
    # 从user中删除
    """
    pattern = r'\b({})\b'.format('|'.join(removeDic))
    msgStr = re.sub(pattern, "", msgStr, count=1).strip()
    msgStr = msgStr.strip()
    userId = msgData.userId
    pcname = await eventUtil.getPcName(userId)
    if pcname == msgStr:
        return await reply(msgCode.CARD_NOW_USED_SO_CANT_REMOVE.name, msgData)
    pcname = msgStr
    cardList = await dataSource.getUserItem(userId, "cardList")
    if pcname not in cardList:
        return await reply(msgCode.NOT_FOUND_CARD.name, msgData, result=pcname)
    cardId = cardList[pcname]
    cardInfo = await dataSource.getCharacter(cardId)
    locked = cardInfo['locked']
    if not locked == []:
        # 被某些群锁定了
        result = "[" + ",".join(locked) + "]"
        return await reply(msgCode.CARD_LOCKED_BY_OTHER_GROUP.name, msgData, pcname=pcname, result=result)
    # 从当前user中删除
    cardList.pop(pcname)
    await dataSource.updateUserItem(userId, 'cardList', cardList)
    await dataSource.updateCharacterItem(cardId, 'status', -1)
    return await reply(msgCode.ST_RM_SUCCESS.name, msgData, pcname=pcname)


async def lockCard(msgData):
    """
    # 获取当前角色卡，不存在返回
    # 如果在本群已经锁定，返回先解锁
    # 获取groupInfo/cardLock
    # 添加、保存
    """
    userId = msgData.userId
    groupId = msgData.groupId
    cardInfo = await dataSource.getCurrentCharacter(userId)
    if cardInfo == {}:
        return await reply(msgCode.NO_CARD.name, msgData)
    locked = await dataSource.getGroupItem(groupId, 'cardLock')
    if userId in locked:
        cardId = locked[userId]
        oldLocked = await dataSource.getCharacter(cardId)
        return await reply(msgCode.ST_IS_LOCKED.name, msgData, pcname=oldLocked['name'])
    locked[userId] = cardInfo['id']
    pcname = cardInfo['name']
    # 保存到角色卡的locked
    cardLocked = cardInfo['locked']
    if groupId not in cardLocked:
        cardLocked.append(groupId)
    await dataSource.updateCharacterItem(cardInfo['id'], 'locked', cardLocked)
    await dataSource.updateGroupItem(msgData.groupId, 'cardLock', locked)
    return await reply(msgCode.ST_LOCK_SUCCESS.name, msgData, pcname=pcname)


async def unlockCard(msgStr, msgData):
    """
    # 检测是否为纯数字。如是则是远程解锁当前选择的角色卡
    # 包里没有角色卡返回
    # 尝试查找目标群聊，不存在返回，存在解锁
    # 非纯数字则解锁当前群
    """
    pattern = r'\b({})\b'.format('|'.join(unlockDic))
    msgStr = re.sub(pattern, "", msgStr, count=1).strip()
    userId = msgData.userId
    groupId = msgData.groupId
    if await dataSource.getCurrentCharacter(userId) == {}:
        return await reply(msgCode.NO_CARD.name, msgData)
    if msgStr.isdigit():
        groupId = msgStr
        groupLock = await dataSource.getGroupItem(groupId, 'cardLock')
        if groupLock == {}:
            return await reply(msgCode.ST_UNLOCK_TARGET_GROUP_NO_LOCK.name, msgData, ext1=groupId)
        cardId = groupLock[userId]
        groupLock.pop(userId)
        await unlockTargetGroup(cardId, groupId)
        await dataSource.updateGroupItem(groupId, 'cardLock', groupLock)
    else:
        groupLock = await dataSource.getGroupItem(groupId, 'cardLock')
        cardId = groupLock[userId]
        groupLock.pop(userId)
        await unlockTargetGroup(cardId, groupId)
        await dataSource.updateGroupItem(groupId, 'cardLock', groupLock)

    return await reply(msgCode.ST_UNLOCK.name, msgData)


async def unlockTargetGroup(cardId, groupId):
    """
    在目标角色卡中删除目标群聊的锁定信息（在角色卡信息中操作）
    """
    cardInfo = await dataSource.getCharacter(cardId)
    if "locked" not in cardInfo:
        locked = []
    else:
        locked = cardInfo['locked']
    if groupId in locked:
        locked.remove(groupId)
    await dataSource.updateCharacterItem(cardId, 'locked', locked)


def stHelp():
    resultMsg = (f"st 角色名 切卡，例如.st 林言\n"
                 f"st 角色名-属性属性值 录入/更新角色卡，例如.st 犬神香-hp7智力30魅力80\n"
                 f"st 属性+-值 当前卡属性调整，例如.st 智商+999\n"
                 f"st show (属性名) 查看角色卡详情/属性值，例如 .st show 炮术\n"
                 f"st list 查看角色卡列表\n"
                 f"st rm 删除角色卡\n"
                 f"st lock/unlock 锁定/解锁角色卡"
                 f"ps：在二级指令中help=帮助，show=info=查看，list=列表，lock=锁定，rm=删除")
    return resultMsg
