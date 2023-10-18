import random

from ..utils import dice
from ..sub.custom import reply
from ..em.msgCode import msgCode


async def roll3d6():
    a = 0
    for i in range(3):
        d = await dice.roll(6)
        a += d
    return str(a)


async def roll3d6_5():
    """
    简单的3d6 * 5
    """
    a = int(await roll3d6()) * 5
    return str(a)


async def roll2d6And6():
    """
    简单的2d6 + 6
    """
    a = 0
    for i in range(2):
        d = await dice.roll(6)
        a += d
    return str(a)


async def roll2d6And6_5():
    """
    简单的(2d6 + 6) * 5
    """
    a = int(await roll2d6And6()) * 5
    return str(a)


async def getOneCocCard():
    strength = await roll3d6_5()
    constitution = await roll3d6_5()
    size = await roll2d6And6_5()
    dexterity = await roll3d6_5()
    appearance = await roll3d6_5()
    intelligence = await roll2d6And6_5()
    power = await roll3d6_5()
    education = await roll2d6And6_5()
    luck = await roll3d6_5()
    sanity = power

    # 计算伤害加值和体格
    dbcount = int(strength) + int(size)
    if 2 <= dbcount <= 64:
        damageB = "-2"
        build = -2
    elif 65 <= dbcount <= 84:
        damageB = "0"
        build = 0
    elif 85 <= dbcount <= 124:
        damageB = "1d4"
        build = 1
    elif 125 <= dbcount <= 164:
        damageB = "1d6"
        build = 2
    elif 165 <= dbcount <= 204:
        damageB = "2d6"
        build = 3
    elif 205 <= dbcount <= 284:
        damageB = "3d6"
        build = 4
    elif 285 <= dbcount <= 364:
        damageB = "4d6"
        build = 5
    elif 365 <= dbcount <= 444:
        damageB = "5d6"
        build = 6
    else:
        damageB = "0"
        build = "0"

    # print(rf"build = {build}")
    # 计算
    health = (int(size) + int(constitution)) // 10
    mana = int(power) // 5
    totalNoLuck = (int(strength) + int(constitution) + int(size) + int(dexterity) +
                   int(appearance) + int(intelligence) + int(power) + int(education) + int(luck))
    total = (totalNoLuck + int(luck))

    return "".join([
        f"力量:{strength} 敏捷:{dexterity} 意志:{power}\n",
        f"体质:{constitution} 魅力:{appearance} 教育:{education}\n",
        f"体型:{size} 智力:{intelligence} 幸运:{luck}\n",
        f"体力:{health} 魔法:{mana} DB:{damageB}\n",
        f"san:{sanity} 体格：{build}\n",
        f"总值:{totalNoLuck}/{total}\n",
        f"★———☆—————"
    ])


async def cocMaker(num, msgData):
    resultList = []
    num = int(num)

    for i in range(num):
        resultList.append(await getOneCocCard())
        if not i == num - 1:
            resultList.append("\n")
    result = "".join(resultList)
    return await reply(msgCode.MAKE_CARD_COC7.name, msgData, result)


async def dndMaker():
    return


async def coc5thMaker():
    return


async def cochildMaker():
    return
