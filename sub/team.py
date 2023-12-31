# -*- coding:utf8 -*-
# @Author: opaup
import re
from ..core.rd import rdSplit, doRd
from ..core.st import unlockTargetGroup
from ..sub.custom import reply
from ..utils import data as dataSource
from ..utils import cqUtil, eventUtil
from ..em.msgCode import msgCode
from ..core.aspect import team_operator_error, check_from_group


# @team_operator_error
@check_from_group
async def teamFlow(msgStr, msgData, bot):
    # 检测是否在群聊中

    listDic = ["list", "列表"]
    addDic = ["add"]
    clrDic = ["clr", "clear", "cls", "清空", "解散"]
    showDic = ["show"]
    rmDic = ["rm", "del", "delete"]
    callDic = ["call"]
    lockDic = ["lock"]
    unlockDic = ["unlock"]
    helpDic = ["help", "帮助"]
    if msgStr == "":
        return await teamList(msgData, bot)
    cmdSplit = re.split(" ", msgStr)
    cmd = cmdSplit[0]
    if cmd in listDic:
        return await teamList(msgData, bot)
    if cmd in callDic:
        return await teamCall(msgData, bot)
    if cmd in addDic:
        msgStr = re.sub('|'.join(addDic), "", msgStr, 1).strip()
        return await teamAdd(msgStr, msgData, bot)
    if cmd in showDic:
        msgStr = re.sub('|'.join(showDic), "", msgStr, 1).strip()
        return await teamShow(msgStr, msgData, bot)
    if cmd in clrDic:
        return await teamClr(msgData, bot)
    if cmd in rmDic:
        msgStr = re.sub('|'.join(rmDic), "", msgStr, 1).strip()
        return await teamRm(msgStr, msgData, bot)
    if cmd in lockDic:
        msgStr = re.sub('|'.join(lockDic), "", msgStr, 1).strip()
        return await teamLock(msgStr, msgData, bot)
    if cmd in unlockDic:
        return await teamUnLock(msgData, bot)
    if cmd in helpDic:
        msgStr = re.sub('|'.join(helpDic), "", msgStr, 1).strip()
        return teamHelp(msgStr)
    # 如果为数字或起始终止符为[]
    if (re.match(r'^\d{2,}$', cmd)) or (len(cmd) >= 2 and cmd[0] == '[' and cmd[-1] == ']'):
        return await teamProp(msgStr, msgData, bot)

    return False


# team 查看团队列表
async def teamList(msgData, bot):
    groupInfo = await dataSource.getGroupInfo(msgData.groupId)
    # 应当显示属性和状态
    nowTeamList = groupInfo["teamList"]
    i = 0
    result = [' ']
    for idStr in nowTeamList:
        i += 1
        s = []
        cardInfo = await dataSource.getCurrentCharacter(idStr, msgData.groupId)
        pcname = await eventUtil.getPcName(idStr, msgData, bot)
        s.append(f"{str(i)}.{pcname}|{idStr}")
        if not cardInfo == {}:
            s2 = []
            s.append(f"(")
            prop = cardInfo['prop']
            if 'hp' in prop:
                hp = prop['hp']
                s2.append(f"hp:{str(hp)}")
            if 'mp' in prop:
                mp = prop['mp']
                s2.append(f"mp:{str(mp)}")
            if 'san' in prop:
                san = prop['san']
                s2.append(f"san:{str(san)}")
            s.append(", ".join(s2))
            s.append(")")
        result.append("".join(s))
    resultMsg = await reply(msgCode.TEAM_LIST.name, msgData, "\n".join(result))
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team show 查看团队成员属性
async def teamShow(msgStr, msgData, bot):
    userId = cqUtil.fromStrGetUserId(msgStr)
    cardInfo = await dataSource.getCurrentCharacter(userId, msgData.groupId)
    prop = cardInfo['prop']
    pcname = await eventUtil.getPcName(userId, msgData, bot)
    if cardInfo == "":
        return await reply(msgCode.TARGET_USER_NOT_HAVE_CARD.name, msgData, ext1=ext1)
    # 如果没有匹配到，返回全部属性
    propName = re.search(r']\s*(\D+)', msgStr)
    if propName:
        propName = propName.group(0).replace(']', '').strip()
        if propName not in prop:
            prop[propName] = 0
        result = f"{propName} : {prop[propName]}"
    else:
        s = []
        for propName, propValue in prop.items():
            s.append(f"{propName} : {propValue}")
        result = "\n".join(s)
    resultMsg = await reply(msgCode.TEAM_SHOW.name, msgData, result, pcname=pcname)
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team add @at|uid 添加到队伍
async def teamAdd(msgStr, msgData, bot):
    cqCodePattern = r'\[(.+?)\]'
    idPattern = r'\d+'
    willAddIds = []
    if re.search(cqCodePattern, msgStr):
        willAddIds = re.findall(cqCodePattern, msgStr)
    elif re.search(idPattern, msgStr):
        willAddIds = re.findall(idPattern, msgStr)
    result = " [" + "], [".join(willAddIds) + "] "
    # 获取当前成员列表，查看是否存在该用户
    groupList = await bot.get_group_member_list(group_id=msgData.groupId)
    # 为CQ码则解析CQ码再加入，如为ID则直接加入
    tempList = []
    for user in willAddIds:
        tempList.append(cqUtil.fromAtGetId(user))
    if not len(tempList) == 0:
        willAddIds = tempList
    userIdInGroupList = []
    for userInGroup in groupList:
        userIdInGroupList.append(str(userInGroup['user_id']))
    for user in willAddIds:
        if user not in userIdInGroupList:
            return await reply(msgCode.GROUP_NO_ONE.name, msgData)
    oldTeamList = await dataSource.getGroupItem(msgData.groupId, "teamList")
    # 如果已在team中，不重复加入
    for willAddId in willAddIds:
        if willAddId not in oldTeamList:
            oldTeamList.append(willAddId)
    await dataSource.updateGroupItem(msgData.groupId, "teamList", oldTeamList)
    resultMsg = await reply(msgCode.TEAM_ADD_SUCCESS.name, msgData, result)
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team clear/clr/cls 清空队伍
async def teamClr(msgData, bot):
    result = f"{msgData.groupName}({msgData.groupId})"
    resultMsg = await reply(msgCode.TEAM_CLR.name, msgData, result)
    await dataSource.updateGroupItem(msgData.groupId, "teamList", [])
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team rm/del @at|uid 从队伍删除
async def teamRm(msgStr, msgData, bot):
    # 获取当前成员列表，查看是否存在该用户，如不存在则移除
    cqCodePattern = r'\[(.+?)\]'
    idPattern = r'\d+'
    willRmIds = []
    if re.search(cqCodePattern, msgStr):
        willRmIds = re.findall(cqCodePattern, msgStr)
    elif re.search(idPattern, msgStr):
        willRmIds = re.findall(idPattern, msgStr)
    result = " [" + "], [".join(willRmIds) + "] "
    # 获取当前团队列表，查看是否存在该用户
    groupInfo = await dataSource.getGroupInfo(msgData.groupId)
    nowTeamList = groupInfo["teamList"]
    locked = groupInfo["cardLock"]
    # 为CQ码则解析CQ码再加入，如为ID则直接删除
    tempList = []
    for idStr in willRmIds:
        if idStr in locked:
            pcname = await eventUtil.getPcName(idStr, msgData, bot)
            ext1 = cqUtil.atSomebody(idStr)
            return await reply(msgCode.TEAM_IN_LOCK.name, msgData, pcname=pcname, ext1=ext1)
        tempList.append(cqUtil.fromAtGetId(idStr))
    if not len(tempList) == 0:
        willRmIds = tempList
    for idStr in willRmIds:
        if idStr not in nowTeamList:
            result = idStr
            return await reply(msgCode.TEAM_NO_ONE.name, msgData, result)
        nowTeamList.remove(idStr)

    resultMsg = await reply(msgCode.TEAM_RM_SUCCESS.name, msgData, result)
    await dataSource.updateGroupItem(msgData.groupId, "teamList", nowTeamList)
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team call 呼叫队伍全体成员
async def teamCall(msgData, bot):
    groupInfo = await dataSource.getGroupInfo(msgData.groupId)
    # 应当显示属性和状态
    nowTeamList = groupInfo["teamList"]
    i = 0
    result = []
    for idStr in nowTeamList:
        i += 1
        s = f"{str(i)}.{cqUtil.atSomebody(idStr)}"
        result.append(s)
    resultMsg = await reply(msgCode.TEAM_CALL.name, msgData, "\n".join(result))
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team @at|uid propvalue 调整成员卡属性
async def teamProp(msgStr, msgData, bot):
    userId = cqUtil.fromStrGetUserId(msgStr)
    cardInfo = await dataSource.getCurrentCharacter(userId, msgData.groupId)
    prop = cardInfo['prop']
    pcname = await eventUtil.getPcName(userId, msgData, bot)
    if cardInfo == "":
        return await reply(msgCode.TARGET_USER_NOT_HAVE_CARD.name, msgData, ext1=ext1)
    # 如果没有匹配到则为错误格式
    propName = re.search(r']\s*(\D+)', msgStr).group(0).replace(']', '').strip()
    adjust = re.search(r'\d+(?:[a-zA-Z]+)?$', msgStr).group(0).strip()
    if propName[-1] == '-':
        adjust = '-' + adjust
        propName = propName.replace('-', '')
    if propName not in prop:
        prop[propName] = 0
    propValue = prop[propName]
    oldValue = propValue
    propValue = int(propValue) - int(adjust)
    result = f"{str(oldValue)}-({adjust}) = {str(propValue)}"
    if propValue < 0:
        propValue = 0
    await dataSource.updateCharacterProp(cardInfo['id'], propName, propValue)
    resultMsg = await reply(msgCode.TEAM_PROP.name, msgData, result, pcname=pcname, ext1=propName)
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team lock 一键全体卡上锁
async def teamLock(msgStr, msgData, bot):
    """
    获取list
    获取对应cardInfo，如有人不存在card，则返回error
    写入cardLock
    """
    groupId = msgData.groupId
    groupInfo = await dataSource.getGroupInfo(groupId)
    locked = groupInfo['cardLock']
    team = groupInfo['teamList']
    flag = False
    ext1 = []
    for uid in team:
        cardInfo = await dataSource.getCurrentCharacter(uid)
        if cardInfo == {}:
            flag = True
            name = await eventUtil.getPcName(uid, msgData, bot)
            ext1.append(name)
        if flag:
            return await reply(msgCode.TARGET_USER_NOT_HAVE_CARD.name, msgData, ext1="、".join(ext1))
        locked[uid] = cardInfo['id']
        cardLocked = cardInfo['locked']
        if groupId not in cardLocked:
            cardLocked.append(groupId)
        await dataSource.updateCharacterItem(cardInfo['id'], 'locked', cardLocked)

    await dataSource.updateGroupItem(groupId, 'cardLock', locked)
    resultMsg = await reply(msgCode.TEAM_LOCK_SUCCESS.name, msgData)
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


# team unlock 一键全体卡解锁
async def teamUnLock(msgData, bot):
    groupId = msgData.groupId
    groupInfo = await dataSource.getGroupInfo(msgData.groupId)
    locked = groupInfo['cardLock']
    for uid, cardId in locked.items():
        await unlockTargetGroup(cardId, groupId)
    # 清空cardLock
    await dataSource.updateGroupItem(msgData.groupId, 'cardLock', {})
    resultMsg = await reply(msgCode.TEAM_UNLOCK_SUCCESS.name, msgData)
    await bot.send_msg(user_id=msgData.userId, group_id=msgData.groupId, message=resultMsg, auto_escape=False)
    return True


def teamHelp():
    resultMsg = (f"team (list) 查看当前小队列表，加不加list都一样\n"
                 f"team add 添加小队成员，例.team add [@蟹林言]\n"
                 f"team clear 清空小队\n"
                 f"team show (@成员+属性名) 查看小队成员的角色属性、没有指定成员和属性则是查看全部角色的属性，例.team show [@五仁月饼]血量"
                 f"team [@成员]属性名属性值 调整指定成员的属性，模型值默认为减去，如为负数则是增加，例.team [@帕沫]信用评级999\n"
                 f"team rm @成员 从小队中删除指定成员\n"
                 f"team call 一键呼叫小队成员\n"
                 f"team lock/unlock 一键锁定/解锁小队成员角色卡\n"
                 f"其中二级指令，list=列表，clr=clear=cls=清空=解散，rm=del=delete")
    return resultMsg
