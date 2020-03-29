import logging
from aiogram.bot import Bot

import requests

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import *

from bs4 import BeautifulSoup

class CommandPS4:
    def __init__(self, bot: Bot, scheduler: AsyncIOScheduler, logger: logging.Logger=None):
        self.bot = bot
        self.scheduler = scheduler
        self.logger = logger if logger is not None else logging.getLogger("CommandPS4")
        self.send_message = self.bot.send_message

    async def main(self, message):
        message_bot = await self.bot.send_message(message.chat.id, 'Минутку')

        print(123412)

        ps4 = await self.get_ps4_price()

        await self.bot.delete_message(chat_id = message.chat.id, message_id = message_bot.message_id)
        await self.bot.send_photo(chat_id = message.chat.id, photo = ps4['image'], caption = ps4['text'])
        

    async def get_ps4_price(self):
        url = "https://market.yandex.ru/product--igrovaia-pristavka-sony-playstation-4-slim-500-gb/14211947"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'market.yandex.ru',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Cookie': 'settings-notifications-popup=%7B%22isAnswered%22%3Atrue%7D; yandexuid=6656918781576960938; _ym_uid=1576960941823078106; mda=0; L=dnVRcWBEXlN4VWoFYEUCXgxZdXVHBVBzLi1cPicH.1576960999.14086.371293.e45e2d071de2f7c608e0c5076c7e6cd5; yandex_login=Dionir; i=44z2DFDN6SB13ewsgBeltKsbiQXoRj7q7CdNWDAtt/1Wke7yfb3/4qTPhQSrUKh6YVdjbdy6P8R2jXsGUN+Tif31J34=; yuidss=6656918781576960938; my=YwA=; categoryQA=1; _ym_d=1580629604; yabs-frequency=/4/0000000000000000/SQO-RP0v8PTPi72GEI40/; Session_id=3:1581326383.5.0.1576960999760:maOluQ:52.1|10892184.0.2|212327.514724.wRjOLdyUKjMfnjo2VbEUudpxIcY; sessionid2=3:1581326383.5.0.1576960999760:maOluQ:52.1|10892184.0.2|212327.596715.lNN20tcIVxkgpWb-qMunPhIaE18; yp=1596397609.szm.1:1600x900:1600x760#1892320999.udn.cDrQktCw0LvQvtCyICDQkNC70LXQutGB0LDQvdC00YA%3D#1581218194.ygu.1#1892320940.yrtsi.1576960940; ymex=1897241544.yrts.1581881544#1892320940.yrtsi.1576960940; skid=3668532211582549450; visits=1578672506-1578777398-1582549450; parent_reqid_seq=7f79569e10d80b3e9af27e0e3b507f41; uid=AABcEl5TycpSjAC0LBLmAg==; js=1; dcm=1; _ym_visorc_160656=b; _ym_visorc_45411513=b; first_visit_time=2020-02-24T16%3A04%3A13%2B03%3A00; currentRegionId=213; currentRegionName=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%83; ugcp=1; fonts-loaded=1; _ym_isad=1'
        }


        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.content, 'html.parser')

        print(soup.get_text())

        img_src = soup.find('img', attrs={'class': 'n-gallery__image image'}).attrs['src']
        print(img_src)

        div_price = soup.find('div', attrs={'class': 'n-product-summary__default-offer-container'}).find('div', attrs={'class': 'n-product-price-cpa2__price'}).find('span', attrs={'class': 'price'})


        return {'text': div_price.text, 'image': 'https:' + img_src}