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
    UPDATE_CARD_SUCCESS = ("UPDATE_CARD_SUCCESS", "成功更新角色卡")
    SWITCH_CARD_SUCCESS = ("SWITCH_CARD_SUCCESS", "成功切换角色卡")
    NOT_FOUND_CARD = ("NOT_FOUND_CARD", "找不到角色卡")
    CARD_NAME_TOO_LONG = ("NOT_FOUND_CARD", "卡名过长")
    CARD_IN_GROUP_LOCKED = ("NOT_FOUND_CARD", "已在本群锁卡。无法切换")
