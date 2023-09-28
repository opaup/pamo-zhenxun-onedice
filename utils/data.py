from pathlib import Path
import template.jsonTemplate as jsonTemplate
import importlib.util as importlibUtil
import json

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
def loadNickName():
    try:
        zhenxunConfig = "configs.config"
        if importlibUtil.find_spec(zhenxunConfig):
            from configs.config import NICKNAME as zhenxun
            global NICKNAME
            NICKNAME = zhenxun
    except ImportError:
        NICKNAME = ""


def load_path():
    charactersPath.mkdir(parents=True, exist_ok=True)
    usersPath.mkdir(parents=True, exist_ok=True)
    customPath.mkdir(parents=True, exist_ok=True)
    statusPath.mkdir(parents=True, exist_ok=True)
    statisticsPath.mkdir(parents=True, exist_ok=True)
    logsPath.mkdir(parents=True, exist_ok=True)

    if not botJsonPath.exists():
        create_bot(botJsonPath)
    if not msgJsonPath.exists():
        create_msg(msgJsonPath)


def suppleMsg(msgPath, msg):
    with open(msgPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[msg] = jsonTemplate.msgDefaultJson[msg]
    with msgPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[msg]


def suppleUser(userPath, item):
    with open(userPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[item] = jsonTemplate.userDefaultJson[item]
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[item]


def suppleGroup(groupPath, item):
    with open(groupPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[item] = jsonTemplate.groupDefaultJson[item]
    with groupPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[item]


def create_bot(bot_path):
    with bot_path.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.botDefaultJson, f, indent=4, ensure_ascii=False)


def create_msg(msg_path):
    with msg_path.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.msgDefaultJson, f, indent=4, ensure_ascii=False)


def getDiceType(groupId):
    return getGroupInfo(groupId)['diceType']


def createGroupInfo(groupPath):
    with groupPath.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.groupDefaultJson, f, indent=4, ensure_ascii=False)


def createUserInfo(userPath):
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(jsonTemplate.userDefaultJson, f, indent=4, ensure_ascii=False)


def getUserInfo(userId):
    userPath = usersPath / (userId + ".json")
    if not userPath.exists():
        createUserInfo(userPath)
    with open(userPath, 'r', encoding='utf-8') as f:
        userInfo = json.load(f)
    return userInfo


def getGroupInfo(groupId):
    groupPath = statusPath / (groupId + ".json")
    if not groupPath.exists():
        createGroupInfo(groupPath)
    with open(groupPath, 'r', encoding='utf-8') as f:
        groupInfo = json.load(f)
    return groupInfo


def getCharacter(cardId):
    characterPath = charactersPath / (cardId + ".json")
    if not characterPath.exists():
        return {}
    with open(characterPath, 'r', encoding='utf-8') as f:
        characterInfo = json.load(f)
    return characterInfo


def getCurrentCharacter(userId, groupId=""):
    # 角色卡默认是全局的，如果群有设置，则优先取群的
    if not groupId == "":
        cardLock = getGroupItem(groupId, "cardLock")
        if userId in cardLock:
            characterId = cardLock[userId]
        else:
            characterId = getUserItem(userId, "currentCard")
    else:
        characterId = getUserItem(userId, "currentCard")
    characterInfo = getCharacter(characterId)
    return characterInfo


def getGroupItem(groupId, item):
    userInfo = getGroupInfo(groupId)
    if item not in userInfo:
        groupPath = statusPath / (groupId + ".json")
        userInfo[item] = suppleGroup(groupPath, item)
    return userInfo[item]


def getUserItem(userId, item):
    userInfo = getUserInfo(userId)
    if item not in userInfo:
        userPath = usersPath / (userId + ".json")
        userInfo[item] = suppleUser(userPath, item)
    return userInfo[item]


def saveUserItem(userId, item, value):
    userInfo = getUserInfo(userId)
    userInfo[item] = value
    userPath = usersPath / (userId + ".json")
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(userInfo, f, indent=4, ensure_ascii=False)


def saveUserInfo(userId, value):
    userInfo = value
    userPath = usersPath / (userId + ".json")
    with userPath.open('w', encoding='utf-8') as f:
        json.dump(userInfo, f, indent=4, ensure_ascii=False)


def createCharacter(newId, newJson):
    characterPath = charactersPath / (newId + ".json")
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(newJson, f, indent=4, ensure_ascii=False)


def saveCharacterProp(cardId, prop, value):
    characterPath = charactersPath / (cardId + ".json")
    charactersInfo = getCharacter(cardId)
    charactersInfo["prop"][prop] = value
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(charactersInfo, f, indent=4, ensure_ascii=False)


def saveCharacterItem(cardId, item, value):
    characterPath = charactersPath / (cardId + ".json")
    charactersInfo = getCharacter(cardId)
    charactersInfo[item] = value
    with characterPath.open('w', encoding='utf-8') as f:
        json.dump(charactersInfo, f, indent=4, ensure_ascii=False)


def getGroupIdAndName(msgData):
    groupId = ""
    groupName = ""
    if msgData["msgType"] == "group":
        msgData
    return


load_path()
loadNickName()
