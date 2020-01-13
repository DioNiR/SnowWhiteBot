import logging
from aiogram.bot import Bot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import *

class CommandHelp:
    def __init__(self, bot: Bot, logger: logging.Logger=None):
        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandHelp")

        self.send_message = self.bot.send_message

    async def main(self, message):
        button_say = KeyboardButton('/скажи')
        button_call = KeyboardButton('/вызывай')
        button_cause = KeyboardButton('/вызвать')
        button_stop = KeyboardButton('/хватит')

        kb = ReplyKeyboardMarkup()
        kb.add(button_say)
        kb.add(button_call)
        kb.add(button_cause)
        kb.add(button_stop)

        await message.reply(help_message, reply_markup = kb)
