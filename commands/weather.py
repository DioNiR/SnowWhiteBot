import logging
from aiogram.dispatcher import Dispatcher
from aiogram.bot import Bot

import requests

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import *

from . import commands

class CommandWeather(commands):
    def __init__(self, dp: Dispatcher, bot: Bot, scheduler: AsyncIOScheduler, logger: logging.Logger=None):
        self.dp = dp
        self.bot = bot
        self.scheduler = scheduler
        self.logger = logger if logger is not None else logging.getLogger("CommandWeather")
        self.send_message = self.bot.send_message

        self.api_key = '4cba48cbd8b05d3c372aec57bdc1b6a7'

        #scheduler.add_job(self.weather_timer, 'cron', year='*', month='*', day='*', week='*', hour='22', minute=37, second=0)

    def register_message_handler(self):
        self.dp.register_message_handler(self.main, commands=["погода"])

    async def main(self, message):
        weather = await self.weather_by_city("Moscow, Russia")
        weather_text = f"Погода: {weather['temperature']}°C, ощущается как {weather['feelslike']}°C"
        await message.reply(text = weather_text)

        self.scheduler.add_job(self.weather_timer, 'cron', year='*', month='*', day='*', week='*', hour='8', minute=0,
                               second=0, kwargs={'chat_id': message.chat.id})


    async def weather_timer(self, chat_id = 0):
        weather = await self.weather_by_city("Moscow")
        weather_text = f"Погода: {weather['temperature']}°C, ощущается как {weather['feelslike']}°C"
        await self.bot.send_message(chat_id, weather_text)

    async def weather_by_city(self, city_name):
            url = "http://api.weatherstack.com/current"
            params = {
                "access_key": self.api_key,
                "query": city_name,
            }
            try:
                result = requests.get(url, params=params)
                weather = result.json()

                print(weather)

                if 'current' in weather:
                    if 'temperature' in weather['current']:
                        try: 
                            return weather['current']
                        except(IndexError, TypeError):
                            return False

            except(requests.RequestException, ValueError):
                print("Сетевая ошибка")
                return False
            return False