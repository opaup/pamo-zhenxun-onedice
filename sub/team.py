# -*- coding:utf8 -*-
# @Author: opaup
import re
from ..core.rd import rdSplit, doRd
from ..sub.custom import reply
from ..utils import data as dataSource
from ..utils import cqUtil
from ..em.msgCode import msgCode
from ..core.aspect import team_operator_error, check_from_group, check_from_admin


# @team_operator_error
@check_from_group
async def teamFlow(msgStr, msgData, bot):
    # 检测是否在群聊中

    listDic = ["list", "列表"]
    addDic = ["add"]
    clrDic = ["clr", "clear", "cls"]
    showDic = ["show"]
    rmDic = ["rm", "del"]
    callDic = ["call"]
    lockDic = ["lock"]
    if msgStr == "":
        return await teamList(msgData, bot)
    cmdSplit = re.split(" ", msgStr)
    cmd = cmdSplit[0]
    if cmd in listDic:
        return await teamList(msgData, bot)
    if cmd in callDic:
        return await teamCall(msgData, bot)
    if cmd in addDic:
        msgStr = re.sub('|'.join(addDic), "", msgStr, 1).lstrip()
        return await teamAdd(msgStr, msgData, bot)
    if cmd in showDic:
        msgStr = re.sub('|'.join(showDic), "", msgStr, 1).lstrip()
        return await teamShow(msgStr, msgData, bot)
    if cmd in clrDic:
        msgStr = re.sub('|'.join(clrDic), "", msgStr, 1).lstrip()
        return await teamClr(msgStr, msgData, bot)
    if cmd in rmDic:
        msgStr = re.sub('|'.join(rmDic), "", msgStr, 1).lstrip()
        return await teamRm(msgStr, msgData, bot)
    if cmd in lockDic:
        msgStr = re.sub('|'.join(lockDic), "", msgStr, 1).lstrip()
        return await teamLock(msgStr, msgData, bot)
    # 如果为数字或起始终止符为[]
    if (re.match(r'^\d{2,}$', text)) or (len(text) >= 2 and text[0] == '[' and text[-1] == ']'):
        return await teamProp(msgStr, msgData, bot)

    return False


# team 查看团队列表
async def teamList(msgData, bot):
    groupInfo = await dataSource.getGroupInfo(msgData['groupId'])
    # 应当显示属性和状态
    nowTeamList = groupInfo["teamList"]
    i = 0
    result = []
    for idStr in nowTeamList:
        i += 1
        # s = f"{str(i)}.{cqUtil.atSomebody(idStr)}"
        # 是否锁定卡
        locked = groupInfo["cardLock"]
        if idStr in locked:
            cardInfo = await dataSource.getCharacter(locked[idStr])
        else:
            cardId = await dataSource.getUserItem(idStr, "currentCard")
            cardInfo = await dataSource.getCharacter(cardId)
        s = []
        if cardInfo == {}:
            userInfo = await bot.get_stranger_info(user_id=int(idStr))
            if userInfo:
                pcname = userInfo["nickname"]
            else:
                pcname = idStr
            s.append(f"{str(i)}.{pcname}")
        else:
            prop = cardInfo['prop']
            pcname = cardInfo['name']
            s.append(f"{str(i)}.{pcname}(")
            s2 = []
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
    await bot.send_msg(user_id=msgData["userId"], group_id=msgData["groupId"], message=resultMsg, auto_escape=False)
    return True


# team 查看团队列表
async def teamShow(msgStr, msgData, bot):
    return


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
    print(f"result = {result}")
    # 获取当前成员列表，查看是否存在该用户
    groupList = await bot.get_group_member_list(group_id=msgData['groupId'])
    # 为CQ码则解析CQ码再加入，如为ID则直接加入
    tempList = []
    for user in willAddIds:
        tempList.append(cqUtil.fromAtGetId(user))
    if not len(tempList) == 0:
        willAddIds = tempList
    userIdInGroupList = []
    for userInGroup in groupList:
        userIdInGroupList.append(str(userInGroup['user_id']))
    print(f"userIdInGroupList = {userIdInGroupList}")
    for user in willAddIds:
        if user not in userIdInGroupList:
            return await reply(msgCode.TEAM_NO_ONE.name, msgData)

    oldTeamList = await dataSource.getGroupItem(msgData['groupId'], "teamList")
    print(f"oldTeamList = {oldTeamList}")
    print(f"willAddIds={willAddIds}")
    # 如果已在team中，不重复加入
    for willAddId in willAddIds:
        if willAddId not in oldTeamList:
            oldTeamList.append(willAddId)
    await dataSource.updateGroupItem(msgData['groupId'], "teamList", oldTeamList)
    resultMsg = await reply(msgCode.TEAM_ADD_SUCCESS.name, msgData, result)
    await bot.send_msg(user_id=msgData["userId"], group_id=msgData["groupId"], message=resultMsg, auto_escape=False)
    return True


# team clear/clr/cls 清空队伍
async def teamClr(msgStr, msgData, bot):
    return


# team rm/del @at|uid|id 从队伍删除
async def teamRm(msgStr, msgData, bot):
    # 获取当前成员列表，查看是否存在该用户，如不存在则移除
    return


# team call 呼叫队伍全体成员
async def teamCall(msgData, bot):
    groupInfo = await dataSource.getGroupInfo(msgData['groupId'])
    # 应当显示属性和状态
    nowTeamList = groupInfo["teamList"]
    i = 0
    result = []
    for idStr in nowTeamList:
        i += 1
        s = f"{str(i)}.{cqUtil.atSomebody(idStr)}"
        result.append(s)
    resultMsg = await reply(msgCode.TEAM_CALL.name, msgData, "\n".join(result))
    await bot.send_msg(user_id=msgData["userId"], group_id=msgData["groupId"], message=resultMsg, auto_escape=False)
    return True


# team @at|uid propvalue 调整成员卡属性
async def teamProp(msgStr, msgData, bot):
    return


# team lock 一键全体卡上锁
async def teamLock(msgStr, msgData, bot):
    return
