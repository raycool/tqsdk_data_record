# coding: utf-8
# author: 胡光辉
# date  : 2023/11/1
# file  : symbol_filter

from tqsdk import TqApi, TqAuth
import os
import json
from trader.setting import SETTINGS

EXCHANGES = ['CZCE','DCE','SHFE','INE','GFEX']
class SymbolFilter(object):
    def __init__(self, tq_name: str, tq_password: str):
        self.api = TqApi(auth=TqAuth(tq_name, tq_password))
        self.save_symbols: dict = {}

    def get_symbol_class(self, exchange, type_='FUTURE'):
        symbols = self.api.query_quotes(ins_class=type_, exchange_id=exchange, expired=False)  # 防止郑州有些品种出错
        return symbols

    def filter_symbols(self):
        symbols = []
        for exchange in EXCHANGES:
            symbols_ = self.get_symbol_class(exchange)
            symbols.extend(symbols_)
        for index in range(0, len(symbols), 50):
            quote_list = self.api.get_quote_list(symbols[index:index + 50])
            for item in quote_list:
                if item.open_interest >= 50000:
                    self.save_symbols.update({item.instrument_id: [item.instrument_name, item.open_interest]})

    def save_json(self):
        cwd_path = os.getcwd()
        with open(os.path.join(cwd_path, 'symbols.json'), 'w') as fp:
            json.dump(self.save_symbols, fp, ensure_ascii=False, indent=4)

    def save_latest_symbols(self):
        self.filter_symbols()
        self.save_json()
        self.api.close()


if __name__ == '__main__':
    tq_name = SETTINGS["tq.account"]
    tq_password = SETTINGS["tq.password"]
    sf = SymbolFilter(tq_name, tq_password)
    sf.save_latest_symbols()
