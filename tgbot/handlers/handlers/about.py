from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def about(message: types.Message):
    text = '''Цей бот створен для того, щоб відправляти корректні силки та коди до уроків по розкладу, та попереджувати коли буде наступний урок та який.
Рад пройденим шляхом та результатом!
Подивитися код можна по силці: https://github.com/dNhCm/SchoolHelpBot'''
    await message.answer(text=text)


def register_about(dp: Dispatcher):
    dp.register_message_handler(about, Command('about'), IsPrivate())