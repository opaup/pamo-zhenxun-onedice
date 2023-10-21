# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/20
import re
import time
import csv

from nonebot import on_command, on_notice, on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, NoticeEvent

from ..utils import data as dataSource
from ..utils import eventUtil, logsUtil, emailUtil

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
                await log.finish("输入的logName包含非法字符")
            await logOn(logName, logInfo, groupId, bot)
        else:
            await log.finish("必须告诉真寻日志叫什么名字呀")
    if split[0] == "get":
        if not len(split) <= 1:
            logName = split[1]
            illegalRegex = r'[\\/:*\?"<>|]'
            if re.search(illegalRegex, logName):
                await log.finish("输入的logName包含非法字符")
            await logGet(logName, logInfo, userId, groupId, bot)
        else:
            await log.finish("必须告诉真寻日志叫什么名字呀")
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
    resultMsg = f"已暂时关闭名为{logName}的日志记录，可以使用.log on/get {logName}开启或获取哦。"
    await dataSource.updateGroupItem(groupId, 'log', logInfo)
    await bot.send_msg(group_id=int(groupId), message=resultMsg, auto_escape=False)


async def logGet(logName, logInfo, userId, groupId, bot):
    # 最后再对临时日志进行排序整理、格式化时间戳
    # 识别图片CQ码
    # line = f"({nowTime}){pcname}: {msgStr}"
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    groupName = await eventUtil.getGroupName(groupId, bot)
    logData = await logsUtil.readFromCSV(groupId, logName)
    txtUrl = await logsUtil.putToTxt(groupId, logName, logData)
    csvUrl = logsUtil.getCsvPath(groupId, logName)
    title = f"【拉比邮政局】群聊[{groupName}({groupId})]中的日志文件：{logName}"
    content = f"这是您在群聊[{groupName}({groupId})]中存放的日志文件：{logName}\n\t ---拉比邮政局 {nowTime}"
    recvAddress = f"{userId}@qq.com"
    with open(txtUrl, 'r', encoding='utf-8') as f:
        payload_txt = f.read()
    with open(csvUrl, 'r', encoding='utf-8') as f:
        payload_csv = f.read()
    await emailUtil.sendMail(title, content, recvAddress, logName=logName, payload_txt=payload_txt, payload_csv=payload_csv)
    resultMsg = f"包含日志文件的邮件包裹已经寄出给地址：[{recvAddress}]啦，请注意查收~"
    await bot.send_msg(group_id=int(groupId), message=resultMsg, auto_escape=False)


async def getLogList():
    return


async def logHelp():
    return


msgHandler = on_message(priority=1, block=False)
noticeHandler = on_notice(priority=1, block=False)


@msgHandler.handle()
async def msgRecoder(bot: Bot, event: MessageEvent):
    messageId = str(event.message_id)
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
    # 解析AT类型的CQ码
    pattern = r'\[CQ:at,qq=(\d+)\]'
    match = re.search(pattern, message)
    if match:
        qid = match.group(1)
        atPcname = await eventUtil.getPcName(str(qid), msgData, bot)
        message = re.sub(pattern, f'@{atPcname}({qid})', message)

    row = [typeName, messageId, timestamp, message, userId, pcname]
    await logsUtil.writeIntoCSV(groupId, logName, row)
    await msgHandler.finish(None)


@noticeHandler.handle()
async def noticeRecoder(bot: Bot, event: NoticeEvent):
    await noticeHandler.finish(None)


