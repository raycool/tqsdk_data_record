# coding: utf-8
# author: 胡光辉
# date  : 2023/11/1
# file  : setting

from logging import INFO
from typing import Dict, Any
from tzlocal import get_localzone_name


SETTINGS: Dict[str, Any] = {
    "log.active": True,
    "log.level": INFO,
    "log.console": True,
    "log.file": True,

    "database.timezone": get_localzone_name(),
    "database.name": "tdengine",                # see database.Driver
    "database.database": "ctp",
    "database.host": "127.0.0.1",
    "database.port": 6030,
    "database.user": "xxxx",        # 数据库用户名
    "database.password": "xxxx",    # 数据库密码

    "tq.account": "xxxx",   # 账号
    "tq.password": "xxxx"  # 密码
}
