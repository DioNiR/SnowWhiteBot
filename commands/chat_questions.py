import logging

from aiogram import types
from aiogram.bot import Bot
from aiogram.types import ParseMode
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
        question_row = self.db.select_random_questions(message['from']['id'])
        answers_row  = self.db.select_question_answers(question_id = question_row[0][0])

        question_id = question_row[0][0]

        messages = [f'{question_row[0][3]}\n']
        inline_btn = []
        inline_kb_full = InlineKeyboardMarkup()


        a = 0
        for answer in answers_row:
            a += 1
            messages.append(f'{a}. {answer[3]}\n')

            inline_btn.append(InlineKeyboardButton(a, callback_data = f'vote_{question_id}_{answer[0]}'))

        inline_kb_full.row(*inline_btn)


        await self.bot.send_message(message.chat.id, text(*messages), reply_markup = inline_kb_full)

    async def callback_kb_vote(self, callback_query: types.CallbackQuery):
        print(callback_query)

        data = callback_query.data.split('_')

        question_id = data[1]
        answer_id   = data[2]
        user_id     = callback_query.message['from']['id']

        is_vote = self.db.ckeck_answer_user_vote(question_id, answer_id, user_id)
        print(is_vote)

        if is_vote == None:
            await self.bot.answer_callback_query(callback_query.id, text='Ваш голос засчитан', show_alert=True)
            points = self.db.get_answer_points_by_id(answer_id)
            self.db.add_answer_vote(question_id, answer_id, user_id, points = points[0])
        else:
            await self.bot.answer_callback_query(callback_query.id, text='Вы уже голосовали', show_alert=True)



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