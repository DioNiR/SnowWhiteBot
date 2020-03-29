import logging
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


from config import *

from . import commands

class CommandStart(commands):
    def __init__(self, dp: Dispatcher, bot: Bot, logger: logging.Logger=None):
        self.dp = dp

        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandStart")

        self.send_message = self.bot.send_message

    def register_message_handler(self):
        self.dp.register_message_handler(self.main, commands=["start"])


    async def main(self, message):
        await message.reply(text="Привет.\n Я Бот белоснежка")
        await self.bot.send_photo(message.chat.id, PHOTOS[1])

        button_say = KeyboardButton('/скажи')
        button_call = KeyboardButton('/вызывай')
        button_stop = KeyboardButton('/хватит')
        button_mikhail = KeyboardButton('/мишаня')

        greet_kb = ReplyKeyboardMarkup()
        greet_kb.add(button_say)
        greet_kb.add(button_call)
        greet_kb.add(button_stop)
        greet_kb.add(button_mikhail)

        await message.reply(help_message, reply_markup=greet_kb)