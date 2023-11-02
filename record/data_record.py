# coding: utf-8
# author: 胡光辉
# date  : 2023/11/1
# file  : data_record

import asyncio
import json
import os
import queue
import time
from asyncio import Queue as a_queue
from collections import defaultdict
from copy import copy
from datetime import datetime
from queue import Queue as q_queue
from threading import Thread

from pandas import DataFrame
from tqsdk import TqApi, TqAuth

from trader.database import get_database
from trader.object import BarData, TickData
from trader.setting import SETTINGS
from .config import SAVE_TIME, EXIT_TIME
from .utility import tq_data_to_bar, tq_data_to_tick


class CTPDataRecord(object):
    def __init__(self, tq_name, tq_password):
        self.api = TqApi(auth=TqAuth(tq_name, tq_password))
        self.a_queue: asyncio.Queue = a_queue()
        self.t_queue: queue.Queue = q_queue()
        self.symbols_tick_dict: dict[str, list] = defaultdict(list)
        self.symbols_bar_dict: dict[str, list] = defaultdict(list)

        self.time_interval: int = 10
        self.active = True
        self.current_time_str: str = f"{datetime.now():%H:%M}"
        self.database = get_database()
        self.thread: Thread = Thread(target=self.save_data_to_db, args=())
        self.thread.start()

    @staticmethod
    def query_all_symbols():
        cwd_path = os.getcwd()
        with open(os.path.join(cwd_path, 'symbols.json'), 'r') as fp:
            symbols_json = json.load(fp)
        return symbols_json.keys()

    async def get_symbol_data(self, symbol: str):
        # tick: dict = await self.api.get_quote(symbol)  # 支持 await 异步，这里会订阅合约，等到收到合约行情才返回
        tick: DataFrame = await self.api.get_tick_serial(symbol)
        bar: DataFrame = await self.api.get_kline_serial(symbol, 60)
        async with self.api.register_update_notify() as update_chan:
            async for _ in update_chan:
                if self.api.is_changing(tick):
                    await self.a_queue.put(('tick', copy(tick.iloc[-1])))

                if self.api.is_changing(bar.iloc[-1], "datetime"):
                    await self.a_queue.put(('bar', copy(bar.iloc[-2])))

    async def get_data_from_queue(self):
        while True:
            data: tuple = await self.a_queue.get()
            self.a_queue.task_done()
            self.t_queue.put(data)

    def save_data_to_db(self):
        while self.active:
            try:
                data: tuple = self.t_queue.get(timeout=1)
                self.t_queue.task_done()
            except queue.Empty:
                continue

            data_type, data_ = data
            if data_type == 'tick':
                tick_data: TickData = tq_data_to_tick(data_)
                self.database.save_tick_data(('tick', tick_data))
            elif data_type == 'bar':
                bar_data: BarData = tq_data_to_bar(data_)
                self.database.save_bar_data(('bar', bar_data))

    def time_to_save_data_to_db(self):
        self.database.save_tick_data(None)
        self.database.save_bar_data(None)

    def create_record_task(self):
        self.api.create_task(self.get_data_from_queue())
        symbols = self.query_all_symbols()
        for symbol in symbols:
            self.api.create_task(self.get_symbol_data(symbol))

    async def update_time(self):
        self.current_time_str = f"{datetime.now():%H:%M}"

    async def check_time(self):
        if self.current_time_str in SAVE_TIME:
            self.time_to_save_data_to_db()

        elif self.current_time_str in EXIT_TIME:
            self.stop_record()

    async def timer(self):
        while True:
            await asyncio.sleep(self.time_interval)
            await self.update_time()
            await self.check_time()

    def start_record(self):
        self.api.create_task(self.timer())
        self.create_record_task()
        while self.active:  # 通过协程控制self.active的值 控制是否退出
            self.api.wait_update(deadline=int(time.time()) + 10)
        self.api.close()

    def stop_record(self):
        self.active = False
        self.database.active = False
        self.database.thread.join()
        self.thread.join()


if __name__ == '__main__':
    name = SETTINGS['tq.account']
    password = SETTINGS['tq.password']
    record = CTPDataRecord(name, password)
    record.start_record()  # 也可以改写为线程控制时间，目前为协程控制时间
