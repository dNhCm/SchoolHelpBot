from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def time_schedule(message: types.Message):
    with open('data/time_schedule/schedule.txt', 'r', encoding='UTF-8') as f:
        text = ''.join(f.readlines())

    await message.answer(text)


def register_time_schedule(dp: Dispatcher):
    dp.register_message_handler(time_schedule, Command('time_schedule'), IsPrivate())