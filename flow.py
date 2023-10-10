from sub.custom import reply
from em.msgCode import msgCode
import utils.data as dataSource
from core import ra, rd, make, st, sanCheck
import re


async def doFlow(msgData):
    cmdStr = msgData["msg"].lower().lstrip()
    print(cmdStr)

    # 检查该环境下的dice功能是否开启

    # coc
    if re.match(r'^(coc)', cmdStr):
        cmdStr = re.sub("coc", "", cmdStr, count=1).strip()
        try:
            num = int(cmdStr)
        except ValueError:
            num = 1
        return await make.cocMaker(num, msgData)
    # dnd
    if re.match(r'^(dnd)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # coc5th
    if re.match(r'^(coc5th)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # cochild
    if re.match(r'^(cochild)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # rh
    if re.match(r'^(rh)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # st
    if re.match(r'^(st|pc|nn)', cmdStr):
        cmdStr = re.sub(r'\b(st|pc|nn)\b', "", cmdStr, count=1).strip()
        return await st.stFlow(cmdStr, msgData)
    # ra
    if re.match(r'^(ra)', cmdStr):
        cmdStr = re.sub(r'ra', "", cmdStr, count=1).strip()
        return await ra.doRa(cmdStr, msgData)
    # sc
    if re.match(r'^(sc)', cmdStr):
        cmdStr = re.sub(r'sc', "", cmdStr, count=1).strip()
        return await sanCheck.sc(cmdStr, msgData)
    # rc
    if re.match(r'^(rc)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # rb
    if re.match(r'^(rb)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # rp
    if re.match(r'^(rp)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # npc
    if re.match(r'^(npc)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)

    # rd单独最后处理（如果前面都没匹配上，则执行rd
    rdPattern = r'(?:r(?:\\d{1,2})?(?:d\\w{0,16}|$)|r)(.*)'
    if re.match(rdPattern, cmdStr):
        try:
            return await rd.rdFlow(cmdStr, msgData)
        except ValueError:
            return await reply(msgCode.ILLEGAL_FORMAT.name, msgData)
    # return await reply(msgCode.NO_COMMAND.name)
    return False

# ===二级指令


# st
