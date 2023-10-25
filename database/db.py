# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/24
import time
from . import backups
from ..utils import data as dataSource
from services.log import logger


# dice pull/push/(rollback)
# dataSource check superusers

async def pullAll(msgData):
    startTime = time.time()
    if msgData.userId not in dataSource.SUPERUSERS:
        return
    logger.warning(f"[onedice] [{msgData.username}({msgData.userId})]主动执行了pullAll指令")
    await backups.pullAll()
    endTime = time.time()
    spendTime = "{:.2f}秒".format(endTime - startTime)
    return f"已完成pull-all任务，耗时{spendTime}"

async def pushAll(msgData):
    startTime = time.time()
    if msgData.userId not in dataSource.SUPERUSERS:
        return
    logger.warning(f"[onedice] [{msgData.username}({msgData.userId})]主动执行了pushAll指令")
    await backups.pushAll()
    endTime = time.time()
    spendTime = "{:.2f}秒".format(endTime - startTime)
    return f"已完成push-all任务，耗时{spendTime}"


async def rollbackAll(msgData):
    startTime = time.time()
    if msgData.userId not in dataSource.SUPERUSERS:
        return
    logger.warning(f"[onedice] [{msgData.username}({msgData.userId})]主动执行了rollbackAll指令")
    await backups.rollbackAll()
    endTime = time.time()
    spendTime = "{:.2f}秒".format(endTime - startTime)
    return f"已完成rollback-all任务，耗时{spendTime}"


async def pushLogsAll(msgData):
    startTime = time.time()
    if msgData.userId not in dataSource.SUPERUSERS:
        return
    logger.warning(f"[onedice] [{msgData.username}({msgData.userId})]主动执行了pushLogsAll指令")
    await backups.pushLogsAll()
    endTime = time.time()
    spendTime = "{:.2f}秒".format(endTime - startTime)
    return f"已完成push-logs-all任务，耗时{spendTime}"
