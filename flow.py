from sub.custom import reply
from em.msgCode import msgCode
import utils.data as dataSource
from core import ra, rd, make, st
import re

cmdStr = ""
groupId = ""
userId = ""
username = ""


def doFlow(msgData):
    global cmdStr, username, userId, groupId
    result = ""
    cmdStr = msgData["msg"]
    groupId = msgData["groupId"]
    userId = msgData["userId"]
    username = msgData["username"]
    diceType = dataSource.getDiceType(groupId)
    cmdStr = cmdStr.lower().lstrip()
    print(cmdStr)

    # 检查该环境下的dice功能是否开启

    # coc
    if re.match(r'^(coc)', cmdStr):
        cmdStr = re.sub("coc", "", cmdStr, count=1).strip()
        try:
            num = int(cmdStr)
        except ValueError:
            num = 1
        return make.cocMaker(num, msgData)
    # dnd
    if re.match(r'^(dnd)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # coc5th
    if re.match(r'^(coc5th)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # cochild
    if re.match(r'^(cochild)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # rh
    if re.match(r'^(rh)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # st
    if re.match(r'^(st|pc|nn)', cmdStr):
        cmdStr = re.sub(r'\b(st|pc|nn)\b', "", cmdStr, count=1).strip()
        return st.stFlow(msgStr=cmdStr, msgData=msgData)
    # ra
    if re.match(r'^(ra)', cmdStr):
        return ra.doRa(cmdStr, msgData=msgData)
    # sc
    if re.match(r'^(sc)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # rc
    if re.match(r'^(rc)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # rb
    if re.match(r'^(rb)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # rp
    if re.match(r'^(rp)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)
    # npc
    if re.match(r'^(npc)', cmdStr):
        return reply(key=msgCode.NO_ACHIEVE_CMD.name, result="", msgData=msgData)

    # rd单独最后处理（如果前面都没匹配上，则执行rd
    rdPattern = r'(?:r(?:\\d{1,2})?(?:d\\w{0,16}|$)|r)(.*)'
    if re.match(rdPattern, cmdStr):
        try:
            return rd.rdFlow(cmdStr, diceType, msgData=msgData)
        except ValueError:
            return reply(key=msgCode.ILLEGAL_FORMAT.name, result="", msgData=msgData)
    # return reply(msgCode.NO_COMMAND.name)
    return False

# ===二级指令


# st
