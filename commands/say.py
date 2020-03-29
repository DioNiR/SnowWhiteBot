import logging
import asyncio

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from . import commands

class CommandSay(commands):
    def __init__(self, dp: Dispatcher, bot: Bot, logger: logging.Logger = None):
        self.dp = dp

        self.bot = bot
        self.logger = logger if logger is not None else logging.getLogger("CommandStart")

        self.send_message = self.bot.send_message

        self.messages = []
        self.is_running = False

    def register_message_handler(self):
        self.dp.register_message_handler(self.say, commands=["говори"])
        self.dp.register_message_handler(self.shut_up, commands=["замолчи"])

    async def listen(self, message):
        await self.main(message)

    async def say(self, message):
        message_text = 'Ответом на это сообщение напиши что надо говорить'
        message_reply = await message.reply(text = message_text)

        self.messages.append({'reply_id': message_reply['message_id'], 'shut_up_status': False, 'chat_id': message.chat.id, 'text': ''})

        await self.process_say()

    async def shut_up(self, message):
        chat_id = message.chat.id

        for msg in self.messages:
            if msg['chat_id'] == chat_id:
                msg['shut_up_status'] = True

    async def main(self, message):
        reply_id = message['reply_to_message']['message_id']

        for msg in self.messages:
            if msg['reply_id'] == reply_id:
                msg['text'] = message['text']

        await self.process_say()

    async def process_say(self):
        if self.is_running == False:
            self.is_running = True
            while True:
                for msg in self.messages:
                    if msg['shut_up_status'] == False:
                        if msg['text'] != '':
                            await self.bot.send_message(chat_id = msg['chat_id'], text = msg['text'])
                await asyncio.sleep(3)