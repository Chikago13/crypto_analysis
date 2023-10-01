# https://www.tradingview.com/symbols/BTSUSDT/
# https://python-tradingview-ta.readthedocs.io/en/latest/overview.html
# https://tvdb.brianthe.dev/  TradingView List
# # https://mastergroosha.github.io/aiogram-3-guide/quickstart/#hello-world
# http://docs.ccxt.com

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters.command import Command
from tradingview_ta import TA_Handler, Interval, Recommendation
import ccxt

API_TOKEN ='6531929248:AAFTh9wDMnmqpkYpvl-h5ttT-OgGHNM4VkA'

RECOMMENDATIONS = {
    Recommendation.buy: 'Покупай',
    Recommendation.strong_buy: 'Срочно_покупай',
    Recommendation.sell: 'Продавай',
    Recommendation.strong_sell: 'Срочно_продавай',
    Recommendation.neutral: 'Непонятная ситуация',
    Recommendation.error: 'Ошибка',
}



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher(bpt = bot)
exchange = ccxt.binance()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")



def get_current_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except:
        return None



@dp.message()
async def get_crypto_price(message: types.Message):
    try:
        symbol = message.text.upper()
        price = get_current_price(symbol)
        if price is not None:
            await message.answer(f"Текущая цена {symbol} равна {price}")
            response = TA_Handler(
                symbol=symbol,
                screener="crypto",
                exchange="BINANCE",
                interval=Interval.INTERVAL_5_MINUTES
            )
            result = response.get_analysis().summary
            # await message.answer(result)
            analysis = result.get('RECOMMENDATION', Recommendation.error)
            await message.answer(RECOMMENDATIONS.get(analysis))
    except:
        await message.answer('Некорректный ввод')        


# # Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

