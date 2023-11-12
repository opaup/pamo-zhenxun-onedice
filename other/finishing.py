# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/31
import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import bot, MessageEvent

钓鱼_handler = on_command(cmd="钓鱼", priority=5, block=True)
摸鱼_handler = on_command(cmd="摸鱼", priority=5, block=True)
烤鱼_handler = on_command(cmd="烤鱼", priority=5, block=True)
卖鱼_handler = on_command(cmd="卖鱼", priority=5, block=True)

@钓鱼_handler.handler()
async def finishing():
    return
