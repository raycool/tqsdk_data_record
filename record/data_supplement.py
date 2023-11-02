# coding: utf-8
# author: 胡光辉
# date  : 2023/11/1
# file  : data_supplement


import json
import os
import time
from copy import copy

from pandas import DataFrame
from tqsdk import TqApi, TqAuth

from trader.database import get_database
from trader.object import BarData
from trader.setting import SETTINGS
from .utility import tq_data_to_bar


class LastMinuteDataRecord(object):
    def __init__(self, tq_name, tq_password):
        self.api = TqApi(auth=TqAuth(tq_name, tq_password))
        self.database = get_database()

    @staticmethod
    def query_all_symbols():
        cwd_path = os.getcwd()
        with open(os.path.join(cwd_path, 'symbols.json'), 'r') as fp:
            symbols_json = json.load(fp)
        return symbols_json.keys()

    @staticmethod
    def get_table_names():
        table_names = set()
        cwd_path = os.getcwd()
        with open(os.path.join(cwd_path, 'symbols.json'), 'r') as fp:
            symbols_json = json.load(fp)
        for key in symbols_json.keys():
            exchange = key.split('.')[0].lower()
            symbol = key.split('.')[1]
            table_name: str = "_".join(["bar", symbol, exchange, '1m'])
            table_names.add(table_name)
        return table_names

    def get_symbol_bar_data(self, symbol: str):
        bar: DataFrame = self.api.get_kline_serial(symbol, 60)
        data_ = copy(bar.iloc[-1])
        bar_data: BarData = tq_data_to_bar(data_)
        self.database.save_bar_data(('bar', bar_data))

    def time_to_save_data_to_db(self):
        self.database.save_bar_data(None)

    def update_database_info(self):
        table_names = self.get_table_names()
        for table_name in table_names:
            self.database.update_tag_count_info(table_name)

    def start_record(self):
        symbols = self.query_all_symbols()
        for symbol in symbols:
            self.get_symbol_bar_data(symbol)
        self.time_to_save_data_to_db()
        time.sleep(10)               # 等待数据存储完成
        self.update_database_info()
        self.stop_record()

    def stop_record(self):
        self.database.active = False
        self.database.thread.join()
        self.api.close()


if __name__ == '__main__':
    name = SETTINGS['tq.account']
    password = SETTINGS['tq.password']
    record = LastMinuteDataRecord(name, password)
    record.start_record()  # 也可以改写为线程控制时间，目前为协程控制时间
