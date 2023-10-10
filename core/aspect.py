import asyncio
import random
from functools import wraps
from sub.custom import reply


# 为roll点检定添加延迟骰（后期添加群组的独立开关选项
# 让掷骰结果有一个等待的过程而不是立刻出值，增加趣味性
def rd_before(func):
    @wraps(func)
    async def wrapper(cmdStr, msgData, *args, **kwargs):
        result = await reply("RD_BEFORE", msgData)
        print(result)
        await asyncio.sleep(2)
        return await func(cmdStr, msgData, *args, **kwargs)

    return wrapper
