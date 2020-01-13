import logging
from aiogram.bot import Bot

import requests

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import *

class CommandWeather:
    def __init__(self, bot: Bot, scheduler: AsyncIOScheduler, logger: logging.Logger=None):
        self.bot = bot
        self.scheduler = scheduler
        self.logger = logger if logger is not None else logging.getLogger("CommandWeather")
        self.send_message = self.bot.send_message

    async def main(self, message):
        weather = await self.weather_by_city("Moscow, Russia")
        weather_text = f"Погода: {weather['temp_C']}°C, ощущается как {weather['FeelsLikeC']}°C"
        await message.reply(text=weather_text)

        #scheduler.add_job(self.weather_timer, 'cron', year='*', month='*', day='*', week='*', hour='22', minute=37, second=0)
        self.scheduler.add_job(self.weather_timer, 'cron', year='*', month='*', day='*', week='*', hour='8', minute=0, second=0, kwargs={'chat_id': message.chat.id})


    async def weather_timer(self, chat_id = 0):
        weather = await self.weather_by_city("Moscow, Russia")
        weather_text = f"Погода: {weather['temp_C']}°C, ощущается как {weather['FeelsLikeC']}°C"
        await self.bot.send_message(chat_id, weather_text)

    async def weather_by_city(self, city_name):
            url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
            params = {
                "key": "f9680c083e67400ab0e114736200801 ",
                "q": city_name,
                "format": "json",
                "num_of_days": 1,
                "lang": "ru"
            }
            try:
                result = requests.get(url, params=params)
                weather = result.json()

                if 'data' in weather:
                    if 'current_condition' in weather['data']:
                        try: 
                            return weather['data']['current_condition'][0]
                        except(IndexError, TypeError):
                            return False

            except(requests.RequestException, ValueError):
                print("Сетевая ошибка")
                return False
            return False