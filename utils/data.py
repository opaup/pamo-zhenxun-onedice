from pathlib import Path
from template.propDic import propName
import template.jsonTemplate as jsonTemplate
import importlib.util as importlibUtil
import json
import asyncio

NICKNAME = ""

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
# 临时
tempPath = datePath / "temp"

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


async def create_bot(bot_path):
    with bot_path.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.botDefaultJson, f, indent=4, ensure_ascii=False)


async def create_msg(msg_path):
    with msg_path.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.msgDefaultJson, f, indent=4, ensure_ascii=False)


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


async def getCharacter(cardId):
    characterPath = charactersPath / (cardId + ".json")
    if not characterPath.exists():
        return {}
    with open(characterPath, 'r', encoding='utf-8') as f:
        characterInfo = json.load(f)
    return characterInfo


async def getCurrentCharacter(userId, groupId=""):
    # 角色卡默认是全局的，如果群有设置，则优先取群的
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


async def saveUserItem(userId, item, value):
    userInfo = await getUserInfo(userId)
    userInfo[item] = value
    userPath = usersPath / (userId + ".json")
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(userInfo, f, indent=4, ensure_ascii=False)


async def saveUserInfo(userId, value):
    userInfo = value
    userPath = usersPath / (userId + ".json")
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(userInfo, f, indent=4, ensure_ascii=False)


async def createCharacter(newId, newJson):
    characterPath = charactersPath / (newId + ".json")
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(newJson, f, indent=4, ensure_ascii=False)


async def saveCharacterProp(cardId, prop, value):
    characterPath = charactersPath / (cardId + ".json")
    charactersInfo = await getCharacter(cardId)
    charactersInfo["prop"][prop] = value
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(charactersInfo, f, indent=4, ensure_ascii=False)


async def saveCharacterItem(cardId, item, value):
    characterPath = charactersPath / (cardId + ".json")
    charactersInfo = await getCharacter(cardId)
    charactersInfo[item] = value
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(charactersInfo, f, indent=4, ensure_ascii=False)


async def updateMultiCharacterProp(cardId, prop, value):
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

asyncio.run(load_path())
asyncio.run(loadNickName())

