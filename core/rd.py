from ..utils import dice as dice
from ..utils import calculate as cal
from ..sub.custom import reply
from ..em.msgCode import msgCode
from ..core.aspect import rd_before
from ..utils import data as dataSource
import re


# rd
@rd_before
async def rdFlow(cmdStr, msgData, bot):
    split = await rdSplit(cmdStr, msgData)
    a1 = split['a1']
    a2 = split['a2']
    b1 = split['b1']
    b2 = split['b2']
    operator = split['operator']
    diceType = split['diceType']
    extMsg = split['extMsg']
    return await getRdResult(a1=a1, a2=a2, b1=b1, b2=b2, operator=operator, diceType=diceType, extMsg=extMsg,
                             msgData=msgData)


async def rdSplit(cmdStr, msgData):
    diceType = "100"
    a1 = 0
    a2 = 0
    b1 = 0
    b2 = 0
    m = ""
    operator = ""
    extMsg = ""
    if msgData["msgType"] == "group":
        groupId = msgData["groupId"]
        diceType = await dataSource.getDiceType(groupId)
    cmdStr = re.sub("r", "", cmdStr, count=1)
    # 判断是否包含d，如包含，则取d之前的内容
    if cmdStr.find('d') != -1:
        # m = re.match(r'^.*d', cmdStr)
        split = cmdStr.split("d", 1)
        m = split[0]
        cmdStr = split[1]
        # 如果数字在d后面，而d前没数字，如rd20，则diceType=20
        # 判断cmdStr是否为纯数字，如是则diceType=它
        if re.search(r'[+\-*/]', cmdStr):
            operator = re.search(r'[+\-*/]', cmdStr).group()
            s = cmdStr.split(operator)
            if s[0].isdigit():
                diceType = s[0]
    else:
        if cmdStr != "":
            m = cmdStr
    # 如果m不为空，判断 m 是否为数字
    if cmdStr == "":
        # 空则默认1d默认Dice
        a1 = 1
        a2 = diceType
    else:
        try:
            a1 = int(m)
        except ValueError:
            a1 = 1
            extMsg = m
        finally:
            cmdStr = cmdStr.replace(m, "")
        # 判断是否存在附加表达式
        if not re.search(r'[+\-*/]', cmdStr):
            if cmdStr != "":
                a2 = int("".join(re.findall(r'\d+', cmdStr)))
                extMsg = re.findall(r'\D+', cmdStr)
            else:
                a2 = diceType
        else:
            operator = re.search(r'[+\-*/]', cmdStr).group()
            split = cmdStr.split(operator, 1)
            a2 = int(split[0])
            cmdStr = split[1]
    # 运算符不为空，则表示存在附加表达式
    if not operator == "":
        # cmdStr = cmdStr.split(operator)[1]
        # 判断是否包含d，如包含，则取d之前的内容
        if cmdStr.find('d') != -1:
            split = cmdStr.split("d", 1)
            b1 = int(split[0])
            if split[1] != "":
                if re.findall(r'\d+', split[1]) != "":
                    b2 = int("".join(re.findall(r'\d+', split[1])))
                extMsg = re.findall(r'\D+', split[1])
            else:
                b2 = diceType
                extMsg = ""
        else:
            # 取数字和附加消息
            b1 = int("".join(re.findall(r'\d+', cmdStr)))
            extMsg = re.findall(r'\D+', cmdStr)
    extMsg = "".join(extMsg)

    result = {
        "a1": a1,
        "a2": a2,
        "b1": b1,
        "b2": b2,
        "operator": operator,
        "diceType": diceType,
        "extMsg": extMsg
    }
    return result


async def getRdResult(a1, a2, b1, b2, operator, diceType, extMsg, msgData):
    resultStr = await doRd(a1=a1, a2=a2, b1=b1, b2=b2, operator=operator, diceType=diceType, extMsg=extMsg)
    return await reply(msgCode.RD_RESULT.name, msgData, resultStr)


async def doRd(a1, a2, b1, b2, operator, diceType, extMsg):
    result = []
    if a1 == 0:
        a1 = 1
    if a2 == 0:
        a2 = diceType
    firstResult = await dice.xdy(a1, a2)
    equation = [str(a1) + "d" + str(a2)]

    # 如果operator存在
    if not operator == "":
        equation.append(operator)
        if firstResult["equation"] == '':
            firstResult["equation"] = firstResult["result"]
        if b1 == 0:
            return await reply(msgCode.RD_ILLEGAL_FORMAT.name)
        if b2 == 0:
            c = await cal.operatorCal(operator, int(firstResult["result"]), b1)
            equation.append(str(b1))
            equation.append("=")
            equation.append(str(c))
            equation.append("[")
            equation.append(firstResult["equation"] + operator + str(b1) + "=" + str(c))
            equation.append("]")
        else:
            extResult = await dice.xdy(b1, b2)
            c = await cal.operatorCal(operator, int(firstResult["result"]), int(extResult["result"]))
            equation.append(str(b1) + "d" + str(b2) + "=")
            equation.append(str(c))
            equation.append("[")
            equation.append(firstResult["equation"] + operator + extResult["equation"] + "=" + str(c))
            equation.append("]")
        result.append("".join(equation))
    else:
        equation.append("=" + firstResult["result"] + firstResult["equation"])
        result.append("".join(equation))
    if extMsg != "":
        result.append("▶")
        result.append(extMsg)
        # result.append("◀")
    resultStr = "".join(result)
    return resultStr
