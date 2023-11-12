# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/11/3
from ..em.msgCode import msgCode
from ..sub.custom import reply
from ..utils import data as dataSource

async def getHistoryForRoll(msgData):
    userId = msgData.userId
    userInfo = dataSource.getUserInfo(userId)
    rollNum = userInfo["successRollNum"]
    successRollNum = userInfo["successRollNum"]
    failRollNum = userInfo["failRollNum"]
    greatSuccessRollNum = userInfo["greatSuccessRollNum"]
    greatFailRollNum = userInfo["greatFailRollNum"]
    # 总计创建角色卡
    # 总计购买拉比服务券、总计消耗次数
    resultMsg = (f"根据小真寻的笔记本显示，你总计进行了{rollNum}次roll点检定：\n"
                 f"其中，成功次数为{successRollNum}，失败次数为{failRollNum}\n"
                 f"大成功次数为{greatSuccessRollNum}，大失败次数为{greatFailRollNum}")

    return resultMsg
