from sub.custom import reply
from em.msgCode import msgCode
import utils.data as dataSource
from core import ra, rd, make, st
import re


def doFlow(cmdStr):
    result = ""
    userId = dataSource.USERID
    groupId = dataSource.GROUPID
    diceType = dataSource.getDiceType(groupId)
    cmdStr = cmdStr.lower().lstrip()
    print(cmdStr)

    # coc
    if re.match(r'^(coc)', cmdStr):
        cmdStr = re.sub("coc", "", cmdStr, count=1)
        try:
            num = int(cmdStr)
        except ValueError:
            num = 1
        return make.cocMaker(num)
    # dnd
    if re.match(r'^(dnd)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # coc5th
    if re.match(r'^(coc5th)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # cochild
    if re.match(r'^(cochild)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # rh
    if re.match(r'^(rh)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # st
    if re.match(r'^(st|pc|nn)', cmdStr):
        return st.stFlow(cmdStr=cmdStr, userId=userId, groupId=groupId)
    # ra
    if re.match(r'^(ra)', cmdStr):
        return ra.doRa()
    # sc
    if re.match(r'^(sc)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # rc
    if re.match(r'^(rc)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # rb
    if re.match(r'^(rb)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # rp
    if re.match(r'^(rp)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)
    # npc
    if re.match(r'^(npc)', cmdStr):
        return reply(msgCode.NO_ACHIEVE_CMD.name)

    # rd单独最后处理（如果前面都没匹配上，则执行rd
    rdPattern = r'(?:r(?:\\d{1,2})?(?:d\\w{0,16}|$)|r)(.*)'
    if re.match(rdPattern, cmdStr):
        try:
            return rd.rdFlow(cmdStr, diceType)
        except ValueError:
            return reply(msgCode.ILLEGAL_FORMAT.name, result)
    # return reply(msgCode.NO_COMMAND.name)
    return False

# ===二级指令


# st
