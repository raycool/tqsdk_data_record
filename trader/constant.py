# coding: utf-8
# author: 胡光辉
# date  : 2023/11/1
# file  : constant

from enum import Enum


class Exchange(Enum):
    """Exchange枚举"""
    CFFEX = "CFFEX"         # China Financial Futures Exchange
    SHFE = "SHFE"           # Shanghai Futures Exchange
    CZCE = "CZCE"           # Zhengzhou Commodity Exchange
    DCE = "DCE"             # Dalian Commodity Exchange
    GFEX = "GFEX"           # Guangzhou Commodity Exchange
    INE = "INE"             # Shanghai International Energy Exchange
    SSE = "SSE"             # Shanghai Stock Exchange
    SZSE = "SZSE"           # Shenzhen Stock Exchange


class Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "1m"
    MINUTE_30 = '30m'
    HOUR = "1h"
    DAILY = "d"
    WEEKLY = "w"
    TICK = "tick"
