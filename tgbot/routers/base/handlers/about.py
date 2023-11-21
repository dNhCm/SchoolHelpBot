from aiogram import types, Router
from aiogram.filters import Command

from tgbot.filters.is_private import IsPrivate


async def about(message: types.Message):
    text = '''Цей бот створен для того, щоб відправляти корректні силки та коди до уроків по розкладу, та попереджувати коли буде наступний урок та який.
Рад пройденим шляхом та результатом!
Подивитися код можна по силці: https://github.com/dNhCm/SchoolHelpBot'''
    await message.answer(text=text)


def register(router: Router):
    router.message.register(about, Command('about'), IsPrivate())
