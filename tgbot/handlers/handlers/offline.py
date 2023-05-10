from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def offline(message: types.Message):
    photo = open('data/offline/offline.png', 'rb')
    await message.bot.send_photo(chat_id=message.chat.id, photo=photo)


def register_offline(dp: Dispatcher):
    dp.register_message_handler(offline, Command('offline'), IsPrivate())