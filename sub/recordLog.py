# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/20
import re
import time
import csv

from nonebot import on_command, on_notice, on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, NoticeEvent
from services.log import logger
from utils.utils import scheduler
from ..models import MsgData
from ..em.msgCode import msgCode
from ..sub.custom import reply
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
                resultMsg = await reply(msgCode.LOGS_START_FAIL.name)
                await log.finish(resultMsg)
            await logOn(logName, logInfo, userId, groupId, bot)
        else:
            resultMsg = await reply(msgCode.LOGS_NOT_HAVE_NAME.name)
            await log.finish(resultMsg)
        return
    if split[0] == "get":
        if not len(split) <= 1:
            logName = split[1]
            illegalRegex = r'[\\/:*\?"<>|]'
            if re.search(illegalRegex, logName):
                resultMsg = await reply(msgCode.LOGS_START_FAIL.name)
                await log.finish(resultMsg)
            await logGet(logName, logInfo, userId, groupId, bot)
        else:
            resultMsg = await reply(msgCode.LOGS_NOT_HAVE_NAME.name)
            await log.finish(resultMsg)
        return
    if split[0] == "off":
        await logOff(logInfo, userId, groupId, bot)
        return
    if split[0] == "end":
        await logEnd(msgStr, userId, groupId, bot)
        return
    if split[0] == "help":
        return log.finish(logHelp())
    if split[0] == "list":
        await getLogList(logInfo, userId, groupId, bot)
        return
    await log.finish(None)


async def logOn(logName, logInfo, userId, groupId, bot):
    """
    # 判断是否已经有在记录且未关闭，有则返回，无则split[1] 为logName
    # 设置当前group的log的logging = logName，状态为on
    # 添加log记录到logList，key为name，value为创建时间|最后修改时间
    """
    if logInfo['status'] == "on":
        # 已被开启，不可重复开启
        resultMsg = f"当前还在记录日志[{logInfo['logging']}]，请先使用 [log off {logInfo['logging']}] 关闭记录"
        await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)
        return
    if logName in logInfo['endList']:
        # 已结束不可开启
        resultMsg = f"该日志已被结束，无法进行操作，请使用.log get获取，如有疑问可联系管理员"
        await bot.send_msg(group_id=int(groupId), message=resultMsg, auto_escape=False)
        return
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    logInfo['status'] = "on"
    logInfo['logging'] = logName
    logList = logInfo['logList']
    logList[logName] = f"{startTime},"
    resultMsg = f"已开启名为{logName}的日志记录，记得使用.log off暂时关闭哦。"
    await dataSource.updateGroupItem(groupId, 'log', logInfo)
    await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)


async def logOff(logInfo, userId, groupId, bot):
    if not logInfo['status'] == "on":
        # 没有在记录的日志
        resultMsg = f"当前没有正在记录的日志哦！"
        await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)
        return
    updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    logInfo['status'] = "off"
    logList = logInfo['logList']
    logName = logInfo['logging']
    timeGroup = logList[logName]
    split = re.split(",", timeGroup)
    startTime = split[0]
    logList[logName] = f"{startTime}|{updateTime}"
    resultMsg = await reply(msgCode.LOGS_OFF_SUCCESS.name, result=logName)
    await dataSource.updateGroupItem(groupId, 'log', logInfo)
    await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)

async def logEnd(msgStr, userId, groupId, bot):
    endTime = time.time()
    logName = msgStr.replace("end", "").strip()
    logInfo = await dataSource.getGroupItem(groupId, 'log')
    if logInfo['status'] == "on":
        # 当前还在记录日志
        resultMsg = f"当前还在记录日志[{logInfo['logging']}]，请先使用 [log off {logInfo['logging']}] 关闭记录"
        await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)
        return
    if logName == "":
        resultMsg = await reply(msgCode.LOGS_NOT_HAVE_NAME.name)
        await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)
        return
    if logName in logInfo['endList']:
        resultMsg = f"该日志已被结束，无法进行操作，请使用.log get获取，如有疑问可联系管理员"
        await bot.send_msg(group_id=int(groupId), message=resultMsg, auto_escape=False)
        return
    logInfo['endList'][logName] = int(endTime)
    resultMsg = f"已结束日志[{logName}]的记录，可以使用(.log get {logName})获取，超过14天未获取将被自动清除。"
    await dataSource.updateGroupItem(groupId, 'log', logInfo)
    await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)


async def logGet(logName, logInfo, userId, groupId, bot):
    """
    # 最后再对临时日志进行排序整理、格式化时间戳
    # 识别图片CQ码
    # line = f"({nowTime}){pcname}: {msgStr}"
    """
    # TODO 对撤回等事件记录进行处理
    if logName not in logInfo['endList']:
        resultMsg = f"该日志还没有创建或结束哦，需要先使用 .log end 结束日志记录。"
        await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)
        return
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    groupName = await eventUtil.getGroupName(groupId, bot)
    logData = await logsUtil.readFromCSV(groupId, logName)
    txtUrl = await logsUtil.putToTxt(groupId, logName, logData)
    csvUrl = logsUtil.getCsvPath(groupId, logName)
    title = f"【拉比邮政局】群聊[{groupName}({groupId})]中的日志文件：{logName}"
    content = f"这是您在群聊[{groupName}({groupId})]中存放的日志文件：{logName}\n  ---拉比邮政局 {nowTime}"
    recvAddress = f"{userId}@qq.com"
    with open(txtUrl, 'r', encoding='utf-8') as f:
        payload_txt = f.read()
    with open(csvUrl, 'r', encoding='utf-8') as f:
        payload_csv = f.read()
    await emailUtil.sendMail(title, content, recvAddress, logName=logName, payload_txt=payload_txt,
                             payload_csv=payload_csv)
    resultMsg = await reply(msgCode.LOGS_SEND_SUCCESS.name, result=recvAddress)
    await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)


async def getLogList(logInfo, userId, groupId, bot):
    i = 1
    logsList = []
    for logName in logInfo['logList']:
        if logName == logInfo['logging'] and logInfo['status'] == "on":
            status = f"（记录ing）"
        else:
            if logName in logInfo['endList']:
                endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logInfo['endList'][logName]))
                status = f" (已结束于: {endTime})"
            else:
                status = ""
        logsList.append(f"{i}. {logName}{status}")
        i += 1
    groupName = await eventUtil.getGroupName(groupId, bot)
    listStr = "\n".join(logsList)
    resultMsg = f"群聊[{groupName}({groupId})]的日志记录列表：\n{listStr}"
    await bot.send_msg(user_id=int(userId), group_id=int(groupId), message=resultMsg, auto_escape=False)


def logHelp():
    resultMsg = (f"log on/off 开启/关闭日志记录"
                 f"log end 结束日志记录"
                 f"log get 获取日志"
                 f"log list 获取当前群组下的日志列表")
    return resultMsg


msgHandler = on_message(priority=1, block=False)
noticeHandler = on_notice(priority=1, block=False)


@msgHandler.handle()
async def msgRecoder(bot: Bot, event: MessageEvent, msgData=MsgData.MsgData()):
    if not event.message_type == "group":
        return
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
    logger.info(f"[onedice-logRecoder] logging message({messageId}) to the log named {logName}")
    msgData.userId = str(userId)
    msgData.groupId = str(groupId)
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
    # TODO 对撤回等事件进行记录
    await noticeHandler.finish(None)


@scheduler.scheduled_job(
    "cron",
    hour=2,
    minute=1,
)
async def cleanLocalLogs():
    """
    # 每天凌晨两点钟进行一次本地logs检查，已完成且超过14天的logs将被清除
    # 清理前先push一次
    """
    return
