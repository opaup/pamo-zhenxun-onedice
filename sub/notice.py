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
import nonebot

driver: Driver = nonebot.get_driver()
itemName = '拉比服务券'


# 只有在开启了扩散功能的群聊才可使用该功能
# 添加商城道具：每日购买上限1件，最多持有3件
# 发布团贴需要消耗该道具
# 多出来的券会被概率收缴所以需要进行检定
@driver.on_startup
async def _():
    @shop_register(
        name=itemName,
        price=100,
        des='还在等什么？快将你的开团公告扩散到其他群聊吧！（每人上限3张，大于3张时可能会被额外收缴哦~）',
        load_status=True,
        daily_limit=2,
        is_passive=True,
    )
    async def used(goods_name: str, user_id: int, group_id: int, prob: float):
        print(f"USER {user_id} GROUP {group_id} 这个道具：{goods_name}使用成功了：{prob}")

noticeCmds = [".notice", "。notice", "发布公告", "发布团贴"]
notice = on_command(".notice", aliases={"。notice", "发布公告", "发布团贴"}, priority=5, block=True)


@notice.handle()
async def notice(bot: Bot, event: MessageEvent):
    startTime = time.time()
    userId = event.sender.user_id
    groupId = event.group_id
    msg = str(event.message)
    userName = event.sender.nickname
    groupName = await eventUtil.getGroupName(groupId, bot)
    groupInfo2 = await dataSource.getGroupInfo(str(groupId))
    atSender = cqUtil.atSomebody(userId)
    mid = str(event.message_id)
    flag = False
    if not groupInfo2['isNotice'] == 'on':
        msg = f"{atSender} 本群非扩散群，请先让管理员使用.dice notice on打开扩散功能！"
        await bot.send_msg(group_id=int(groupId), message=msg, auto_escape=False)
        return
    for s in noticeCmds:
        msg = msg.replace(s, "").strip()
    # 是否有券或大于3个
    userBag = await BagUser.get_property(userId, groupId)
    if itemName not in userBag:
        msg = f"{atSender} 的包包里没有{itemName}，别想在真寻面前萌混过关哦"
        await bot.send_msg(group_id=int(groupId), message=msg, auto_escape=False)
        return
    rabi = userBag[itemName]
    if rabi > 3:
        consume = -(3 - rabi) + 1
        flag = True
    else:
        consume = 1

    timestamp = event.time
    timeTuple = time.localtime(timestamp)
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", timeTuple)
    pioneerText = f"{atSender} 已将你的公告添加到了扩散队列，请耐心等待啦~"
    noticeText = f"来自[{groupName}({groupId})]的[{userName}({userId})]发布了公告：\n{msg}\n---回T不会退订，公告时间：{datetime}"
    logger.info(f"[onedice-notice]{noticeText}")

    await bot.send_msg(group_id=int(groupId), message=pioneerText, auto_escape=False)
    count = 0
    # 获取开启了扩散的全部群聊
    groupInfoList = await bot.get_group_list()
    print(groupInfoList)
    for groupInfo2 in groupInfoList:
        gid = str(groupInfo2['group_id'])
        flag = await dataSource.getGroupItem(gid, 'isNotice')
        # 不在该群发送
        if int(gid) == int(groupId):
            continue
        if flag == "on":
            count += 1
            await bot.send_msg(group_id=int(gid), message=noticeText, auto_escape=False)
            logger.info(f"[onedice-notice]已将扩散任务:[{mid}]扩散到群聊：{gid}")
            time.sleep(3)

    # 消耗掉道具，如果大于3，则概率多消耗
    await BagUser.delete_property(userId, groupId, itemName, consume)
    endTime = time.time()
    spendTime = "{:.2f}秒".format(endTime - startTime)
    result = f"{atSender} 扩散任务完毕！已将任务id[{mid}]扩散到了{count}个群聊~总计耗时{spendTime}"
    logger.info(result)
    await bot.send_msg(group_id=int(groupId), message=result, auto_escape=False)
    await notice.finish(None)
