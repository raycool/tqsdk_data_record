# coding: utf-8
# author: 胡光辉
# date  : 2023/11/1
# file  : utility

from datetime import datetime

from pandas import Series
from tqsdk.tafunc import time_to_datetime

from trader.constant import Exchange, Interval
from trader.object import TickData, BarData


def filter_future(symbol):
    if symbol.startswith('DCE') and not symbol.startswith('DCE.SP'):
        if '-' not in symbol:
            return True
        else:
            return False

    elif symbol.startswith('CZCE') and not symbol.startswith('CZCE.SPD'):
        if 'P' in symbol or 'C' in symbol:
            return False
        else:
            return True

    elif symbol.startswith('SHFE') or symbol.startswith('INE'):
        if 'P' in symbol or 'C' in symbol:
            return False
        else:
            return True
    else:
        return False


def tq_data_to_tick(tick: Series) -> TickData:
    tick.fillna(value=0, inplace=True)
    tick = TickData(
        gateway_name='TQ',
        symbol=tick['symbol'].split('.')[-1],
        exchange=Exchange(tick['symbol'].split('.')[0]),
        datetime=time_to_datetime(tick['datetime']),

        volume=tick['volume'],

        open_interest=tick['open_interest'],
        last_price=tick['last_price'],
        # limit_up=tick['upper_limit'],
        # limit_down=tick['lower_limit'],

        # open_price=tick['open'],
        high_price=tick['highest'],
        low_price=tick['lowest'],
        # pre_close=tick['pre_close'],
        turnover=tick['amount'],

        bid_price_1=tick['bid_price1'],
        bid_price_2=tick['bid_price2'],
        bid_price_3=tick['bid_price3'],
        bid_price_4=tick['bid_price4'],
        bid_price_5=tick['bid_price5'],

        ask_price_1=tick['ask_price1'],
        ask_price_2=tick['ask_price2'],
        ask_price_3=tick['ask_price3'],
        ask_price_4=tick['ask_price4'],
        ask_price_5=tick['ask_price5'],

        bid_volume_1=tick['bid_volume1'],
        bid_volume_2=tick['bid_volume2'],
        bid_volume_3=tick['bid_volume3'],
        bid_volume_4=tick['bid_volume4'],
        bid_volume_5=tick['bid_volume5'],

        ask_volume_1=tick['ask_volume1'],
        ask_volume_2=tick['ask_volume2'],
        ask_volume_3=tick['ask_volume3'],
        ask_volume_4=tick['ask_volume4'],
        ask_volume_5=tick['ask_volume5'],

        localtime=datetime.now())

    # tick = dict(map(lambda x: (x[0], 0) if isnan(x[1]) else (x[0], x[1]), tick.__dict__))

    return tick


def tq_data_to_bar(bar: Series) -> BarData:
    bar.fillna(value=0, inplace=True)
    return BarData(
        gateway_name='TQ',
        symbol=bar['symbol'].split('.')[-1],
        exchange=Exchange(bar['symbol'].split('.')[0]),
        datetime=time_to_datetime(bar['datetime']),
        interval=Interval.MINUTE,
        volume=bar['volume'],
        open_interest=bar['open_oi'],
        open_price=bar['open'],
        high_price=bar['high'],
        low_price=bar['low'],
        close_price=bar['close'])
