# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/23

import psutil
import platform
from ..utils import data as dataSource

project_name = "zhenxun-onedice"
plugin_version = 0.3


async def botInfo(msgData, bot):
    friendList = await bot.get_friend_list()
    groupList = await bot.get_group_list()
    friendNum = len(friendList)
    groupNum = len(groupList)
    nickname = dataSource.NICKNAME

    # 获取操作系统信息和磁盘使用情况
    system_info = platform.system()
    release_info = platform.release()
    disk_usage = psutil.disk_usage("/")
    memory_info = psutil.virtual_memory()
    storage_used = (disk_usage.used / disk_usage.total) * 100
    memory_used = (memory_info.used / memory_info.total) * 100
    storage_used = f"{storage_used:.2f}"
    memory_used = f"{memory_used:.2f}"
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_used = f"{cpu_usage:.2f}"
    if msgData.msgType == "group":
        location = f"(群聊) {msgData.groupName}({msgData.groupId})"
    else:
        location = f"(私聊) {msgData.username}({msgData.userId})"

    resultMsg = (
        f"[{project_name}]当前位置：{location}\n"
        f"目前版本：{plugin_version}-preview\n"
        f"使用 真寻帮助\t获取其他功能的菜单\n"
        f"使用 .help\t获取骰功能的帮助菜单\n"
        f"使用 .dice on\t开启骰功能\n"
        f"使用 .dice off\t关闭骰功能\n"
        f"项目地址：https://github.com/opaup/pamo-zhenxun-onedice\n"
        f"——————————\n"
        f"{nickname}目前拥有{friendNum}个好友与{groupNum}个群聊。\n"
        f"当前操作系统：{system_info} {release_info}\n"
        f"硬盘状态：{storage_used}% 内存占用：{memory_used}% CPU占用：{cpu_used}%"
    )
    return resultMsg
