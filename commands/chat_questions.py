import logging
from aiogram.bot import Bot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import *

class CommandChatQuestions:
    def __init__(self, bot: Bot, logger: logging.Logger=None):
        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandChatQuestions")

        self.send_message = self.bot.send_message

    async def main(self, message):
        message_questions = await self.bot.send_message(message.chat.id, 'Напишите вопрос ответом на это сообщение')