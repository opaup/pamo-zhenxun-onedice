import re

import utils.calculate as cal
import utils.data as dataSource
import utils.dice as dice
import utils.propUtil as propUtil
from em.msgCode import msgCode
from sub.custom import reply


def doRa(cmdStr, msgData):
    calResult = doRaCal(cmdStr, msgData)
    pcname = calResult["pcname"]
    ruleType = calResult["ruleType"]
    propName = calResult["propName"]
    propValue = calResult["propValue"]
    operator = calResult["operator"]
    equation = calResult["equation"]
    secondEquation = calResult["secondEquation"]
    checkNum = calResult["checkNum"]
    normalResult = calResult["normalResult"]

    checkResultNum = checkResult(propValue, checkNum, ruleType)
    if checkResultNum == 0:
        return
    checkStr = getCheckStrAndRecord(checkResultNum, msgData)
    result = rf"{checkNum}/{propValue}"
    if not operator == "":
        result += rf"[{normalResult}{operator}{equation}{secondEquation}]"

    if checkResultNum == 1:
        return reply(msgCode.ROLL_CHECK_GREAT_SUCCESS.name, msgData, result, ext1=propName, ext2=checkStr,
                     pcname=pcname)
    if checkResultNum == 2:
        return reply(msgCode.ROLL_CHECK_EXT_HARD_SUCCESS.name, msgData, result, ext1=propName, ext2=checkStr,
                     pcname=pcname)
    if checkResultNum == 3:
        return reply(msgCode.ROLL_CHECK_HARD_SUCCESS.name, msgData, result, ext1=propName, ext2=checkStr, pcname=pcname)
    if checkResultNum == 4:
        return reply(msgCode.ROLL_CHECK_SUCCESS.name, msgData, result, ext1=propName, ext2=checkStr, pcname=pcname)
    if checkResultNum == 5:
        return reply(msgCode.ROLL_CHECK_FAIL.name, msgData, result, ext1=propName, ext2=checkStr, pcname=pcname)
    if checkResultNum == 6:
        return reply(msgCode.ROLL_CHECK_GREAT_FAIL.name, msgData, result, ext1=propName, ext2=checkStr, pcname=pcname)
    return


def getCheckStrAndRecord(checkResultNum, msgData):
    checkStr = ""
    if checkResultNum == 0:
        checkStr = "错误"
    if checkResultNum == 1:
        checkStr = "大成功"
    if checkResultNum == 2:
        checkStr = "极难成功"
    if checkResultNum == 3:
        checkStr = "困难成功"
    if checkResultNum == 4:
        checkStr = "成功"
    if checkResultNum == 5:
        checkStr = "失败"
    if checkResultNum == 6:
        checkStr = "大失败"

    if checkResultNum != 0:
        userInfo = dataSource.getUserInfo(msgData["userId"])
        if checkResultNum <= 4:
            successRollNum = userInfo["successRollNum"]
            userInfo["successRollNum"] = successRollNum + 1
            if checkResultNum == 1:
                greatSuccessRollNum = userInfo["greatSuccessRollNum"]
                userInfo["greatSuccessRollNum"] = greatSuccessRollNum + 1
        if checkResultNum > 4:
            failRollNum = userInfo["failRollNum"]
            userInfo["failRollNum"] = failRollNum + 1
            if checkResultNum == 6:
                greatFailRollNum = userInfo["greatFailRollNum"]
                userInfo["greatFailRollNum"] = greatFailRollNum + 1
        dataSource.saveUserInfo(msgData["userId"], userInfo)
    return checkStr


# 进行房规检定，并得到检定结果
# 0 出错了 1 大成功 2 极难成功 3 困难成功 4 成功 5 失败 6 大失败
def checkResult(propValue, checkNum, ruleType):
    result = 0
    if ruleType == "1":
        result = propUtil.check1(propValue, checkNum)
    return result


def doRaCal(cmdStr, msgData):
    cardId = ""
    propName = ""
    propValue = ""
    diceType = "100"
    if not msgData["msgType"] == "group":
        diceType = dataSource.getGroupItem(msgData["groupId"], "diceType")
    operator = ""
    equation = ""
    num1 = 0
    num2 = 0
    ruleType = "1"
    normalResult = dice.roll(int(diceType))

    if not msgData["msgType"] == "group":
        character = dataSource.getCurrentCharacter(msgData["userId"])
    else:
        character = dataSource.getCurrentCharacter(msgData["userId"], msgData["groupId"])
        ruleType = dataSource.getGroupItem(msgData["groupId"], "ruleType")
        cardId = character["id"]
    if not character:
        character["name"] = "{USERNAME}"
    pcname = character["name"]

    # 是否存在操作符
    if re.search(r'[+\-*/]', cmdStr):
        operator = re.search(r'[+\-*/]', cmdStr).group()
        split = cmdStr.split(operator)
        # 存在一个操作符以上的非法格式
        if len(split) > 2:
            return reply(msgCode.ILLEGAL_FORMAT.name, msgData)
        equation = split[1]
        cmdStr = cmdStr.replace(operator + equation, "")
    if not cmdStr == "":
        propName = "".join(re.findall(r'\D+', cmdStr))
        propValue = "".join(re.findall(r'\d+', cmdStr)) or 0
        propValue = int(propValue)
    # 优先读了指令中的propValue，如无则读卡
    if propValue == 0 and not propName == "":
        propValue = character["prop"][propName]

    # 运算符不为空，则表示存在附加表达式
    try:
        if not operator == "":
            # 判断是否包含d，如包含，则取d之前的内容
            if equation.find('d') != -1:
                split = equation.split("d", 1)
                num1 = int(split[0])
                if split[1] != "":
                    if re.findall(r'\d+', split[1]) != "":
                        num2 = int("".join(re.findall(r'\d+', split[1])))
                else:
                    num2 = diceType
            else:
                num1 = int("".join(re.findall(r'\d+', equation)))
    except ValueError:
        return reply(msgCode.ILLEGAL_FORMAT.name, "", msgData)

    # print(rf"propName = {propName}, propValue = {propValue}, operator = {operator}, equation = {equation}")
    # 计算开始
    xdy = dice.xdy(num1, num2)
    secondResult = xdy["result"]
    secondEquation = xdy["equation"]
    checkNum = normalResult
    if not operator == "":
        checkNum = cal.operatorCal(operator, normalResult, int(secondResult))

    calResult = {
        "propName": propName,
        "propValue": int(propValue),
        "xdy": xdy,
        "secondResult": secondResult,
        "equation": equation,
        "secondEquation": secondEquation,
        "checkNum": checkNum,
        "operator": operator,
        "normalResult": normalResult,
        "ruleType": ruleType,
        "pcname": pcname,
        "cardId": cardId
    }
    return calResult
