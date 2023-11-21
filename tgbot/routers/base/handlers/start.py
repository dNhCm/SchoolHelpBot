from aiogram import types, Router
from aiogram.filters import CommandStart

from tgbot.filters.is_private import IsPrivate


async def start(message: types.Message):
    await message.answer('Добро дня, учню.\nТрохи про мене можна дізнатися через: /about\nА всі команди тут: /help')


def register(router: Router):
    router.message.register(start, CommandStart(), IsPrivate())
