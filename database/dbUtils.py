# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/24
from . import _model as database
from ..utils import data as dataSource
from ..utils import strUtil, logsUtil


async def pullUserData(userId=None):
    """
    传入id为获取一个，否则为获取全部
    """
    if userId is None:
        users = await database.onedice_user.getAllList()
    else:
        users = await database.onedice_user.getAllList(userId)
    for user in users:
        userInfo = {
            "id": user.id,
            "permissionLevel": user.permission_level,
            "successRollNum": user.success_roll_num,
            "failRollNum": user.fail_roll_num,
            "greatSuccessRollNum": user.great_success_roll_num,
            "greatFailRollNum": user.great_fail_roll_num,
            "currentCardName": user.current_card_name,
            "currentCard": user.current_card,
            "cardList": user.card_list
        }
        await dataSource.saveUserInfo(user.id, userInfo)


async def pullGroupData(groupId=None):
    if groupId is None:
        groups = await database.onedice_group.getAllList()
    else:
        groups = await database.onedice_group.getAllList(groupId)
    for group in groups:
        groupInfo = {
            "id": group.id,
            "onOff": group.on_off,
            "diceMode": group.dice_mode,
            "diceType": group.dice_type,
            "ruleType": group.rule_type,
            "isNotice": group.is_notice,
            "secretMode": group.secret_mode,
            "cardLock": group.card_lock,
        }
        await dataSource.saveGroupInfo(group.id, groupInfo)


async def pullCharacterData(cardId=None):
    if cardId is None:
        characters = await database.onedice_character.getAllList()
    else:
        characters = await database.onedice_character.getAllList(cardId)
    for character in characters:
        cardInfo = {
            "id": character.id,
            "userId": character.user_id,
            "name": character.name,
            "status": character.status,
            "locked": character.locked,
            "prop": character.prop,
        }
        await dataSource.createCharacter(character.id, cardInfo)


async def saveOrUpdateById(model_class, theId, dic):
    existing = await model_class.filter(id=theId).first()
    dic = {strUtil.camelToSnake(k): v for k, v in dic.items()}
    return await existing.update_or_create(id=theId, defaults=dic)


async def pullLogs(groupId=None, logName=None):
    """
    传入groupId则是群组下全部日志，传入logName则是精准查，单传logName无效
    都不传就是都全部所有
    按时间排序
    """
    if groupId is not None:
        if logName is not None:
            return
    # await logsUtil.readFromCSV()
    return


async def pushLogsData(data):
    for x, y in data.items():
        dic = {strUtil.camelToSnake(k): v for k, v in y.items()}
        dic['group_id'] = groupId
        dic['log_name'] = file
        existing = await database.onedice_log.filter(
            type_name=dic['type_name'],
            message_id=dic['message_id'],
            timestamp=dic['timestamp']
        ).first()
        if not existing:
            await database.onedice_log.create(**dic)
    return data

