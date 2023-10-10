import asyncio
import random
from functools import wraps
from sub.custom import reply


def rd_before(func):
    @wraps(func)
    async def wrapper(cmdStr, msgData, *args, **kwargs):
        result = await reply("RD_BEFORE", msgData)
        print(result)
        await asyncio.sleep(0.6)
        return await func(cmdStr, msgData, *args, **kwargs)

    return wrapper
