# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/20
import csv
import sys
import time
import shutil
from .data import logsPath, logsTempPath
from pathlib import Path


async def writeIntoCSV(groupId, logName, row):
    """
    将一行log，写入到目标临时csv文件中
    list固定顺序：类型type 发送者id pcname 消息内容/事件描述 消息/事件id 时间戳
    # typeName, messageId, timestamp, message, userId, pcname
    """
    tempFile = f"{logName}.csv"
    tempPath = logsTempPath / groupId
    tempPath.mkdir(parents=True, exist_ok=True)
    tempUrl = tempPath / tempFile
    with open(tempUrl, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        f.close()


async def readFromCSV(groupId, logName):
    """
    返回：字典[行数(int)] - 一个key-value对应一行
    'typeName': row[0],
    'messageId': row[1],
    'timestamp': row[2],
    'message': row[3],
    'userId': row[4],
    'pcname': row[5]
    """
    tempFile = f"{logName}.csv"
    tempPath = logsTempPath / groupId
    tempUrl = tempPath / tempFile
    with open(tempUrl, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data = {}
        for i, row in enumerate(reader):
            data[i + 1] = {
                'typeName': row[0],
                'messageId': row[1],
                'timestamp': row[2],
                'message': row[3],
                'userId': row[4],
                'pcname': row[5]
            }
    return data


async def putToTxt(groupId, logName, logData):
    """
    整理进txt文件
    """
    file = f"{logName}.txt"
    path = logsPath / "sorted" / groupId
    path.mkdir(parents=True, exist_ok=True)
    filePath = path / file
    with open(filePath, 'w', encoding='utf-8') as f:
        for idx, record in logData.items():
            timestamp = int(record['timestamp'])
            msgStr = record['message']
            pcname = record['pcname']
            msgTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            line = f"({msgTime}){pcname}: {msgStr}\n"
            f.write(line)
    return filePath

def getCsvPath(groupId, logName):
    return logsTempPath / groupId / f"{logName}.csv"


async def writeToNewCSV(groupId, logName, data):
    """
    将从readFromCSV读出的全部信息一次性写入一个新的CSV文件
    """
    fileName = f"{logName}.csv"
    tempPath = logsTempPath / groupId
    tempUrl = tempPath / fileName
    tempPath.mkdir(parents=True, exist_ok=True)

    with open(tempUrl, 'w', encoding='utf-8-sig', newline='') as new_f:
        writer = csv.writer(new_f)
        for _, row_data in data.items():
            writer.writerow([row_data['typeName'],
                             row_data['messageId'],
                             row_data['timestamp'],
                             row_data['message'],
                             row_data['userId'],
                             row_data['pcname']])
    return tempUrl
