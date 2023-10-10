import re


async def replaceCmdByDic(msgStr, dic):
    pattern = r'\b({})\b'.format('|'.join(dic))
    msgStr = re.sub(pattern, "", msgStr, count=1).strip()
    return msgStr
