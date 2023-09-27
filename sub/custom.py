import json
import utils.data as dataSource

msgJsonPath = dataSource.msgJsonPath
botJsonPath = dataSource.botJsonPath

# 定义占位符字典
placeholders = {}


def updatePlaceholders(msgData):
    with open(botJsonPath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        placeholders.update(data)
    with open(msgJsonPath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        placeholders.update(data)
    if dataSource.NICKNAME != "":
        data['NICKNAME'] = dataSource.NICKNAME
    if msgData['GROUPID'] != "":
        data['GROUPID'] = msgData['GROUPID']
    if msgData['USERNAME'] != "":
        data['USERNAME'] = msgData['USERNAME']
    placeholders.update(data)


def reply(key, result, msgData):
    updatePlaceholders(msgData)
    with open(msgJsonPath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if key not in data:
        data[key] = dataSource.suppleMsg(msgJsonPath, key)
    value = replace_placeholders(data[key], result=result)
    return value


# 替换占位符
def replace_placeholders(text, result):
    for placeholder, value in placeholders.items():
        placeholder_with_braces = "{" + placeholder + "}"
        text = text.replace(placeholder_with_braces, value)
        if result != "":
            text = text.replace("{RESULT}", result)
    return text
