from pathlib import Path
from ..template.propDic import propName
from ..template import jsonTemplate as jsonTemplate
import importlib.util as importlibUtil
import os
import json
import asyncio

NICKNAME = ""
SUPERUSERS = ['525915186']
# 配置目录
configsPath = Path() / "configs"
# pdice配置
configPath = configsPath / "pdice_configs.json"
# 数据目录
datePath = Path() / "data" / "pdice"
# 用户数据
usersPath = datePath / "users"
# 卡数据
charactersPath = datePath / "character"
# 自定义
customPath = datePath / "custom"
# 状态
statusPath = datePath / "status"
# 统计
statisticsPath = datePath / "statistics"
# 日志记录
logsPath = datePath / "logs"
# 临时日志
logsTempPath = logsPath / "temp"

msgJsonPath = customPath / "msg.json"

botJsonPath = customPath / "bot.json"


# 如果为真寻bot，则优先加载真寻bot配置文件中的nickname
async def loadNickName():
    try:
        zhenxunConfig = "configs.config"
        if importlibUtil.find_spec(zhenxunConfig):
            from configs.config import NICKNAME as zhenxun
            global NICKNAME
            NICKNAME = zhenxun
    except ImportError:
        NICKNAME = ""


async def load_path():
    charactersPath.mkdir(parents=True, exist_ok=True)
    usersPath.mkdir(parents=True, exist_ok=True)
    customPath.mkdir(parents=True, exist_ok=True)
    statusPath.mkdir(parents=True, exist_ok=True)
    statisticsPath.mkdir(parents=True, exist_ok=True)
    logsPath.mkdir(parents=True, exist_ok=True)
    logsTempPath.mkdir(parents=True, exist_ok=True)
    configsPath.mkdir(parents=True, exist_ok=True)

    if not botJsonPath.exists():
        await create_bot(botJsonPath)
    if not msgJsonPath.exists():
        await create_msg(msgJsonPath)


async def suppleMsg(msgPath, msg):
    with open(msgPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[msg] = jsonTemplate.msgDefaultJson[msg]
    with msgPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[msg]


async def suppleUser(userPath, item):
    with open(userPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[item] = jsonTemplate.userDefaultJson[item]
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[item]


async def suppleGroup(groupPath, item):
    with open(groupPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[item] = jsonTemplate.groupDefaultJson[item]
    with groupPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[item]


async def suppleConfigs(item):
    with open(configPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[item] = jsonTemplate.configDefaultJson[item]
    with configPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[item]


async def create_bot(bot_path):
    with bot_path.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.botDefaultJson, f, indent=4, ensure_ascii=False)


async def create_msg(msg_path):
    with msg_path.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.msgDefaultJson, f, indent=4, ensure_ascii=False)


async def create_configs():
    with configPath.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.configDefaultJson, f, indent=4, ensure_ascii=False)


async def getDiceType(groupId):
    groupInfo = await getGroupInfo(groupId)
    diceType = groupInfo['diceType']
    return diceType


async def createGroupInfo(groupPath):
    with groupPath.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.groupDefaultJson, f, indent=4, ensure_ascii=False)


async def createUserInfo(userPath):
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.userDefaultJson, f, indent=4, ensure_ascii=False)


async def getUserInfo(userId):
    userPath = usersPath / (userId + ".json")
    if not userPath.exists():
        await createUserInfo(userPath)
    with open(userPath, 'r', encoding='utf-8') as f:
        userInfo = json.load(f)
    return userInfo


async def getGroupInfo(groupId):
    groupPath = statusPath / (groupId + ".json")
    if not groupPath.exists():
        await createGroupInfo(groupPath)
    with open(groupPath, 'r', encoding='utf-8') as f:
        groupInfo = json.load(f)
    return groupInfo


async def getGroupStatusList():
    """获取已存在于本地的群组状态列表-json(dict)格式，key为groupId，value为groupInfo的格式"""
    statusFiles = os.listdir(statusPath)
    statusList = {}
    for file in statusFiles:
        groupId = file.replace(".json", "")
        groupInfo = await getGroupInfo(groupId)
        statusList[groupId] = groupInfo
    return statusList


async def getConfigInfo():
    if not configPath.exists():
        await create_configs()
    with open(configPath, 'r', encoding='utf-8') as f:
        configInfo = json.load(f)
    return configInfo


async def getCharacter(cardId):
    if cardId == "":
        return {}
    characterPath = charactersPath / (cardId + ".json")
    if not characterPath.exists():
        return {}
    with open(characterPath, 'r', encoding='utf-8') as f:
        characterInfo = json.load(f)
    return characterInfo


async def getCurrentCharacter(userId, groupId=""):
    """
    获取user当前的角色卡
    角色卡默认是全局的，如果有在该群设置cardLock，则优先取群lock的
    没有找到卡返回{}
    """
    if not groupId == "":
        cardLock = await getGroupItem(groupId, "cardLock")
        if userId in cardLock:
            characterId = cardLock[userId]
        else:
            characterId = await getUserItem(userId, "currentCard")
    else:
        characterId = await getUserItem(userId, "currentCard")
    characterInfo = await getCharacter(characterId)
    return characterInfo


async def getGroupItem(groupId, item):
    """
    不存在时为新的默认值/默认值查看template
    """
    userInfo = await getGroupInfo(groupId)
    if item not in userInfo:
        groupPath = statusPath / (groupId + ".json")
        userInfo[item] = await suppleGroup(groupPath, item)
    return userInfo[item]


async def getUserItem(userId, item):
    userInfo = await getUserInfo(userId)
    if item not in userInfo:
        userPath = usersPath / (userId + ".json")
        userInfo[item] = suppleUser(userPath, item)
    return userInfo[item]


async def getConfigItem(item):
    configInfo = await getConfigInfo()
    if item not in configInfo:
        configInfo[item] = suppleConfigs(item)
    return configInfo[item]


async def updateUserItem(userId, item, value):
    """
    覆盖原来的保存新的item
    """
    userInfo = await getUserInfo(userId)
    userInfo[item] = value
    userPath = usersPath / (userId + ".json")
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(userInfo, f, indent=4, ensure_ascii=False)


async def saveUserInfo(userId, value):
    """
    覆盖原来的保存新的Info
    """
    userInfo = value
    userPath = usersPath / (userId + ".json")
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(userInfo, f, indent=4, ensure_ascii=False)


async def saveGroupInfo(groupId, value):
    """
    覆盖原来的保存新的Info
    """
    groupInfo = value
    groupPath = statusPath / (groupId + ".json")
    with groupPath.open('w', encoding='utf-8') as f:
        json.dump(groupInfo, f, indent=4, ensure_ascii=False)


async def createCharacter(newId, newJson):
    characterPath = charactersPath / (newId + ".json")
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(newJson, f, indent=4, ensure_ascii=False)


async def saveCharacterProp(cardId, prop, value):
    """
    覆盖原来的保存新的prop
    """
    characterPath = charactersPath / (cardId + ".json")
    charactersInfo = await getCharacter(cardId)
    charactersInfo["prop"][prop] = value
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(charactersInfo, f, indent=4, ensure_ascii=False)


async def updateCharacterItem(cardId, item, value):
    characterPath = charactersPath / (cardId + ".json")
    charactersInfo = await getCharacter(cardId)
    charactersInfo[item] = value
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(charactersInfo, f, indent=4, ensure_ascii=False)


async def updateGroupItem(groupId, item, value):
    groupPath = statusPath / (groupId + ".json")
    groupInfo = await getGroupInfo(groupId)
    groupInfo[item] = value
    with groupPath.open('w', encoding='utf-8') as f:
        json.dump(groupInfo, f, indent=4, ensure_ascii=False)


async def updateCharacterProp(cardId, prop, value):
    """
    更新角色的指定属性为指定值。
    会同时更新保存在propDic中的其他别名的值
    """
    key = ""
    for standard_key, aliases in propName.items():
        if prop in aliases:
            key = standard_key
            break
    if not key == "":
        propAlias = propName[key]
        for alias in propAlias:
            await saveCharacterProp(cardId, alias, value)
    else:
        await saveCharacterProp(cardId, prop, value)


async def getGroupIdAndName(msgData):
    groupId = ""
    groupName = ""
    # if msgData["msgType"] == "group":
    # msgData
    return


async def checkExist_user(userId):
    filePath = usersPath / (userId + ".json")
    return os.path.isfile(filePath)


async def checkExist_group(groupId):
    filePath = statusPath / (groupId + ".json")
    return os.path.isfile(filePath)


async def checkExist_character(cardId):
    filePath = charactersPath / (cardId + ".json")
    return os.path.isfile(filePath)


async def getAllUsersDataFile():
    fileList = []
    # 使用os.listdir()获取指定文件夹下的所有文件和子文件夹
    for filename in os.listdir(usersPath):
        fileList.append(filename)
    return fileList


async def getAllGroupsDataFile():
    fileList = []
    # 使用os.listdir()获取指定文件夹下的所有文件和子文件夹
    for filename in os.listdir(statusPath):
        fileList.append(filename)
    return fileList


async def getAllCharactersDataFile():
    fileList = []
    # 使用os.listdir()获取指定文件夹下的所有文件和子文件夹
    for filename in os.listdir(charactersPath):
        fileList.append(filename)
    return fileList


async def getLogsTempGroups():
    groups = []
    for groupId in os.listdir(logsTempPath):
        groups.append(groupId)
    return groups


async def getLogsTempName(groupId):
    fileList = []
    for filename in os.listdir(logsTempPath / groupId):
        fileList.append(filename)
    return fileList


asyncio.run(load_path())
asyncio.run(loadNickName())
