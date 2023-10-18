import re


def atSomebody(idStr):
    """
    转义：at对应的id
    """
    return f"[CQ:at,qq={idStr}]"


def fromAtGetId(s):
    """
    解析：从CQ码中获取id，如传入的参数为纯数字则返回纯数字
    """
    if s[0] == '[' and s[-1] == ']':
        s = s[1:-1]
    userId = re.search(r"qq=(\d+)", user)
    if userId:
        userId = userId.group(1)
    else:
        if user.isdigit():
            userId = user
        else:
            userId = ""
    return userId
