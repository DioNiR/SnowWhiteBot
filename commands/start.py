import logging
from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


from config import *

from . import commands

class CommandStart(commands):
    def __init__(self, dp: Dispatcher, bot: Bot, logger: logging.Logger = None):
        self.dp = dp

        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandStart")

        self.send_message = self.bot.send_message

    def register_message_handler(self):
        self.dp.register_message_handler(self.main, commands=["start"])
        return self.dp


    async def main(self, message):
        greet_kb = ReplyKeyboardMarkup()
        for row in buttons:
            greet_kb.add(*row)

        await message.reply(text="Привет.\n Я Бот белоснежка 2.0", reply_markup=greet_kb)
        await self.bot.send_photo(message.chat.id, PHOTOS[1])
        await message.reply(text = help_message)