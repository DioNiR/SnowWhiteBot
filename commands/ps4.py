import logging
from aiogram.dispatcher import Dispatcher
from aiogram.bot import Bot

import requests

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from . import commands

import db as db

from bs4 import BeautifulSoup

class CommandPS4(commands):
    def __init__(self, dp: Dispatcher, bot: Bot, scheduler: AsyncIOScheduler, logger: logging.Logger=None):
        self.bot = bot
        self.dp = dp
        self.db = db.DBProducts()
        self.scheduler = scheduler
        self.logger = logger if logger is not None else logging.getLogger("CommandPS4")
        self.send_message = self.bot.send_message

    async def main(self, message):
        message_bot = await self.bot.send_message(message.chat.id, 'Минутку')

        data = await self.parse_product_data()
        print(data)

        await self.bot.delete_message(chat_id = message.chat.id, message_id = message_bot.message_id)
        await self.bot.send_photo(chat_id = message.chat.id, photo = data['image'], caption = data['text'] )

        self.scheduler.add_job(self.ps4_timer, 'cron', year='*', month='*', day='*', week='*', hour='8', minute=0,
                               second=0, kwargs={'chat_id': message.chat.id})

    def register_message_handler(self):
        self.dp.register_message_handler(self.main, commands=["ps4"])

    async def ps4_timer(self):
        data = await self.get_price()
        last_price = self.db.select_last_price_by_product_id(1)

        pass

    async def parse_product_data(self, product_id = 1):
        data = await self.get_price()
        print(data)
        last_price = self.db.select_last_price_by_product_id(product_id)
        if last_price[0] == None:
            self.db.update_price_by_product_id(product_id, data['price'])
            text = f"Цена: {data['price']}р"
        else:
            text = f"Цена не изменилась: {data['price']}р"

            if data['price'] > last_price[0]:
                text = f"Цена поднилась! {last_price} > {data['price']}р"
            elif data['price'] < last_price[0]:
                text = f"Цена уменьшилась! {last_price} > {data['price']}р"

        return {'text': text, 'price': data['price'], 'old_price': last_price, 'image': data['image']}

    async def get_price(self):
        url = "https://www.e-katalog.ru/SONY-PLAYSTATION-4-SLIM-500GB.htm"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        }

        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.content, 'html.parser')

        span_price = soup.find('span', itemprop = 'lowPrice')
        img_src = soup.find('img', rel = 'v:photo')
        price = ''.join(x for x in span_price.text if x.isdigit())

        return {'price': int(price), 'image': 'https://www.e-katalog.ru/' + img_src['src']}

