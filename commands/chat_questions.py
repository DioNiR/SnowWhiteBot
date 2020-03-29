import logging
from aiogram.bot import Bot
from aiogram.utils.markdown import text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import *

from db import *

class CommandChatQuestions:
    answers = {}

    def __init__(self, bot: Bot, logger: logging.Logger=None):
        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandChatQuestions")

        self.db = db(self.logger)

        self.send_message = self.bot.send_message

    async def create_question(self, message):
        message_question = await self.bot.send_message(message.chat.id, 'Напишите вопрос ответом на это сообщение')
        print(message_question)

        self.message_question_id = message_question['message_id']

    async def my_questions(self, message):
        questions = ["Ваши вопросы:\n"]

        for row in self.db.select_questions_by_author(message['from']['id']):
            questions.append(f'{row[3]}\n')

        message_text = text(*questions)
        await message.reply(text=message_text)

    async def question(self, message):
        row = self.db.select_random_questions(message['from']['id'])
        print(row)

    async def main(self, message):
        if 'reply_to_message' in message:
            reply_id = message['reply_to_message']['message_id']

            if reply_id == self.message_question_id:
                await self.text_question(message)
            else:
                print(message)
                print(reply_id)

                question = self.db.select_question_by_message_id(reply_id)
                print(question)
                if question is not None:
                    await self.text_answer(question, message)

                answer = self.db.select_answer_by_message_id(reply_id)
                print(answer)
                if answer is not None:
                    await self.points(answer, message)
        else:
            pass

    async def text_question(self, message):
        self.question_name = message['text']

        message_text = text(
            f"Вопос: {self.question_name}, создан.",
            "Для добавления ответов на вопрос, отвечайте на это сообщение"
        )

        message_question_add_success = await message.reply(text = message_text)
        self.db.insert_question(self.question_name, message_question_add_success['message_id'], message['from']['id'])

     

    async def text_answer(self, question, message):
        answer_name = message['text']

        message_text = text(
            f"Ответ: {answer_name}, добавлен.",
            "Ответом на это сообщение, соообщите:",
            "Сколько балов мерзости добавить человеку за этот ответ",
            "1 бал мерзости будет добавлен по умолчанию",
            "Но не больше 10",
        )

        message_answer_add_success = await message.reply(text = message_text)
        self.db.insert_answer(question[0], message_answer_add_success['message_id'], answer_name)

    async def points(self, answer, message):
        point_number = int(message['text'])

        if point_number < 11 and point_number > 0:
            message_text = text(
                f"Установленно {point_number} мерзости на ответ: {answer[3]}.",
            )

            await message.reply(text = message_text)
            self.db.update_answer_points_by_id(int(answer[0]), point_number)