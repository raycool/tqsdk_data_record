# coding : utf-8
# date   : 2023/10/15
# author : 胡光辉
# file   : td_script.py

"""
TDengine脚本, 用于在TDengine中创建数据库和数据表。
"""

# 创建数据库
CREATE_DATABASE_SCRIPT = """
CREATE DATABASE IF NOT EXISTS {} KEEP 36500
"""

# 创建bar超级表
CREATE_BAR_TABLE_SCRIPT = """
CREATE STABLE IF NOT EXISTS s_bar (
    datetime TIMESTAMP,
    volume FLOAT,
    turnover DOUBLE,
    open_interest FLOAT,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT
)
TAGS(
    symbol BINARY(20),
    exchange BINARY(10),
    interval_ BINARY(5),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    count_ DOUBLE
)
"""

# 创建tick超级表
CREATE_TICK_TABLE_SCRIPT = """
CREATE STABLE IF NOT EXISTS s_tick (
    datetime TIMESTAMP,
    name NCHAR(20),
    volume FLOAT,
    turnover DOUBLE,
    open_interest FLOAT,
    last_price FLOAT,
    last_volume FLOAT,
    limit_up FLOAT,
    limit_down FLOAT,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    pre_close FLOAT,
    bid_price_1 FLOAT,
    bid_price_2 FLOAT,
    bid_price_3 FLOAT,
    bid_price_4 FLOAT,
    bid_price_5 FLOAT,
    ask_price_1 FLOAT,
    ask_price_2 FLOAT,
    ask_price_3 FLOAT,
    ask_price_4 FLOAT,
    ask_price_5 FLOAT,
    bid_volume_1 FLOAT,
    bid_volume_2 FLOAT,
    bid_volume_3 FLOAT,
    bid_volume_4 FLOAT,
    bid_volume_5 FLOAT,
    ask_volume_1 FLOAT,
    ask_volume_2 FLOAT,
    ask_volume_3 FLOAT,
    ask_volume_4 FLOAT,
    ask_volume_5 FLOAT,
    localtime TIMESTAMP
)
TAGS(
    symbol BINARY(20),
    exchange BINARY(10),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    count_ INT UNSIGNED
)
"""