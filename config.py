from aiogram.utils.markdown import text
from aiogram.types import KeyboardButton

MY_ID = 272590789

DB_FILENAME = 'botuploads.db'
#Dev
#TOKEN = '1043413769:AAHV6QU-_N4CKX0rtIClVDLD6Z1wNUUNySc'

# Prod
TOKEN = '753135015:AAE398rDss1bLXVLbpQKFLmu20iarSDS9ug'

PROXY_URL = 'socks5://learn:python@t1.learn.python.ru:1080' 

chat_id = '-1001415606536'

ignore_nicks = ['DioNiR', 'DimkaSnowWhiteBot',]
#ignore_nicks = []


help_message = text(
    "Доступные команды:\n",
    "/start - приветствие\n",
    sep="\n"
)

PHOTOS = [
    'AgADAgADKawxG5HJ4UsNHS9NdJs-KVjVuQ8ABAEAAwIAA20AA2X3BgABFgQ',
    'AgADAgAD0KsxGxYl4Uv_HyYbPlXbR7UpwQ4ABAEAAwIAA20AA7xeAAIWBA',
    'AgADAgADtq0xG5nH4UsJWzlSSCfidRDZug8ABAEAAwIAA20AA7n5BgABFgQ',
    'AgADAgAD06sxGxYl4UviVIAVnYPRMwABdlwPAAQBAAMCAANtAAP4AAEDAAEWBA',
    'AgADAgAD1asxGxYl4UvfMbtxd_KGeMHWuQ8ABAEAAwIAA20AA9z1BgABFgQ',
]
'''
RANDOM_PHOTOS [
    '1',
]
'''

UNDER_CONSTRUCTION = 'AgADAgAD_KsxG5HJ6Uvw3pDITRONS_NqXA8ABAEAAwIAA3gAA_wRAwABFgQ'
buttons = []
buttons.append([KeyboardButton('/говори'),   KeyboardButton('/замолчи')])
buttons.append([KeyboardButton('/вызывай'), KeyboardButton('/хватит')])
buttons.append([KeyboardButton('/погода'), KeyboardButton('/ps4')])