def check1(propValue, checkNum):
    r = 0
    if propValue <= 50:
        # 先判断成功与失败
        if checkNum <= propValue:
            r = 4
        else:
            r = 5
        # 大成功
        if checkNum == 1:
            r = 1
        # 困难成功
        if checkNum <= propValue / 2:
            r = 3
        # 极难成功
        if checkNum <= propValue / 5:
            r = 2
        # 大失败
        if checkNum >= 98:
            r = 6
    elif propValue > 50:
        if checkNum <= propValue:
            r = 4
        else:
            r = 5
        # 大成功
        if checkNum <= 3:
            r = 1
        # 困难成功
        if checkNum <= propValue / 2:
            r = 3
        # 极难成功
        if checkNum <= propValue / 5:
            r = 2
        # 大失败
        if checkNum >= 100:
            r = 6

    return r
