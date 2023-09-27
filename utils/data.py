from pathlib import Path
import template.jsonTemplate as jsonTemplate
import importlib.util as importlibUtil
import json

USERNAME = ""
USERID = ""
GROUPID = ""
NICKNAME = ""

datePath = Path() / "data" / "pdice"
# 卡数据
characterPath = datePath / "character"
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
    characterPath.mkdir(parents=True, exist_ok=True)
    customPath.mkdir(parents=True, exist_ok=True)
    statusPath.mkdir(parents=True, exist_ok=True)
    statisticsPath.mkdir(parents=True, exist_ok=True)
    logsPath.mkdir(parents=True, exist_ok=True)

    if not botJsonPath.exists():
        create_bot(botJsonPath)
    if not msgJsonPath.exists():
        create_msg(msgJsonPath)


def supple(msgPath, msg):
    with open(msgPath, 'r', encoding='utf-8') as f:
        oldJson = json.load(f)
    oldJson[msg] = jsonTemplate.msgDefaultJson[msg]
    with msgPath.open('w', encoding='utf-8') as f:
        json.dump(oldJson, f, indent=4, ensure_ascii=False)
    return oldJson[msg]


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


def getUserInfo(userPath):
    return


def getGroupInfo(groupId):
    groupPath = statusPath / (groupId + ".json")
    if not groupPath.exists():
        createGroupInfo(groupPath)
    with open(groupPath, 'r', encoding='utf-8') as f:
        groupInfo = json.load(f)
    return groupInfo


def getCharacter(cardId):
    return


def getCurrentCharacter(userId, groupId):
    # 角色卡默认是全局的，如果群有设置，则优先取群的
    return


def refreshUser():
    global USERNAME, USERID, GROUPID
    USERNAME = "绪山美波里"
    USERID = "12138"
    GROUPID = "114514"


load_path()
loadNickName()
