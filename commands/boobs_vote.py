import logging
from aiogram.dispatcher import Dispatcher
from aiogram.bot import Bot
import db as db

from . import commands

class CommandBoobsVote(commands):
    def __init__(self, dp: Dispatcher, bot: Bot, logger: logging.Logger=None):
        self.dp = dp
        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandChatQuestions")

        self.db = db.DBBoobsVote(self.logger)
        self.send_message = self.bot.send_message