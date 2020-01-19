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
        ps4 = await self.get_ps4_price()

        await self.bot.delete_message(chat_id = message.chat.id, message_id = message_bot.message_id)
        await self.bot.send_photo(chat_id = message.chat.id, photo = ps4['image'], caption = ps4['text'])
        

    async def get_ps4_price(self):
        url = "https://market.yandex.ru/product--igrovaia-pristavka-sony-playstation-4-slim-500-gb/14211947"

        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'market.yandex.ru',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Cookie': 'yandexuid=6656918781576960938; _ym_uid=1576960941823078106; mda=0; L=dnVRcWBEXlN4VWoFYEUCXgxZdXVHBVBzLi1cPicH.1576960999.14086.371293.e45e2d071de2f7c608e0c5076c7e6cd5; yandex_login=Dionir; i=44z2DFDN6SB13ewsgBeltKsbiQXoRj7q7CdNWDAtt/1Wke7yfb3/4qTPhQSrUKh6YVdjbdy6P8R2jXsGUN+Tif31J34=; yuidss=6656918781576960938; Session_id=3:1578501738.5.0.1576960999760:maOluQ:52.1|10892184.0.2|210737.662708.pU5NEJoFsJeXk9pbQdgJRxfsdRA; sessionid2=3:1578501738.5.0.1576960999760:maOluQ:52.1|10892184.0.2|210737.513250.gyYbPjoXKehH9cxQbL7dFYN9Ifc; yandex_gid=213; discussion=1; _ym_isad=1; yp=1892320940.yrtsi.1576960940#1892320999.udn.cDrQktCw0LvQvtCyICDQkNC70LXQutGB0LDQvdC00YA%3D#1581218194.ygu.1#1594394198.szm.1:1920x1080:1920x972; my=YwA=; _ym_d=1578672505; FgkKdCjPqoMFm=1; yabs-frequency=/4/0000000000000000/DEToS3GvGG00/; zm=m-white_bender.gen.webp.css-https%3As3home-static_SYOvmzwVVZamdFswMcLoUeRxCbU%3Al; skid=1270000231578672506; visits=1578672506-1578672506-1578672506; cpa-pof=%7B%22clid%22%3A%5B%22505%22%5D%2C%22mclid%22%3Anull%2C%22distr_type%22%3Anull%2C%22vid%22%3Anull%2C%22opp%22%3Anull%7D; utm_campaign=face_abovesearch; utm_source=face_abovesearch; uid=AABcEl4YoXp6GACtBzxfAg==; js=1; dcm=1; first_visit_time=2020-01-10T19%3A08%3A27%2B03%3A00; currentRegionId=213; currentRegionName=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%83; fonts-loaded=1; ugcp=1; _ym_visorc_160656=b; _ym_visorc_45411513=b; parent_reqid_seq=de7c1f7308ec8198b4c5a3226939ab25%2C5f08daa8bd1f9124a244a24cfccb85af%2C9c7a30e0a23ed200d5d7404e97ce5e4d%2Cd31777918b4aabbea6043b0dfa5a44b2%2C7fae88bbb4f4ea4ae37714ce45c0b8c4',
        }


        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.content, 'html.parser')

        img_src = soup.find('img', attrs={'class': 'n-gallery__image image'}).attrs['src']
        print(img_src)

        div_price = soup.find('div', attrs={'class': 'n-product-summary__default-offer-container'}).find('div', attrs={'class': 'n-product-price-cpa2__price'}).find('span', attrs={'class': 'price'})


        return {'text': div_price.text, 'image': 'https:' + img_src}