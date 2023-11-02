from .sub.custom import reply
from .em import msgCode
from .utils import data as dataSource
from .core import ra, rh, rd, rpAndRb, make, st, sanCheck, diceConfig, LiAndTi
from .sub import team, botInfo
from services.log import logger
import re


help_template = f"""这里是一个临时的帮助说明。
目前pamo-zhenxun-onedice仍在初期开发过程，如出现未知bug请及时联系帕沫（525915186）。
简单的指令列表：
基本的.rd
.coc coc7th人物卡作成
.st 角色名 切卡
.st 角色名-属性属性值 录入/更新
.st 属性+-值 当前卡属性调整
.st show (属性名) 查看角色卡详情/属性值
.st list 查看角色卡列表
.st rm 删除角色卡
.st lock/unlock 锁定/解锁角色卡
——————
.rd基础投掷
.ra检定
.rp和.rb惩罚奖励骰
.rh暗骰（格式和rd一致）
.ti (list) 临时/即时疯狂症状| list 查看全部
.li (list) 总结疯狂症状| list 查看全部
.lio 查看全部焦躁症
.lip 查看全部恐惧症
.sc san值检定
——————
.dice help 查看群设置帮助
.team 查看当前队伍列表
.team call 呼叫全体队伍成员
.team add/rm @成员 从本群队伍中添加/移除成员
.team @成员 属性n (n代表数字)调整目标的属性值
.team show @成员 (属性) 获取成员(目标属性)的属性值
.team clear 清除队伍
.team lock/unlock 队伍上锁/解锁
.notice/发布公告/发布团贴 [公告内容] 进行团贴扩散请求
——————
详细可查看项目地址：{botInfo.project_address}
"""


async def doFlow(msgData, bot):
    cmdStr = msgData.msg.lower().strip()
    logger.info(rf"[onedice]检测到指令：{cmdStr}")

    # 查找是否包含cq,替换成CQ
    if re.search(r'cq', cmdStr):
        cmdStr = re.sub(r'cq', 'CQ', cmdStr)

    # 设置
    if re.match(r'^(dice)', cmdStr):
        cmdStr = re.sub("dice", "", cmdStr, count=1).strip()
        return await diceConfig.diceFlow(cmdStr, msgData)
    # 检查该环境下的dice功能是否开启
    if msgData.msgType == "group":
        if not await dataSource.getGroupItem(msgData.groupId, "onOff") == "on":
            return False

    # 获取bot信息
    if re.match(r'^(bot)', cmdStr):
        return await botInfo.botInfo(msgData, bot)
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
    # ti
    if re.match(r'^(ti)', cmdStr):
        cmdStr = re.sub(r'ti', "", cmdStr, count=1).strip()
        return await LiAndTi.getTi(cmdStr)
    # li
    if re.match(r'^(li)', cmdStr):
        cmdStr = re.sub(r'li', "", cmdStr, count=1).strip()
        return await LiAndTi.getLi(cmdStr)
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
    # team
    if re.match(r'^(team)', cmdStr):
        cmdStr = re.sub(r'team', "", cmdStr, count=1).strip()
        return await team.teamFlow(cmdStr, msgData, bot)
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
