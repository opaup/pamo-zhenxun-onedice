import nonebot.adapters.onebot.v11.bot as bot


async def rh(msgStr, msgData):

    await bot.Bot.send_msg(message_type='group', group_id=msgData['groupId'],
                           message='')
    await bot.Bot.send_msg(message_type='private', user_id=msgData['userId'],
                           message='')
    return
