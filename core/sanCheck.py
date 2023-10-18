import re
from ..core import ra
from ..sub.custom import reply
from ..em.msgCode import msgCode
from ..template import propDic
from ..utils import calculate as cal
from ..utils import dice as dice
from ..utils import data as dataSource
from ..core.aspect import rd_before


@rd_before
async def sc(cmdStr, msgData, bot):
    a2 = ""
    b2 = ""
    # 判断格式
    slashes = re.findall(r'[/|]', cmdStr)
    if len(slashes) != 1:
        return reply(msgCode.ILLEGAL_FORMAT.name, msgData)
    split = re.split(r'[/|]', cmdStr)
    successReduce = split[0]
    failReduce = split[1]
    # 拆分
    # equation = ""
    if len(re.findall("d", successReduce)) == 1:
        # equation = rf"({successReduce})"
        sp = re.split("d", successReduce)
        a1 = sp[0]
        a2 = sp[1]
    else:
        a1 = successReduce
    if len(re.findall("d", failReduce)) == 1:
        # equation = rf"({failReduce})"
        sp = re.split("d", failReduce)
        b1 = sp[0]
        b2 = sp[1]
    else:
        b1 = failReduce

    # 检定
    raCal = await ra.doRaCal("灵感", msgData)
    card = await dataSource.getCurrentCharacter(msgData['userId'], msgData['groupId'])
    san = card['prop']['san']
    cardId = raCal["cardId"]
    pcname = raCal["pcname"]
    intelligent = raCal["propValue"]
    checkNum = raCal["checkNum"]
    ruleType = raCal["ruleType"]
    raResult = await ra.checkResult(intelligent, checkNum, ruleType)
    checkStr = await ra.getCheckStrAndRecord(raResult, msgData)
    if raResult <= 4:
        # 成功减少
        # 大成功
        if raResult == 1:
            resultReduce = a1
            ext1 = rf"{a1}"
        else:
            if not a2 == "":
                xdy = await dice.xdy(a1, a2)
                resultReduce = xdy["result"]
                ext1 = rf"{a1}d{a2}={resultReduce}"
            else:
                resultReduce = a1
                ext1 = rf"{resultReduce}"
    else:
        # 失败减少
        # 大失败
        if raResult == 6:
            resultReduce = int(b1)
            if not b2 == "":
                resultReduce = int(b1) * int(b2)
            ext1 = rf"{resultReduce}"
        else:
            if not b2 == "":
                xdy = await dice.xdy(b1, b2)
                resultReduce = xdy["result"]
                ext1 = rf"{b1}d{b2}={resultReduce}"
            else:
                resultReduce = b1
                ext1 = rf"{resultReduce}"
    # resultReduce {'equation': '(3+1)', 'result': '4'}
    san = int(san) - int(resultReduce)
    result = rf"{checkNum}/{intelligent}[{checkStr}]"
    ext2 = rf"{san}"
    # 保存
    await dataSource.updateCharacterProp(cardId, alias, san)

    if raResult <= 4:
        if raResult == 1:
            return await reply(msgCode.SC_CHECK_GREAT_SUCCESS.name, msgData, pcname=pcname, result=result, ext1=ext1,
                               ext2=ext2)
        else:
            return await reply(msgCode.SC_CHECK_SUCCESS.name, msgData, pcname=pcname, result=result, ext1=ext1,
                               ext2=ext2)
    else:
        if raResult == 6:
            return await reply(msgCode.SC_CHECK_GREAT_FAIL.name, msgData, pcname=pcname, result=result, ext1=ext1,
                               ext2=ext2)
        else:
            return await reply(msgCode.SC_CHECK_FAIL.name, msgData, pcname=pcname, result=result, ext1=ext1, ext2=ext2)
