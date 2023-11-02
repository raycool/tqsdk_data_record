# coding: utf-8
# author: 胡光辉
# date  : 2023/11/1
# file  : server

from datetime import datetime, time

from apscheduler.schedulers.background import BlockingScheduler

from record.data_record import CTPDataRecord
from record.data_supplement import LastMinuteDataRecord
from record.symbol_filter import SymbolFilter
from trader.setting import SETTINGS
from trading_calendars import TradingCalendars


def update_symbol():
    if not check_calendar():
        return
    name = SETTINGS['tq.account']
    password = SETTINGS['tq.password']
    sf = SymbolFilter(name, password)
    sf.save_latest_symbols()
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}:  update_symbol 退出.")


def record_data():
    if not check_calendar():
        return
    name = SETTINGS['tq.account']
    password = SETTINGS['tq.password']
    record = CTPDataRecord(name, password)
    record.start_record()  # 也可以改写为线程控制时间，目前为协程控制时间
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}:  record_data 退出.")


def update_bar():
    if not check_calendar():
        return
    name = SETTINGS['tq.account']
    password = SETTINGS['tq.password']
    record = LastMinuteDataRecord(name, password)
    record.start_record()
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}:  update_bar 退出.")


def check_calendar():
    trading_calendar = TradingCalendars()
    current_time = datetime.now().time()
    if time(8, 30) < current_time < time(15, 45):
        if trading_calendar.today_is_trading_day:
            return True
    elif current_time > time(20, 40):
        if trading_calendar.today_is_trading_day and trading_calendar.today_has_night_trade:
            return True
    elif time(0, 5) < current_time < time(2, 50):
        if trading_calendar.yesterday_has_night_trade:
            return True
    else:
        print(f"{datetime.now():%Y-%m-%d %H:%M} 为非交易日或者交易时段，退出!")
        return False


scheduler = BlockingScheduler(timezone="Asia/Shanghai")

# 按照cron定时处理任务
scheduler.add_job(update_symbol, 'cron', day_of_week='mon-fri', hour='20', minute=50)
scheduler.add_job(record_data, 'cron', day_of_week='mon-fri', hour='8,20', minute=55)
scheduler.add_job(record_data, 'cron', day_of_week='mon-fri', hour='13', minute=25)
scheduler.add_job(update_bar, 'cron', day_of_week='tue-sat', hour='2', minute=40)
scheduler.add_job(update_bar, 'cron', day_of_week='mon-fri', hour='11', minute=40)
scheduler.add_job(update_bar, 'cron', day_of_week='mon-fri', hour='15', minute=10)
scheduler.start()

# scheduler.add_job(update_symbol, 'cron', day_of_week='mon-sun', hour='15', minute=51)
# scheduler.start()
