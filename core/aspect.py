import asyncio
import random
from ..em.msgCode import msgCode
from functools import wraps
from ..sub.custom import reply


# 为roll点检定添加延迟骰（后期添加群组的独立开关选项
# 让掷骰结果有一个等待的过程而不是立刻出值，增加趣味性
def rd_before(func):
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
