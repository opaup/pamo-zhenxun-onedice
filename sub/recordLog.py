# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/20
import re
import time
import csv

from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, NoticeEvent

from ..utils import data as dataSource
from ..utils import eventUtil as eventUtil
from ..utils import logsUtil

log = on_command(
    ".log", aliases={"。log"}, priority=2, block=False
)


@log.handle()
async def handle_receive(bot: Bot, event: MessageEvent):
    msgStr = str(event.message).replace(".log", "").replace("。log", "").strip()
    userId = event.sender.user_id
    groupId = str(event.group_id)
    split = re.split(' ', msgStr)
    logInfo = await dataSource.getGroupItem(groupId, 'log')
    if split[0] == "on":
        if not len(split) <= 1:
            logName = split[1]
            illegalRegex = r'[\\/:*\?"<>|]'
            if re.search(illegalRegex, logName):
                print("输入的logName包含非法字符")
                return
            await logOn(logName, logInfo, groupId, bot)
        else:
            # 必须告诉真寻日志叫什么名字呀
            return
    if split[0] == "off":
        await logOff(logInfo, groupId, bot)

    await log.finish(None)


async def logOn(logName, logInfo, groupId, bot):
    """
    # 判断是否已经有在记录且未关闭，有则返回，无则split[1] 为logName
    # 设置当前group的log的logging = logName，状态为on
    # 添加log记录到logList，key为name，value为创建时间|最后修改时间
    """
    if logInfo['status'] == "on":
        # 已被开启，不可重复开启
        return
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    logInfo['status'] = "on"
    logInfo['logging'] = logName
    logList = logInfo['logList']
    logList[logName] = f"{startTime},"
    resultMsg = f"已开启名为{logName}的日志记录，记得使用.log off暂时关闭哦。"
    await dataSource.updateGroupItem(groupId, 'log', logInfo)
    await bot.send_msg(group_id=int(groupId), message=resultMsg, auto_escape=False)
    return


async def logOff(logInfo, groupId, bot):
    if not logInfo['status'] == "on":
        # 没有在记录的日志
        return
    updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    logInfo['status'] = "off"
    logList = logInfo['logList']
    logName = logInfo['logging']
    timeGroup = logList[logName]
    split = re.split(",", timeGroup)
    startTime = split[0]
    logList[logName] = f"{startTime}|{updateTime}"
    resultMsg = f"已暂时关闭名为{logName}的日志记录，可以使用.log on/end {logName}开启或终止哦。"
    await dataSource.updateGroupItem(groupId, 'log', logInfo)
    await bot.send_msg(group_id=int(groupId), message=resultMsg, auto_escape=False)

    return


async def logEnd():
    # 最后再对临时日志进行排序整理、格式化时间戳
    # 识别图片CQ码
    # text = f"({nowTime}){pcname}: {msgStr}"
    # nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return


async def logGet():
    return


async def getLogList():
    return


async def logHelp():
    return


msgHandler = on_command(cmd="", priority=1, block=False)
noticeHandler = on_notice(priority=1, block=False)


@msgHandler.handle()
async def msgRecoder(bot: Bot, event: MessageEvent):
    message = str(event.message)
    userId = event.sender.user_id
    groupId = str(event.group_id)
    typeName = 'message'
    timestamp = str(event.time)
    # 如果log状态不为on，则跳过
    logInfo = await dataSource.getGroupItem(groupId, 'log')
    if not logInfo['status'] == "on":
        # 没有在记录的日志
        return
    logName = logInfo['logging']
    msgData = {
        "userId": str(userId),
        "groupId": groupId
    }
    pcname = await eventUtil.getPcName(userId, msgData, bot)

    row = [typeName, id, timestamp, message, userId, pcname]
    await logsUtil.writeIntoCSV(groupId, logName, row)
    await msgHandler.finish(None)


@noticeHandler.handle()
async def noticeRecoder(bot: Bot, event: NoticeEvent):
    await noticeHandler.finish(None)


