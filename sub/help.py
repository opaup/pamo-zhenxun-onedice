# -*- coding: utf-8 -*-
# @Author: opaup
import re
from ..models import MsgData
from ..em.msgCode import msgCode
from ..sub.custom import reply
from ..utils import data as dataSource

async def helpFlow(msgStr, msgData):
    cmds = re.split(" ", msgStr)
    if cmds[0] == "normal":
        # 基础指令
        return
    if cmds[0] == "character":
        # 角色卡相关（包括团队
        return
    if cmds[0] == "dice":
        # 骰设置相关
        return
    if cmds[0] == "others":
        # 其他
        return

    return
