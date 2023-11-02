# -*- coding: utf-8 -*-
# @Author: opaup
import re
from ..em.msgCode import msgCode
from ..sub.custom import reply
from ..utils import data as dataSource


async def helpFlow(msgStr, msgData):
    cmds = re.split(" ", msgStr)
    normal = ["normal", "普通", "一般", "一般指令", "roll"]
    # character = ["character", "角色", "卡", "角色卡", "st", "nn", "pc", "card"]
    subsidiary = ["sub", "subsidiary", "附属"]
    if cmds[0] in normal:
        resultMsg = (f"rd 基础的roll点指令\n"
                     f"ra 规则检定\n"
                     f"rp/rb 惩罚/奖励骰，例rp2即两个惩罚骰\n"
                     f"rh 暗骰，用法与rd一致\n"
                     f"sc成功/失败 例 sc1/1d3，即san值检定成功减少1，失败减少1d3\n"
                     f"ti/li(症状名) 临时/即时疯狂与总结症状，如后面跟症状名即获取症状描述，否则为随机获取，如.li失忆\n"
                     f"tio/tip 查看狂躁症与恐惧症列表")
        return resultMsg
    if cmds[0] in subsidiary:
        resultMsg = (f"coc (num) coc7th角色卡作成，如后面有数字则是获取n次\n"
                     f"st help 角色卡相关帮助\n"
                     f"team help 团队操作相关帮助\n"
                     f"log help 日志操作相关帮助\n"
                     f"notice [内容] 发布团贴扩散任务，发布团贴需要消耗拉比服务券，如没有请使用[签到]/[购买拉比服务券]，详见[真寻帮助]\n"
                     f"其中一级指令，notice≈(发布公告=发布团贴(无需加.作为前缀))， st=pc=nn")
        return resultMsg
    if cmds[0] == "dice":
        return await reply(key=msgCode.DICE_SET_HELP.name, msgData=msgData)
    if cmds[0] == "other":
        return "暂无"

    return
