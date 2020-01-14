import logging
from aiogram.bot import Bot
from aiogram.utils.markdown import text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import *

class CommandChatQuestions:
    answers = []

    def __init__(self, bot: Bot, logger: logging.Logger=None):
        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandChatQuestions")

        self.send_message = self.bot.send_message

    async def create_question(self, message):
        message_question = await self.bot.send_message(message.chat.id, 'Напишите вопрос ответом на это сообщение')
        print(message_question)

        self.message_question_id = message_question['message_id']

    async def main(self, message):

        if message['reply_to_message']['message_id'] == self.message_question_id:
            await self.text_question(message)

        elif message['reply_to_message']['message_id'] == self.message_question_add_success_id:
            await self.text_answer(message)

    async def text_question(self, message):
        self.question_name = message['text']

        message_text = text(
            f"Вопос: {self.question_name}, создан.\n",
            "Для добавления ответов на вопрос, отвечайте на это сообщение"
        )

        message_question_add_success = await message.reply(text = message_text)
        self.message_question_add_success_id = message_question_add_success['message_id']

        print(message)     

    async def text_answer(self, message):
        answer_name = message['text']

        self.answers.append(message['text'])

        message_text = text(
            f"Ответ: {answer_name}, добавлен.\n",
            "Ответом на это сообщение, соообщите:\n",
            "Сколько балов мерзости добавить человеку за этот ответ\n",
            "1 бал мерзости будет добавлен по умолчанию",
        )

        message_answer_add_success = await message.reply(text = message_text)

        print(message)   