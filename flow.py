from .sub.custom import reply
from .em import msgCode
from .utils import data as dataSource
from .core import ra, rh, rd, rpAndRb, make, st, sanCheck, diceConfig
import re


help_template = """这里是一个临时的帮助说明。
目前pamo-zhenxun-onedice仍在初期开发过程，如出现未知bug请及时联系帕沫（525915186）。
目前实现了：
基本的.rd
.coc
.st 角色名 切卡
.st 角色名-属性属性值 录入/更新
.st 属性+-值 当前卡属性调整
.st show (属性名) 查看角色卡详情/属性值
.st list 查看角色卡列表
.rd基础投掷
.ra检定
.rp和.rb惩罚奖励骰
.rh暗骰（格式和rd一致）
.sc
.dice help 查看群设置帮助
——————
项目地址：https://github.com/opaup/pamo-zhenxun-onedice
"""


async def doFlow(msgData, bot):
    cmdStr = msgData["msg"].lower().lstrip()
    print(cmdStr)

    # 设置
    if re.match(r'^(dice)', cmdStr):
        cmdStr = re.sub("dice", "", cmdStr, count=1).strip()
        return await diceConfig.diceFlow(cmdStr, msgData)
    # 检查该环境下的dice功能是否开启
    if msgData['msgType'] == "group":
        if not await dataSource.getGroupItem(msgData['groupId'], "onOff") == "on":
            return False

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
        cmdStr = re.sub(r'rh', "", cmdStr, count=1).strip()
        return await rh.rh(cmdStr, msgData, bot)
    # st
    if re.match(r'^(st|pc|nn)', cmdStr):
        cmdStr = re.sub(r'\b(st|pc|nn)\b', "", cmdStr, count=1).strip()
        return await st.stFlow(cmdStr, msgData)
    # ra
    if re.match(r'^(ra)', cmdStr):
        cmdStr = re.sub(r'ra', "", cmdStr, count=1).strip()
        return await ra.doRa(cmdStr, msgData, bot)
    # sc
    if re.match(r'^(sc)', cmdStr):
        cmdStr = re.sub(r'sc', "", cmdStr, count=1).strip()
        return await sanCheck.sc(cmdStr, msgData, bot)
    # rc
    if re.match(r'^(rc)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # rb
    if re.match(r'^(rb)', cmdStr):
        cmdStr = re.sub(r'rb', "", cmdStr, count=1).strip()
        return await rpAndRb.rb(cmdStr, msgData)
    # rp
    if re.match(r'^(rp)', cmdStr):
        cmdStr = re.sub(r'rp', "", cmdStr, count=1).strip()
        return await rpAndRb.rp(cmdStr, msgData)
    # npc
    if re.match(r'^(npc)', cmdStr):
        return await reply(msgCode.NO_ACHIEVE_CMD.name, msgData)
    # help
    if re.match(r'^(help|帮助)', cmdStr):
        cmdStr = re.sub(r'\b(help|帮助)\b', "", cmdStr, count=1).strip()
        tempResult = help_template
        return tempResult
    # rd单独最后处理（如果前面都没匹配上，则执行rd
    rdPattern = r'(?:r(?:\\d{1,2})?(?:d\\w{0,16}|$)|r)(.*)'
    if re.match(rdPattern, cmdStr):
        try:
            return await rd.rdFlow(cmdStr, msgData, bot)
        except ValueError:
            return await reply(msgCode.ILLEGAL_FORMAT.name, msgData)
    # return await reply(msgCode.NO_COMMAND.name)
    return False

# ===二级指令


# st
