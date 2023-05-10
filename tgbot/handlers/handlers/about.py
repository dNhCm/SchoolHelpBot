from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def about(message: types.Message):
    await message.answer('Цей бот допоможе 10-Б, а саме Дані, не шукати правильні посилання на уроки вручну. Дані сумно, що він зробив цього бота лише під кінець начального року, а не на початку. Але се одно рад пройденим шляхом та результатом!\nПосмотреть код можете по ссылке: https://github.com/dNhCm/SchoolHelpBot')


def register_about(dp: Dispatcher):
    dp.register_message_handler(about, Command('about'), IsPrivate())