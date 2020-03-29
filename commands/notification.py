import logging

from aiogram.dispatcher import Dispatcher
from aiogram.bot import Bot

from . import commands

class CommandNotification(commands):
    def __init__(self, dp: Dispatcher, bot: Bot, logger: logging.Logger=None):
        self.bot = bot
        self.dp = dp
        self.logger = logger if logger is not None else logging.getLogger("CommandHandlers")

        self.send_message = self.bot.send_message

    async def main(self, message):
        await message.reply(text="Something awesome is coming soon")
