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
    "NOT_FOUND_CARD_PROP": "从[{RESULT}]的身体里找不到名为【{EXT1}】的属性哦！",
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
    "RD_BEFORE": "转动命运的齿轮，拨开眼前迷雾...|启动吧，命运的水晶球，为[{USERNAME}]指引方向！|嗯哼，在此刻转动吧！命运之轮！|{NICKNAME}在此祈愿，请为[{USERNAME}]降下指引...",
    "SHOW_CARD_INFO": "正在查看[{USERNAME}]的角色卡：{PCNAME}\n{RESULT}",
    "SHOW_CARD_LIST": "正在查看[{USERNAME}]的角色卡列表：\n{RESULT}",
    "RH_TO_PRIVATE": "你在群聊[{EXT1}]进行了暗骰检定：{RESULT}",
    "RH_TO_GROUP": "咕噜噜，[{PCNAME}]发动了暗骰检定！",
    "SENDER_NOT_FROM_GROUP": "只有在群聊中才可以使用暗骰哦~",
    "RP_OR_RB_FORMAT_FAIL": "rp或rb的指令后必须跟10以内的数字哦。",
    "DICE_SET_NOT_ADMIN": "只有群主或管理员才可以使用该指令哦！",
    "DICE_SET_HELP": "定义格式： group 字段名 value\ndice on/off 开关骰功能\ndice set x  设置默认骰\ndice isNotice on/off    "
                     "设置是否为公告群\ndice secret on/off    设置是否开启秘密团模式\ndice mode coc/dnd/其他    设置骰模式\ndice rule x "
                     "设置房规\n------附加内容------\n默认房规，当值小于50时，1大成功，98-100大失败，大于50时，1-3大成功，100大失败",
    "DICE_SET_ON": "骰功能已开启",
    "DICE_SET_OFF": "骰功能已关闭",
    "DICE_SET_SECRET_ON": "已开启秘密团模式",
    "DICE_SET_SECRET_OFF": "已关闭秘密团模式",
    "DICE_SET_ISNOTICE_ON": "已开启本群为团贴公告扩散群",
    "DICE_SET_ISNOTICE_OFF": "已关闭本群为团贴公告扩散群",
    "DICE_SET_MODE": "已设置DICE默认模式为：{RESULT}",
    "DICE_SET_RULE": "已设置本群默认房规为：{RESULT}{EXT1}",
    "DICE_SET_DICETYPE": "已设置本群默认DICE为：{RESULT}",
    "ST_HELP": "",
    "GROUP_NO_ONE": "唔？你说的是谁？群里边有 {RESULT} 这个人吗？",
    "TEAM_NO_ONE": "唔？你说的是谁？队里边有 {RESULT} 这个人吗？",
    "TEAM_ADD_SUCCESS": "已将{RESULT}添加到本群队伍中",
    "TEAM_RM_SUCCESS": "已将{RESULT}从本群队伍中移除",
    "TEAM_IN_LOCK": "{EXT1}已锁定角色卡[{PCNAME}]，请先解锁角色卡",
    "TEAM_LIST": "当前队伍列表：\n{RESULT}",
    "TEAM_SHOW": "{PCNAME}的属性如下：\n{RESULT}",
    "TEAM_CLR": "{RESULT}的队伍已清空",
    "TEAM_CALL": "{NICKNAME}正在帮助[{USERNAME}]释放鸽子召唤术！\n{RESULT}",
    "TEAM_PROP": "将[{PCNAME}]的{EXT1}调整为：{RESULT}",
    "TEAM_LOCK_SUCCESS": "已将队伍中的全部角色卡锁定！",
    "TARGET_USER_NOT_HAVE_CARD": "[{EXT1}]还没有选择好角色卡哦。",
}

groupDefaultJson = {
    "onOff": "on",
    "diceMode": "coc",
    "diceType": "100",
    "ruleType": "1",
    "isNotice": "off",
    "secretMode": "off",
    "cardLock": {},
    "teamList": []
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
