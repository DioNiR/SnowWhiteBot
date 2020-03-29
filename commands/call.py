import logging
import asyncio

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils.markdown import text, bold, italic, code, pre, escape_md
import aiohttp_socks 
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import *
from db import *

import datetime

class CommandCall:
    call_starting   = 0
    chat_id = ''
    call_time = None
    call_text = None

    commands = {
        'вызывай': 'command_call',
        'вызвать': 'command_cause',
        'хватит': 'command_enough',
    }

    command_obj = {}

    def __init__(self, bot: Bot, db: db, logger: logging.Logger=None):
        self.enough_status = False

        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandHandlers")
        self.db = db
        self.send_message = self.bot.send_message

    async def main(self, message, *args, **kwargs):
        pass


    async def check_chat_obj(self, id):
        """Функция проверки экзепляра класса опредленного чата

        Keyword arguments:
        id -- id чата

        """
        if id not in self.command_obj:
            self.command_obj[id] = CommandCall(self.bot, self.db)
        

    async def call(self, message, *args, **kwargs):
        """Функция комманда /вызывай

        Keyword arguments:
        message -- сообщение из чата
        args -- args
        kwargs -- kwargs

        """

        chat_id = message.chat.id

        await self.check_chat_obj(chat_id)
        await self.command_obj[chat_id].command_call(message, args)

    async def enough(self, message, *args, **kwargs):
        """Функция комманда /хватит

        Keyword arguments:
        message -- сообщение из чата
        args -- args
        kwargs -- kwargs

        """
        chat_id = message.chat.id

        await self.check_chat_obj(chat_id)
        await self.command_obj[chat_id].command_enough(message)

    async def ogyrec(self, message):
        await message.reply("Извините пользователи с низким IQ не могут вызывать людей")

    async def empty_nick(self, message):
        """Функция если ника нет. то надо показать кнопки

        Keyword arguments:
        message -- сообщение из чата
        args -- args

        """

        message_from_id = message['from']['id']

        inline_kb_full = InlineKeyboardMarkup(row_width = 2)
        members = self.db.select_chat_members_by_chat_id(chat_id = message.chat.id)

        for member in members:
            inline_btn = InlineKeyboardButton(member[3], switch_inline_query = str(member[2]), callback_data = f'cause_{member[2]}_{message_from_id}')
            inline_kb_full.add(inline_btn)

        await message.reply("Кого вызвать?", reply_markup = inline_kb_full)

    async def process_callback_kb_cause(self, callback_query: types.CallbackQuery):
        """Функция процесс обработки нажатие кнопки

        Keyword arguments:
        callback_query -- клик на кнопку

        """

        click_from_id = callback_query['from']['id']
        data = callback_query.data.split('_')

        if str(click_from_id) == str(data[2]):
            await self.bot.delete_message(chat_id = callback_query.message.chat.id, message_id = callback_query.message.message_id)
            await self.function_call(callback_query.message.reply_to_message, chat_id = callback_query.message.chat.id, user_id = data[1])
        else:
            nick = ''
            if callback_query['from']['username']:
                nick = callback_query['from']['username']
            else:
                first_name = nick = callback_query['from']['first_name']
                nick = f'[{first_name}](tg://user?id={click_from_id})'

            error_text = f'{nick} ты че делаешь?'
            await self.bot.send_message(callback_query.message.chat.id, error_text)


    async def callback_kb_cause(self, callback_query: types.CallbackQuery):
        """Функция обработки нажатие кнопки

        Keyword arguments:
        callback_query -- клик на кнопку

        """
        chat_id = callback_query.message.chat.id

        await self.check_chat_obj(chat_id)
        await self.command_obj[chat_id].process_callback_kb_cause(callback_query)


    async def command_call(self, message, args):
        """Функция обработки комманды вызова

        Keyword arguments:
        message -- сообщение из чата
        args -- args

        """

        if len(args) == 0:
            await self.empty_nick(message)
            return
        else:
            await message.reply("Нет уж, выбирай")
            await self.empty_nick(message)


    async def command_enough(self, message: types.Message):
        """Функция комманды остановки вызова

        Keyword arguments:
        message -- сообщение из чата

        """

        self.call_starting = 0
        self.enough_status = True


    async def process_call(self, message, text):
        """Функция которая пишет ник в чат

        Keyword arguments:
        message -- сообщение из чата
        text -- текст

        """

        while True:
            if self.enough_status == True:
                break

            await self.bot.send_message(chat_id = message.chat.id, 
                                        text = self.call_text, 
                                        parse_mode=ParseMode.MARKDOWN)
            await asyncio.sleep(3)

    async def ignore_nick(self, nick):
        ignore = False

        for ignore_nick in ignore_nicks:
            if ignore_nick.lower() in nick.lower():
                ignore = True

        return ignore

    async def function_call(self, message, chat_id, user_id):
        """Функция которая проверяет на игнорирование и формирует текст который будет писаться

        Keyword arguments:
        message -- сообщение из чата
        chat_id -- id чата
        user_id -- id пользователя которого вызывают

        """

        user_select = self.db.select_chat_members_by_user_id(chat_id = chat_id, user_id = user_id)    
        if not user_select:
            await self.bot.send_message(chat_id, 'Кого кого?')
            return
        
        nick = user_select[3]

        if await self.ignore_nick(nick) == False:
            self.enough_status = False
            if self.call_starting == 0:
                self.call_starting = 1
                self.call_text = f'[{user_select[3]}](tg://user?id={user_select[2]})'

                await self.process_call(message, nick)
            else:
                self.call_text += f' [{user_select[3]}](tg://user?id={user_select[2]})'
        else:
            await self.bot.send_photo(chat_id, PHOTOS[3], reply_to_message_id = message.message_id)