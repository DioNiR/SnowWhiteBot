import logging
import asyncio
import os
import datetime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils.markdown import text, bold, italic, code, pre, escape_md
import aiohttp_socks 
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import *
from db import *


import commands as command

logging.basicConfig(filename="bot.log", level=logging.INFO)

logger = logging.getLogger("SnowWhiteBot")


bot = Bot(token=TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)
db = db(logger)


scheduler = AsyncIOScheduler()

command_call = command.CommandCall(bot, db, logger)
command_notification = command.CommandNotification(bot)
command_start = command.CommandStart(bot)
command_help = command.CommandHelp(bot)
command_weather = command.CommandWeather(bot, scheduler)
command_ps4 = command.CommandPS4(bot, scheduler)
command_chat_questions = command.CommandChatQuestions(bot, scheduler)

dp.register_message_handler(command_start.main, commands=["start"])
dp.register_message_handler(command_help.main, commands=["help"])

dp.register_message_handler(command_call.call, commands=["вызывай"])
dp.register_message_handler(command_call.enough, commands=["хватит"])
dp.register_callback_query_handler(command_call.callback_kb_cause, lambda c: c.data and c.data.startswith('cause_'))


dp.register_message_handler(command_weather.main, commands=["погода"])
dp.register_message_handler(command_ps4.main, commands=["ps4"])

dp.register_message_handler(command_chat_questions.main, regexp='\!создать вопрос')


@dp.message_handler()
async def listen_message(message: types.Message):
    logger.info(message)
    select_chat = db.select_chat_by_chat_id(chat_id = message.chat.id)
    if select_chat == None:
        db.insert_chat(chat_id = message.chat.id, chat_name = message.chat.title)

    select = db.select_chat_members_by_user_id(chat_id = message.chat.id, user_id = message.from_user.id)

    if select == None:
        user_name =  ''
        if 'username' in message.from_user:
            user_name =  message.from_user.username

        db.insert_chat_members_data(chat_id = message.chat.id, user_id = message.from_user.id, user_name = user_name)
    else:
        pass


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp)
    logging.debug("Bot stopped")