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
import db as db
import commands as command

logger = None

bot = Bot(token=TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)

logging.basicConfig(filename="bot.log", level=logging.DEBUG)
logger = logging.getLogger("SnowWhiteBot")

db_connect = db.old(logger)

scheduler = AsyncIOScheduler()

commands_class = {}

commands_class['call']           = command.CommandCall(dp, bot, db_connect)
commands_class['notification']   = command.CommandNotification(dp, bot, logger)
commands_class['start']          = command.CommandStart(dp, bot)
commands_class['help']           = command.CommandHelp(dp, bot)
commands_class['weather']        = command.CommandWeather(dp, bot, scheduler)
commands_class['ps4']            = command.CommandPS4(dp, bot, scheduler)
commands_class['chat_questions'] = command.CommandChatQuestions(dp, bot, scheduler)
commands_class['boobs']          = command.CommandBoobsVote(dp, bot, db_connect)

for commands_obj in commands_class:
   commands_class[commands_obj].register_message_handler()

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
    #scheduler.start()
    executor.start_polling(dp)
    logging.debug("Bot stopped")