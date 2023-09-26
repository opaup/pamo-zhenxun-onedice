import utils.dice as dice


def roll3d6_5():
    a = 0
    b = []
    for i in range(3):
        d = dice.roll(6)
        a += d
        b.append(str(d))
        if not i == 2:
            b.append("+")
    a *= 5
    result = ''.join(b) + "*5" + "=" + str(a)
    return "(" + result + ")"


def getOneCocCard(func):
    result = []
    a = "  a :" + func()
    b = "  b :" + func()
    result.append(a)
    result.append(b)
    return "".join(result)


def cocMaker(num):
    result = []
    num = int(num)

    for i in range(num):
        result.append(getOneCocCard(roll3d6_5))
        if not i == num - 1:
            result.append("\n")

    return "".join(result)


def dndMaker():
    return


def coc5thMaker():
    return


def cochildMaker():
    return
