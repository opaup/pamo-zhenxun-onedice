import nonebot
from nonebot import get_driver, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from .utils import data as dataSource
from .utils import eventUtil as eventUtil
from .sub import notice, recordLog, botInfo
from .flow import doFlow
from .models import MsgData
import asyncio

# 初始化
# load_path()

__zx_plugin_name__ = "DICE"
__plugin_usage__ = f"""
usage：
使用 .help 来查看相关帮助，前缀可以是 . 也可以是 。
快让小真寻担任新的骰娘吧！
（目前仅为预览版）
""".strip()
__plugin_des__ = f""
__plugin_cmd__ = ["."]
__plugin_type__ = ("功能", "工具")
__plugin_version__ = botInfo.plugin_version
__plugin_author__ = "opaup"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["。help"],
}


# 入口
# async def on_message(msg, msgData):
#     # msgData = {
#     # "msg": msg.replace(".", "").replace("。", ""),
#     # "username": "绪山美波里",
#     # "userId": "000000000",
#     # # "msgType": "private",
#     # "msgType": "group",
#     # "groupId": "114514",
#     # "groupName": "测试群",
#     # "isAdmin": False,
#     # }
#     result = await doFlow(msgData)
#     # 如果没有任何匹配的指令，则跳过
#     if type(result) == bool:
#         if result:
#             print("拦截且不回复")
#         if not result:
#             print("跳过拦截")
#     return result


# TODO 定时备份到数据库 || init时同步检测数据更新

# msgStr = ".dice help"
# print(asyncio.run(on_message(msgStr)))

response = on_command(
    ".", aliases={"。"}, priority=5, block=True
)


@response.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, msgData=MsgData.MsgData()):
    msg = str(event.message).replace(".", "").replace("。", "")
    username = event.sender.nickname
    # msgData = {
    #     "msg": msg,
    #     "username": username,
    #     "userId": str(event.sender.user_id),
    #     "msgType": event.message_type,
    #     "groupId": "",
    #     "groupName": "",
    #     "isAdmin": False,
    #     "sender": "user",
    #     "typeName": "message",
    #     "messageId": str(event.message_id),
    #     "timestamp": str(event.time),
    # }
    msgData.msg = msg
    msgData.username = username
    msgData.userId = str(event.sender.user_id)
    msgData.msgType = event.message_type
    msgData.groupId = ""
    msgData.groupName = ""
    msgData.isAdmin = False
    msgData.sender = "user"
    msgData.typeName = "message"
    msgData.messageId = str(event.message_id)
    msgData.timestamp = str(event.time)
    # 如果是群消息
    if msgData.msgType == "group":
        groupId = event.group_id
        msgData.groupId = str(groupId)
        msgData.groupName = await eventUtil.getGroupName(groupId, bot)
        # 是管理员或群主
        if event.sender.role == 'owner' or event.sender.role == 'admin':
            msgData.isAdmin = True
    result = await doFlow(msgData, bot)
    # 如果没有任何匹配的指令，则跳过
    if type(result) == bool:
        if result:
            await response.finish(None)
        if not result:
            await response.skip()
    else:
        await response.finish(result)
