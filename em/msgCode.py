from enum import Enum


class msgCode(Enum):
    NO_COMMAND = ("NO_COMMAND", "无该指令返回")
    NO_ACHIEVE_CMD = ("NO_ACHIEVE_CMD", "该指令功能尚未完成")
    ILLEGAL_FORMAT = ("ILLEGAL_FORMAT", "格式非法")
    RD_ILLEGAL_FORMAT = ("RD_ILLEGAL_FORMAT", "RD格式非法")
    RD_RESULT = ("RD_RESULT", "RD结果")
    MAKE_CARD_COC7 = ("MAKE_CARD_COC7", "角色卡作成")
    NO_CARD = ("NO_CARD", "用户没有角色卡信息")
    SAVE_CARD_SUCCESS = ("SAVE_CARD_SUCCESS", "成功保存角色卡")
