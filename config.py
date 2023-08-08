import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    MARKETS: dict = {'lina': 'linausdt', 'eth': 'ethusdt', 'btc': 'btcusdt',
                     'bnb': 'bnbusdt', 'doge': 'dogeusdt'}
    crypto_status: dict = {'btc': {'rsi': 0, 'last_rsi': 0, 'bbands': None, 'ema': 3.0, 'in_position': False},
                           'ltc': {'rsi': 0, 'last_rsi': 0, 'bbands': None, 'ema': 3.0, 'in_position': False},
                           'eth': {'rsi': 0, 'last_rsi': 0, 'bbands': None, 'ema': 3.0, 'in_position': False}}

    crypto_result: dict = {'btc': [], 'ltc': [], 'eth': []}
    crypto_closes: dict = {'btc': [], 'ltc': [], 'eth': []}

    ADMINS: list = [410296492]
    RSI_PERIOD: int = 14
    RSI_OVERBOUGHT: int = 70
    RSI_OVERSOLD: int = 30


settings = Settings()

RSI_PERIOD: int = settings.RSI_PERIOD
admins_list: list = settings.ADMINS