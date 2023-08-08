import datetime
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from config import settings

bot = Bot('5165798370:AAE9F4cCCbYySC0LGBf4b3cQWJ9ws6-r7J8')
dp = Dispatcher(bot)


async def send_info():
    last_rsi_btc = settings.crypto_status['btc']['last_rsi']
    last_rsi_ltc = settings.crypto_status['ltc']['last_rsi']
    last_rsi_eth = settings.crypto_status['eth']['last_rsi']

    text_message = f'''
Последнее значение BTC: {last_rsi_btc}
Последнее значение LTC: {last_rsi_ltc}
Последнее значение ETH: {last_rsi_eth}
        '''
    settings.crypto_status['btc']['rsi'] = 0
    await bot.send_message("-974345397", text_message)
