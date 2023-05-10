
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command


async def test(message: types.Message):
    await message.answer('I see')


def register_test(dp: Dispatcher):
    dp.register_message_handler(test, Command('test'))