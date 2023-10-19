# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/18
from nonebot import on_command, Driver
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message, MessageEvent
from services.log import logger
from utils.decorator.shop import shop_register, NotMeetUseConditionsException
from ..utils import eventUtil as eventUtil
from ..utils import data as dataSource
from ..utils import cqUtil
from models.bag_user import BagUser
import time

driver: Driver = nonebot.get_driver()


# 只有在开启了扩散功能的群聊才可使用该功能
# 添加商城道具：，每日有概率获得1件，每日购买上限1件，最多持有3件
# 发布团贴需要消耗该道具
@driver.on_startup
async def _():
    await shop_register(
        name='拉比公告服务券',
        price=100,
        des='还在等什么？快将你的开团公告扩散到其他群聊吧！（每人上限3张，大于3张时可能会被收缴哦~）',
        load_status=True,
        daily_limit=2,
        is_passive=True
    )


noticeCmds = [".notice", "。notice", "发布公告", "发布团贴"]
notice = on_command(".notice", aliases={"。notice", "发布公告", "发布团贴"}, priority=5, block=True)


@notice.handle()
async def notice(bot: Bot, event: MessageEvent):
    startTime = time.time()
    userId = 0
    groupId = 0
    msg = str(event.message)
    userName = event.sender.nickname
    groupName = await eventUtil.getGroupName(groupId, bot)
    atSender = cqUtil.atSomebody(userId)
    mid = str(event.message_id)
    for s in noticeCmds:
        msg = msg.replace(s, "").lstrip()
    # 是否有券或大于3个
    property = await BagUser.get_property(userId, groupId)
    rabi = 0
    if rabi <= 0:
        return "dont have rabi"
    elif rabi > 3:
        consume = -(3 - rabi)
    else:
        consume = 1
    # 消耗掉，如果大于3，则多消耗
    await BagUser.delete_property(userId, groupId, "拉比公告服务券", consume)

    timestamp = event.time
    timeTuple = time.localtime(timestamp)
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", timeTuple)
    pioneerText = f"{atSender} 已将你的公告添加到了扩散队列，请耐心等待哦~"
    noticeText = f"来自[{groupName}({groupId})]的[{userName}({userId})]发布了公告：\n{msg}\n---回T不会退订，公告时间：{datetime}"
    logger.info(f"[onedice-notice]{noticeText}")

    await bot.send_msg(group_id=int(groupId), message=pioneerText, auto_escape=False)
    count = 0
    memberCount = 0
    # 获取开启了扩散的全部群聊
    groupInfoList = await bot.get_group_list()
    for groupInfo in groupInfoList:
        gid = str(groupInfo['group_id'])
        member = groupInfo['member_count']
        flag = await dataSource.getGroupItem(gid, 'isNotice')
        if flag == "on":
            count += 1
            memberCount += member
            await bot.send_msg(group_id=int(gid), message=noticeText, auto_escape=False)
            logger.info(f"[onedice-notice]已将扩散任务:[{mid}]扩散到群聊：{gid}")
            time.sleep(3)

    endTime = time.time()
    spendTime = "{:.2f}秒".format(endTime - startTime)
    result = f"{atSender} 扩散任务完毕！已发送到了{count}个扩散群咯~预计可能会有{memberCount}位小伙伴看到公告，任务总计耗时{spendTime}"
    logger.info(result)
    await notice.finish(result)
