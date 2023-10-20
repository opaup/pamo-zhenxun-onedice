import asyncio
import random
from ..em.msgCode import msgCode
from functools import wraps
from ..sub.custom import reply
from aspectlib import weave
from services.log import logger


def rd_before(func):
    """
    为roll点检定添加延迟骰（后期添加群组的独立开关选项
    让掷骰结果有一个等待的过程而不是立刻出值，增加趣味性
    方法必须有 cmdStr, msgData, bot 参数传递
    """

    @wraps(func)
    async def wrapper(cmdStr, msgData, bot, *args, **kwargs):
        result = await reply(msgCode.RD_BEFORE.name, msgData)
        # print(result)
        if msgData['msgType'] == "group":
            await bot.send_group_msg(group_id=msgData['groupId'],
                                     message=result)
        else:
            await bot.send_private_msg(user_id=msgData['userId'],
                                       message=result)
        await asyncio.sleep(2)
        return await func(cmdStr, msgData, bot, *args, **kwargs)

    return wrapper


def team_operator_error(func):
    """
    捕获团队操作异常
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Caught exception in {func.__name__}: {e}")
            return "指令格式或内部逻辑错误，请通过.help获取帮助"

    return wrapper


def check_from_group(func):
    """
    确认是否来源于群聊
    """

    @wraps(func)
    async def wrapper(cmdStr, msgData, *args, **kwargs):
        if not msgData['msgType'] == 'group':
            return await reply(key=msgCode.SENDER_NOT_FROM_GROUP.name, msgData=msgData)
        return await func(cmdStr, msgData, *args, **kwargs)

    return wrapper


def check_from_admin():
    """
    确认发送者是否拥有admin权限
    """

    @wraps(func)
    async def wrapper(cmdStr, msgData, *args, **kwargs):
        return await func(cmdStr, msgData, *args, **kwargs)

    return wrapper


def log_recoder():
    """
    log记录：这里是主要记录dice操作
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        return

    return wrapper
