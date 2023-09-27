botDefaultJson = {
    "NICKNAME": "小真寻"
}

msgDefaultJson = {
    "NO_COMMAND": "{NICKNAME}没有这条指令",
    "NO_ACHIEVE_CMD": "{NICKNAME}没有实现这条指令",
    "ILLEGAL_FORMAT": "格式非法",
    "RD_ILLEGAL_FORMAT": "RD格式非法",
    "RD_RESULT": "{NICKNAME}为[{USERNAME}]掷出了：{RESULT}",
    "MAKE_CARD_COC7": "[{USERNAME}]的coc7th角色卡作成：\n{RESULT}",
    "NO_CARD": "[{USERNAME}]的包包中没有角色卡哦！",
    "SAVE_CARD_SUCCESS": "已为[{USERNAME}]成功创建角色卡：{RESULT}"
}

groupDefaultJson = {
    "onOff": "on",
    "diceType": "100",
    "isNotice": False,
    "cardLock": {}
}

userDefaultJson = {
    # 权限级别 0 无权限 1 normal 2 认证KP(允许发布团贴) 3 协管 4 骰主 默认为1
    "permissionLevel": 1,
    "pcCardId": 0,
    "successRollNum": 0,
    "failRollNum": 0,
    "greatSuccessRollNum": 0,
    "greatFailRollNum": 0,
    "currentCardName": "",
    "currentCard": "",
    "cardList": {}
}
