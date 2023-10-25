# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/24
from utils.utils import scheduler
from services.log import logger
from nonebot import on_command, Driver
import nonebot
import re
from . import _model as database
from . import dbUtils
from ..utils import data as dataSource
from ..utils import logsUtil, strUtil

# 启动时检查本地文件与数据库
driver: Driver = nonebot.get_driver()


@driver.on_startup
async def checkLocalData():
    """
    检查本地文件与数据库是否对应（从数据库下载到本地）
    """
    logger.warning("[onedice] 正在检查本地数据文件")

    try:
        # 检查用户数据
        userList = await database.onedice_user.all().values_list("id", flat=True)
        for userId in userList:
            if not await dataSource.checkExist_user(userId):
                await dbUtils.pullUserData(userId)
        # 检查群组数据
        groupList = await database.onedice_group.all().values_list("id", flat=True)
        for groupId in groupList:
            if not await dataSource.checkExist_group(groupId):
                await dbUtils.pullGroupData(groupId)
        # 检查角色数据
        characterList = await database.onedice_character.all().values_list("id", flat=True)
        for cardId in characterList:
            if not await dataSource.checkExist_character(cardId):
                await dbUtils.pullCharacterData(cardId)

        logger.info("[onedice] 本地数据文件检查成功")
    except Exception:
        logger.error("[onedice] 本地数据文件检查失败！")


async def pullAll():
    # 主动进行一次本地文件数据检查
    await checkLocalData()


async def rollbackAll():
    # 强制将数据库覆盖到本地数据
    return


async def pushAll():
    """
    # 主动进行本地数据备份，先检查本地数据，pull后再push
    # 依次扫描本地文件，将全部数据整理为dic依次push
    """
    await checkLocalData()
    # 用户
    userFiles = await dataSource.getAllUsersDataFile()
    # 群组
    groupFiles = await dataSource.getAllGroupsDataFile()
    # 角色
    cardFiles = await dataSource.getAllCharactersDataFile()
    for name in userFiles:
        userId = name.replace(".json", "").strip()
        if userId == "":
            continue
        userInfo = await dataSource.getUserInfo(userId)
        userInfo['id'] = userId
        await dbUtils.saveOrUpdateById(database.onedice_user, userId, userInfo)
    for name in groupFiles:
        groupId = name.replace(".json", "").strip()
        if groupId == "":
            continue
        groupInfo = await dataSource.getGroupInfo(groupId)
        groupInfo['id'] = groupId
        await dbUtils.saveOrUpdateById(database.onedice_group, groupId, groupInfo)
    for name in cardFiles:
        cardId = name.replace(".json", "").strip()
        if cardId == "":
            continue
        cardInfo = await dataSource.getCharacter(cardId)
        cardInfo['id'] = cardId
        await dbUtils.saveOrUpdateById(database.onedice_character, cardId, cardInfo)
    logger.warning("[onedice] 已完成数据备份")


@scheduler.scheduled_job(
    "interval",
    hours=1
)
async def pushLogsAll():
    """
    # 每小时进行一次日志备份
    # 先查出logs/temp下全部的群聊文件夹
    # for群聊查到全部的csvName -> data = await logsUtil.readFromCSV(groupId, csvName)
    # update_or_create
    """
    logger.warning("[onedice] 正在同步本地日志文件")

    groups = await dataSource.getLogsTempGroups()
    for groupId in groups:
        files = await dataSource.getLogsTempName(groupId)
        for file in files:
            file = file.replace(".csv", "").strip()
            if file == "":
                continue
            data = await logsUtil.readFromCSV(groupId, file)
            await dbUtils.pushLogsData(data)
    logger.warning("[onedice] 同步本地日志文件完成")
