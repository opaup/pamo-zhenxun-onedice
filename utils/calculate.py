async def operatorCal(operator, num1, num2):
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = num1 / num2
    else:
        result = 0
    return result


# 根据rd结果获取数字形式的最终结果
async def getIntResultForRdResult():
    return
