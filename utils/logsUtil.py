# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/20
import csv
from .data import logsPath, logsTempPath
from pathlib import Path

async def writeIntoCSV(groupId, logName, row):
    """
    将一行log，写入到目标临时csv文件中
    list固定顺序：类型type 发送者id pcname 消息内容/事件描述 消息/事件id 时间戳
    # typeName, id, timestamp, message, userId, pcname
    """
    tempFile = f"{groupId}_{logName}.csv"
    tempPath = logsTempPath / groupId
    tempPath.mkdir(parents=True, exist_ok=True)
    tempUrl = tempPath / tempFile
    with open(tempUrl, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        f.close()
