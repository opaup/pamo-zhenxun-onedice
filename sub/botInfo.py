# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/23
import os
import psutil
import platform
from ..utils import data as dataSource

project_name = "zhenxun-onedice"
plugin_version = "0.4.9-preview"
project_address = "https://github.com/opaup/pamo-zhenxun-onedice"

async def botInfo(msgData, bot):
    friendList = await bot.get_friend_list()
    groupList = await bot.get_group_list()
    friendNum = len(friendList)
    groupNum = len(groupList)
    nickname = dataSource.NICKNAME

    # 获取操作系统信息和磁盘使用情况
    # system_info = platform.system()
    # release_info = platform.release()
    disk_usage = psutil.disk_usage("/")
    memory_info = psutil.virtual_memory()
    storage_used = (disk_usage.used / disk_usage.total) * 100
    memory_used = (memory_info.used / memory_info.total) * 100
    storage_used = f"{storage_used:.2f}"
    memory_used = f"{memory_used:.2f}"
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_used = f"{cpu_usage:.2f}"
    if msgData.msgType == "group":
        location = f"群聊： {msgData.groupName}({msgData.groupId})"
    else:
        location = f"私聊： {msgData.username}({msgData.userId})"
    statusList = await dataSource.getGroupStatusList()
    openingNum = 0
    noticeNum = 0
    for groupId, groupInfo in statusList.items():
        if "onOff" in groupInfo:
            openingNum += 1 if groupInfo["onOff"] == "on" else 0
            if "isNotice" in groupInfo:
                noticeNum += 1 if groupInfo["isNotice"] == "on" else 0

    resultMsg = (
        f"[{project_name}]\n"
        f"当前位于{location}\n"
        f"目前版本：{plugin_version}\n"
        f"使用 真寻帮助 获取其他功能的菜单\n"
        f"使用 .dice on 开启骰功能\n"
        f"使用 .dice off 关闭骰功能\n"
        f"使用 .help normal 获取一般指令帮助\n"
        f"使用 .help sub 获取附属指令帮助\n"
        f"使用 .help dice 获取骰设置指令帮助\n"
        f"使用 .help other 获取其他指令帮助\n"
        f"项目地址：{project_address}\n"
        f"——————————\n"
        f"{nickname}目前拥有{friendNum}个好友与{groupNum}个群组。\n"
        f"目前有{openingNum}个群组处于开启状态，其中{noticeNum}个群组开启了扩散功能\n"
        # f"当前操作系统：{system_info} {release_info}\n"
        f"硬盘占用：{storage_used}% 内存占用：{memory_used}% CPU占用：{cpu_used}%"
    )
    return resultMsg
