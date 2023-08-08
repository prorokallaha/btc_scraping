import asyncio
import requests
import websockets
import json
import time

from config import settings
from indicators.rsi import RSI
from bot import send_info

rsi = RSI(config=settings)
program_status = False
last_rsi_btc = 0
last_rsi_eth = 0
last_rsi_ltc = 0


async def socket_connection(parsing_func, status):
    history_btc = json.loads(
        requests.get(
            url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=30m&limit=13"
        ).text
    )
    history_ltc = json.loads(
        requests.get(
            url="https://api.binance.com/api/v3/klines?symbol=LTCUSDT&interval=30m&limit=13"
        ).text
    )
    history_eth = json.loads(
        requests.get(
            url="https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=30m&limit=13"
        ).text
    )
    for _ in range(13):
        try:
            settings.crypto_closes['btc'].append(float(history_btc[_][4]))
            settings.crypto_closes['eth'].append(float(history_eth[_][4]))
            settings.crypto_closes['ltc'].append(float(history_ltc[_][4]))
        except Exception as ex:
            print(f"Socket - {ex}")

    try:
        async with websockets.connect(
                uri='wss://stream.binance.com:9443/ws/btcusdt@kline_1m',
                ping_interval=None
        ) as websocket_btc:
            async with websockets.connect(
                    uri='wss://stream.binance.com:9443/ws/ethusdt@kline_1m',
                    ping_interval=None
            ) as websocket_eth:
                async with websockets.connect(
                        uri='wss://stream.binance.com:9443/ws/ltcusdt@kline_1m',
                        ping_interval=None
                ) as websocket_ltc:
                    start_time = time.time()

                    while True:
                        try:
                            result_btc = await websocket_btc.recv()
                            result_ltc = await websocket_ltc.recv()
                            result_eth = await websocket_eth.recv()

                            # print(
                            #     f"Closes - {str(json.loads(result_btc)['k']['c'])}. Open - {json.loads(result_btc)['k']['x']}")
                            # print(
                            #     f"Closes - {str(json.loads(result_ltc)['k']['c'])}. Open - {json.loads(result_ltc)['k']['x']}")
                            # print(
                            #     f"Closes - {str(json.loads(result_eth)['k']['c'])}. Open - {json.loads(result_eth)['k']['x']}")

                            if time.time() - start_time > 2400:
                                status = True
                                await main(status=status)

                            settings.crypto_result['btc'].append(
                                json.loads(result_btc)['k']
                            )
                            settings.crypto_result['ltc'].append(
                                json.loads(result_ltc)['k']
                            )
                            settings.crypto_result['eth'].append(
                                json.loads(result_eth)['k']
                            )
                            await parsing_func()
                        except Exception as ex:
                            print(f"Socket - {ex}")
                            # logger.error(f'Problem in websockets.recv - {ex}')
    except Exception as ex:
        print(f"Socket - {ex}")


async def parsing_data(socket_result=settings.crypto_result):
    result_btc = socket_result['btc'][-1]
    result_ltc = socket_result['ltc'][-1]
    result_eth = socket_result['eth'][-1]
    if result_btc['x']:
        settings.crypto_closes['btc'].append(float(result_btc['c']))
        settings.crypto_closes['ltc'].append(float(result_ltc['c']))
        settings.crypto_closes['eth'].append(float(result_eth['c']))
        if len(settings.crypto_closes['btc']) > settings.RSI_PERIOD:
            rsi.scraping_rsi(array=settings.crypto_closes, token='btc')
            rsi.scraping_rsi(array=settings.crypto_closes, token='ltc')
            rsi.scraping_rsi(array=settings.crypto_closes, token='eth')
            await send_info()

async def main(status):
    task = asyncio.create_task(
        socket_connection(
            parsing_func=parsing_data,
            status=status
        )
    )
    if status:
        task = task.cancel()
        task1 = asyncio.create_task(
            socket_connection(
                parsing_func=parsing_data,
                status=status
            )
        )
        status = False
        await task1
    else:
        await task


if __name__ == "__main__":
    asyncio.run(main(status=program_status))