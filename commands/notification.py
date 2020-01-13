import logging
from aiogram.bot import Bot

from config import *

class CommandNotification:
    def __init__(self, bot: Bot, logger: logging.Logger=None):
        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandHandlers")

        self.send_message = self.bot.send_message

    async def main(self, message):
        await message.reply(text="Something awesome is coming soon")
