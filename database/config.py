# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/23
import importlib.util as importlibUtil
from ..utils import data as dataSource
import asyncio


bind = ""
sql_name = ""
user = ""
password = ""
address = ""
port = ""
database = ""
# 判断是否存在真寻bot配置，如有则使用真寻bot配置
async def loadConfig():
    try:
        zhenxunConfig = "configs.config"
        if importlibUtil.find_spec(zhenxunConfig):
            from configs import config
            bind = config.bind
            sql_name = config.sql_name
            user = config.user
            password = config.password
            address = config.address
            port = config.port
            database = config.database
    except ImportError:
        configs = await dataSource.getConfigItem("database")
        sql_name = configs['sql_name']
        user = configs['user']
        password = configs['password']
        address = configs['address']
        port = configs['port']
        database = configs['database']

asyncio.run(loadConfig())
