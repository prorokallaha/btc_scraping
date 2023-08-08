# import talib
import numpy as np

from config import settings

class RSI:
    '''Class for RSI indicator'''
    def __init__(self,
                 config: settings):
        self.config = config

    def scraping_rsi(self, array: dict, token: str):
        np_closes = np.array(array[token])
        try:
            pass
            rsi = talib.RSI(np_closes, self.config.RSI_PERIOD)
            last_rsi = rsi[-1]
            self.config.crypto_status[token]['last_rsi'] = last_rsi
        except Exception as ex:
            print(f"RSI - {ex}")