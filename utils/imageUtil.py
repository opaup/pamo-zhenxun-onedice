# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/20
import os, re


async def getCqimgUrl(cqCode, bot):
    """
    从CQ码中获取图片url
    # cqimg -> 图片 -> jpg -> url（string）
    """
    if not cqCode[0] == '[' and not cqCode[-1] == ']':
        cqCode = f'[{cqCode}]'
    pattern = r'file=(.*?)(?:,|\])'
    result = re.search(pattern, cqCode)
    file = result.group(1)
    cqimg = await bot.get_image(file=file)
    url = cqimg['file']
    newFile = url + '.jpg'
    os.rename(url, newFile)
    return newFile
