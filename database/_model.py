# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/23
from services.db_context import Model
import datetime
from tortoise import fields
from typing import List, Optional, Tuple


class onedice_group(Model):
    id = fields.CharField(max_length=50, pk=True)
    """群组id"""
    on_off = fields.CharField(max_length=3, null=True)
    """开关状态"""
    dice_mode = fields.CharField(max_length=10, null=True)
    """dice模式"""
    dice_type = fields.CharField(max_length=5, null=True)
    """dice面数"""
    rule_type = fields.CharField(max_length=3, null=True)
    """房规"""
    is_notice = fields.CharField(max_length=3, null=True)
    """扩散状态"""
    secret_mode = fields.CharField(max_length=3, null=True)
    """秘密团模式"""
    card_lock = fields.JSONField(null=True)
    """锁定状态"""

    class Meta:
        table = "onedice_group"
        table_description = "dice群聊信息表"

    @classmethod
    async def getAllList(cls, theId=None):
        if theId is None:
            query = await cls.filter().all()
        else:
            query = await cls.filter(id=theId).all()
        return query


class onedice_user(Model):
    id = fields.CharField(max_length=50, pk=True)
    """用户id"""
    permission_level = fields.SmallIntField(default=1)
    """权限等级"""
    success_roll_num = fields.SmallIntField(default=0)
    fail_roll_num = fields.SmallIntField(default=0)
    great_success_roll_num = fields.SmallIntField(default=0)
    great_fail_roll_num = fields.SmallIntField(default=0)
    current_card_name = fields.TextField(default=0)
    """当前pc昵称"""
    current_card = fields.TextField(null=True)
    """当前pcid"""
    card_list = fields.JSONField(null=True)
    """pc列表"""

    class Meta:
        table = "onedice_user"
        table_description = "dice用户信息表"

    @classmethod
    async def getAllList(cls, theId=None):
        if theId is None:
            query = await cls.filter().all()
        else:
            query = await cls.filter(id=theId).all()
        return query


class onedice_character(Model):
    id = fields.TextField(pk=True)
    """角色id"""
    user_id = fields.TextField(null=True)
    """用户id"""
    name = fields.TextField(null=True)
    """角色昵称"""
    status = fields.SmallIntField(default=0)
    """状态 0 正常 -1 删除"""
    locked = fields.JSONField(null=True)
    """锁定状态"""
    prop = fields.JSONField(null=True)
    """角色属性"""

    class Meta:
        table = "onedice_character"
        table_description = "dice角色信息表"

    @classmethod
    async def getAllList(cls, theId=None):
        if theId is None:
            query = await cls.filter().all()
        else:
            query = await cls.filter(id=theId).all()
        return query


class onedice_msg(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    text = fields.JSONField()

    class Meta:
        table = "onedice_msg"
        table_description = "dice自定义回复词表"


class onedice_log(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    group_id = fields.BigIntField()
    """群组id"""
    log_name = fields.TextField()
    """日志name"""
    type_name = fields.CharField(max_length=50, null=True)
    """群息类型"""
    message_id = fields.CharField(max_length=50, null=True)
    """群息id"""
    timestamp = fields.IntField(null=True)
    """时间戳"""
    message = fields.TextField(null=True)
    """消息内容"""
    user_id = fields.BigIntField(null=True)
    """发言人id"""
    pcname = fields.TextField(null=True)
    """pc昵称"""

    class Meta:
        table = "onedice_logs"
        table_description = "dice记录表"
