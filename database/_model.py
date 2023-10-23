# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/23
from services.db_context import Model
import datetime
from tortoise import fields
from typing import List, Optional, Tuple


class groupInfo(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    group_id = fields.BigIntField()
    """群聊id"""

    class Meta:
        table = "onedice_groupInfo"
        table_description = "dice群聊信息表"
        unique_together = ("id", "group_id")


    @classmethod
    async def update_groupInfo(cls):
        return
