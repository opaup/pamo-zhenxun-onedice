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


def fromStrGetUserId(msgStr):
    """
    获取单个userId，该字符串需包含有效cq:at或userId数字
    """
    cqCodePattern = r'\[(.+?)\]'
    idPattern = r'\d+'
    willAddIds = []
    if re.search(cqCodePattern, msgStr):
        willAddIds = re.findall(cqCodePattern, msgStr)
    elif re.search(idPattern, msgStr):
        willAddIds = re.findall(idPattern, msgStr)
    return fromAtGetId(willAddIds[0])


