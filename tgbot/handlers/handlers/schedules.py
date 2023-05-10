from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def schedules(message: types.Message):
    with open('data/schedules/schedules.txt', 'r', encoding='UTF-8') as f:
        text = ''.join(f.readlines())

    await message.answer(text)


def register_schedules(dp: Dispatcher):
    dp.register_message_handler(schedules, Command('schedules'), IsPrivate())