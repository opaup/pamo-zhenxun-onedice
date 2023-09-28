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
    "SAVE_CARD_SUCCESS": "已为[{USERNAME}]成功创建角色卡：{RESULT}",
    "UPDATE_CARD_SUCCESS": "{RESULT}的值是⑨是吗？{NICKNAME}记住了！",
    "SWITCH_CARD_SUCCESS": "[{USERNAME}]已切换到身份：{RESULT}",
    "NOT_FOUND_CARD": "从[{USERNAME}]的包包里找不到名为{RESULT}的卡哦（？）",
    "CARD_NAME_TOO_LONG": "目前规定单卡昵称不应大于18字",
    "CARD_IN_GROUP_LOCKED": "已在本群锁卡。无法切换",
    "ROLL_FAIL": "掷骰出错了",
    "ROLL_CHECK_SUCCESS": "{NICKNAME}为[{PCNAME}]进行{EXT1}检定：{RESULT}【{EXT2}】",
    "ROLL_CHECK_HARD_SUCCESS": "{NICKNAME}为[{PCNAME}]进行{EXT1}检定：{RESULT}【{EXT2}】",
    "ROLL_CHECK_EXT_HARD_SUCCESS": "{NICKNAME}为[{PCNAME}]进行{EXT1}检定：{RESULT}【{EXT2}】",
    "ROLL_CHECK_GREAT_SUCCESS": "{NICKNAME}为[{PCNAME}]进行{EXT1}检定：{RESULT}【{EXT2}】",
    "ROLL_CHECK_FAIL": "{NICKNAME}为[{PCNAME}]进行{EXT1}检定：{RESULT}【{EXT2}】",
    "ROLL_CHECK_GREAT_FAIL": "{NICKNAME}为[{PCNAME}]进行{EXT1}检定：{RESULT}【{EXT2}】",
    "SC_CHECK_SUCCESS": "[{PCNAME}]进行san检定：{RESULT}\n扣除san值：{EXT1} 剩余san值：{EXT2}",
    "SC_CHECK_GREAT_SUCCESS": "[{PCNAME}]进行san检定：{RESULT}\n扣除san值：{EXT1} 剩余san值：{EXT2}",
    "SC_CHECK_FAIL": "[{PCNAME}]进行san检定：{RESULT}\n扣除san值：{EXT1} 剩余san值：{EXT2}",
    "SC_CHECK_GREAT_FAIL": "[{PCNAME}]进行san检定：{RESULT}\n扣除san值：{EXT1} 剩余san值：{EXT2}",
}

groupDefaultJson = {
    "onOff": "on",
    "diceType": "100",
    "ruleType": "1",
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
