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

from config import *
from db import *

bot = Bot(token=TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)

db = db()


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['(.*)']))
async def process_tetetet_command(message: types.Message):
    print(1222222222222222)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(text="Привет.\n Я Бот белоснежка")

    await bot.send_photo(message.chat.id, PHOTOS[1])

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    button_say = KeyboardButton('/скажи')
    button_call = KeyboardButton('/вызывай')
    button_cause = KeyboardButton('/вызвать')
    button_stop = KeyboardButton('/хватит')

    greet_kb = ReplyKeyboardMarkup()
    greet_kb.add(button_say)
    greet_kb.add(button_call)
    greet_kb.add(button_cause)
    greet_kb.add(button_stop)

    await message.reply(help_message, reply_markup=greet_kb)

@dp.message_handler(commands=['хватит'])
async def process_enough_command(message: types.Message):
    global enough, call, chat_id
    call = 0
    enough = True

@dp.message_handler(commands=['шутка'])
async def process_enough_command(message: types.Message):
    await bot.send_photo(message.chat.id, PHOTOS[2])

@dp.message_handler(commands=['скажи'])
async def process_say_command(message: types.Message):
    global enough, call, call_time, call_text, chat_id

    command, *args = list(message.text.split())

    await bot.send_message(message.chat.id, ' '.join(args))

async def process_call(message, text):
    global enough, call, call_time, call_text, chat_id

    while True:
        if enough == True:
            break

        now = datetime.now()

        if call_time != 0:
            hour, minute = call_time.split(':')
            if int(now.hour) == int(hour) and int(now.minute) > int(minute):
                break

        await bot.send_message(message.chat.id, call_text)
        await asyncio.sleep(3)

async def function_call(message, args):
    global call, call_text, datetime, bot, enough, call_time

    nick = args[0]

    ignore = False

    for ignore_nick in ignore_nicks:
        if ignore_nick.lower() in nick.lower():
            ignore = True

    if ignore == False:
        if list(nick)[0] != '@':
            await bot.send_message(message.chat.id, 'Кого кого?')
        else:
            enough = False
            if call == 0:
                call = 1
                call_text = nick

                if len(args) == 2:
                    if list(args[1])[2] == ':':
                        hour, minute = args[1].split(':')

                        now = datetime.now()
                        if int(now.hour) == int(hour) and int(now.minute) >= int(minute):
                            await bot.send_message(message.chat.id, 'Ты на время посмотри!')


                        else:
                            call_time = args[1]
                            await process_call(message, nick)
                else:
                    await process_call(message, nick)
            else:
                call_text += ' ' + nick
    else:
        await bot.send_photo(message.chat.id, PHOTOS[3], reply_to_message_id = message.message_id)


@dp.message_handler(commands=['вызывай'])
async def process_call_command(message: types.Message):
    global enough, call, call_time, call_text, chat_id

    command, *args = list(message.text.split())

    print(args)

    if len(args) == 0:
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        members = db.select_chat_members_by_chat_id(chat_id = message.chat.id)
        print(members)

        for member in members:
            inline_btn = InlineKeyboardButton(member[3], switch_inline_query = str(member[2]), callback_data = 'cause_' + str(member[2]))
            inline_kb_full.add(inline_btn)

        await message.reply("Кого вызвать?", reply_markup= inline_kb_full)
    else:
        await function_call(message, args)


@dp.message_handler(commands=['вызвать'])
async def process_cause_command(message: types.Message):
    global enough, call, call_time, call_text, chat_id

    command,*args = list(message.text.split())

@dp.message_handler(commands=['tests'])
async def process_command_1(message: types.Message):
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    members = db.select_chat_members_by_chat_id(chat_id = message.chat.id)

    for member in members:
        inline_btn = InlineKeyboardButton(member[3], switch_inline_query = str(member[2]), callback_data = 'cause_' + str(member[2]))
        inline_kb_full.add(inline_btn)

    await message.reply("Кого вызвать?", reply_markup= inline_kb_full)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cause_'))
async def process_callback_kb_cause(callback_query: types.CallbackQuery):
    print(callback_query)
    print(callback_query.id)
    print(callback_query.message.reply_to_message.message_id)
    print(callback_query.message.message_id)
    print(callback_query.data.split('_'))

    data = callback_query.data.split('_')
    select = db.select_chat_members_by_user_id(chat_id = callback_query.message.chat.id, user_id = data[1])

    await bot.delete_message(chat_id = callback_query.message.chat.id, message_id = callback_query.message.message_id)

    args = ['@' + select[3]]

    print(args)

    await function_call(callback_query.message.reply_to_message, args)

@dp.message_handler(commands=['test'])
async def process_test_command(message: types.Message):
    global enough, call, call_time, call_text, chat_id

    command,*args = list(message.text.split())

    print()

@dp.message_handler(commands=['testss'])
async def process_test_command(message: types.Message):
    content = []

    content.append(escape_md({'offset': 0, "length": 5, "user_id": 350185551}))

    await bot.send_message(message.chat.id, text(*content, sep='\n'), parse_mode = ParseMode.MARKDOWN)

    print()

@dp.message_handler()
async def echo_message(message: types.Message):
    print(message.from_user.id)
    print(type(message.from_user.id))
    print(int(message.from_user.id))

    select = db.select_chat_members_by_user_id(chat_id = message.chat.id, user_id = message.from_user.id)
    print(select)

    if select == None:
        user_name =  ''
        if 'username' in message.from_user:
            user_name =  message.from_user.username

        db.insert_chat_members_data(chat_id = message.chat.id, user_id = message.from_user.id, user_name = user_name)

    if str(message.chat.id) != '-1001415606536':
        print('Написать в чат')
        #await bot.send_message(chat_id, message.text)
        await bot.send_message(message.chat.id, 'Анонимное общение пока приостановленно.')
    else:
        print(message)
        #print('Не пишем в чат')

@dp.message_handler(content_types='photo')
async def photo_message(message: types.Message):
    print(message.photo[-1].file_id)

if __name__ == '__main__':
    executor.start_polling(dp)