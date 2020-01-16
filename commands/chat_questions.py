import logging
from aiogram.bot import Bot
from aiogram.utils.markdown import text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import *

class CommandChatQuestions:
    answers = {}

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
            await self.text_answer(self.message_question_add_success_id, message)
        elif message['reply_to_message']['message_id'] in self.answers[self.message_question_add_success_id]:
            print('?????????????????????')
            print(self.answers[self.message_question_add_success_id])
            await self.points(message)
            print('????????????????????')

        if self.answers[self.message_question_add_success_id]:
            print(message['reply_to_message']['message_id'])
            print(self.answers[self.message_question_add_success_id])
        if message['reply_to_message']['message_id'] in self.answers[self.message_question_add_success_id]:
            print('###############')
            print(self.answers[self.message_question_add_success_id])
            print('###############')

    async def text_question(self, message):
        self.question_name = message['text']

        message_text = text(
            f"Вопос: {self.question_name}, создан.\n",
            "Для добавления ответов на вопрос, отвечайте на это сообщение"
        )

        message_question_add_success = await message.reply(text = message_text)
        self.message_question_add_success_id = message_question_add_success['message_id']

        print(message)     

    async def text_answer(self, message_question_id, message):
        answer_name = message['text']

        message_text = text(
            f"Ответ: {answer_name}, добавлен.",
            "Ответом на это сообщение, соообщите:",
            "Сколько балов мерзости добавить человеку за этот ответ",
            "1 бал мерзости будет добавлен по умолчанию",
            "Но не больше 10",
        )

        print('------------------------------------------')

        message_answer_add_success = await message.reply(text = message_text)
        print(message_answer_add_success)

        if message_question_id in self.answers:
            self.answers[message_question_id][message_answer_add_success['message_id']] = message['text']
        else:
            self.answers[message_question_id] = {}
            self.answers[message_question_id][message_answer_add_success['message_id']] = message['text']

        print(self.answers) 

        print('------------------------------------------')

    async def points(self, message):
        point_number = message['text']
        answer_text = self.answers[self.message_question_add_success_id][message['reply_to_message']['message_id']]

        message_text = text(
            f"Установленно {point_number} мерзости на ответ: {answer_text}.",
            "Напишите !завершить для завершения создания вопроса или начните создавать новый вопрос с комманды !создать вопрос",
        )

        await message.reply(text = message_text)