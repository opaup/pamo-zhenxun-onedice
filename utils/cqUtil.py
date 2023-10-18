import re


def atSomebody(idStr):
    """
    转义：at对应的id
    """
    return f"[CQ:at,qq={idStr}]"


def fromAtGetId(user):
    """
    解析：从CQ码中获取id，如传入的参数为纯数字则返回纯数字
    """
    if user[0] == '[' and user[-1] == ']':
        user = user[1:-1]
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
    willIds = []
    if re.search(cqCodePattern, msgStr):
        willIds = re.findall(cqCodePattern, msgStr)
    elif re.search(idPattern, msgStr):
        willIds = re.findall(idPattern, msgStr)
    return fromAtGetId(willIds[0])


