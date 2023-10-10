import re
import utils.dice as dice
import utils.calculate as cal
from core import ra
from sub.custom import reply
from em.msgCode import msgCode
from template import propDic
import utils.data as dataSource


async def sc(cmdStr, msgData):
    a1 = ""
    a2 = ""
    b1 = ""
    b2 = ""
    propValue = "0"
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
    propName = "san"
    raCal = ra.doRaCal(propName, msgData)
    cardId = raCal["cardId"]
    pcname = raCal["pcname"]
    propValue = raCal["propValue"]
    checkNum = raCal["checkNum"]
    ruleType = raCal["ruleType"]
    oldPropValue = propValue
    raResult = await ra.checkResult(propValue, checkNum, ruleType)
    checkStr = ra.getCheckStrAndRecord(raResult, msgData)
    if raResult <= 4:
        # 成功减少
        # 大成功
        if raResult == 1:
            resultReduce = a1
            ext1 = rf"{a1}"
        else:
            resultReduce = await dice.xdy(a1, a2)["result"]
            ext1 = rf"{a1}d{a2}={resultReduce}"
    else:
        # 失败减少
        # 大失败
        if raResult == 6:
            resultReduce = int(b1) * int(b2)
            ext1 = rf"{resultReduce}"
        else:
            resultReduce = await dice.xdy(b1, b2)["result"]
            ext1 = rf"{b1}d{b2}={resultReduce}"

    # resultReduce {'equation': '(3+1)', 'result': '4'}
    propValue = int(propValue) - int(resultReduce)
    result = rf"{checkNum}/{oldPropValue}[{checkStr}]"
    ext2 = rf"{propValue}"
    # 保存
    propAlias = propDic.propName["san"]
    for alias in propAlias:
        await dataSource.saveCharacterProp(cardId, alias, propValue)

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
