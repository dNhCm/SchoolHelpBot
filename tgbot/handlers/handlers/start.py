from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

from tgbot.handlers.filters import IsPrivate


async def start(message: types.Message):
    await message.answer('Добро дня, учню.\nТрохи про мене можна дізнатися через: /about\nА всі команди тут: /help')


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), IsPrivate())