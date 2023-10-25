# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/25

def camelToSnake(s):
    """
    字符串-驼峰式转蛇式
    """
    result = []
    for char in s:
        if char.isupper():
            result.extend(['_', char.lower()])
        else:
            result.append(char)
    return ''.join(result)
