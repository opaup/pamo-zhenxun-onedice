import json
from sub.custom import reply
from em.msgCode import msgCode
import utils.data as dataSource


def doRa():
    # 读取propName和算式
    #
    character = dataSource.getCurrentCharacter()
    # 如果character为空，则prop值默认为0
    return "执行ra！"
