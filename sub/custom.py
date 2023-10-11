import json
import re
import random

from ..utils import data as dataSource

msgJsonPath = dataSource.msgJsonPath
botJsonPath = dataSource.botJsonPath

# 定义占位符字典
placeholders = {}


async def updatePlaceholders(msgData):
    with open(botJsonPath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        placeholders.update(data)
    with open(msgJsonPath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        placeholders.update(data)
    if dataSource.NICKNAME != "":
        data['NICKNAME'] = dataSource.NICKNAME
    if msgData["msgType"] == "group":
        data['GROUPNAME'] = msgData['groupName']
        data['GROUPID'] = msgData['groupId']
    if msgData['username'] != "":
        data['USERNAME'] = msgData['username']
    placeholders.update(data)


async def reply(key, msgData, result="", pcname="", ext1="", ext2=""):
    await updatePlaceholders(msgData)
    with open(msgJsonPath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if key not in data:
        data[key] = await dataSource.suppleMsg(msgJsonPath, key)
    text = data[key]
    if re.search("[|]", text):
        parts = text.split("|")
        text = random.choice(parts)
    value = await replace_placeholders(text, result, pcname, ext1, ext2)
    return value


# 替换占位符
async def replace_placeholders(text, result="", pcname="", ext1="", ext2=""):
    for placeholder, value in placeholders.items():
        placeholder_with_braces = "{" + placeholder + "}"
        text = text.replace(placeholder_with_braces, value)
        if result != "":
            text = text.replace("{RESULT}", result)
        if pcname != "":
            text = text.replace("{PCNAME}", pcname)
        if ext1 != "":
            text = text.replace("{EXT1}", ext1)
        if ext2 != "":
            text = text.replace("{EXT2}", ext2)
    return text


async def getReply(msgStr, msgData):
    return


async def updateReply(msgStr, msgData):
    return
