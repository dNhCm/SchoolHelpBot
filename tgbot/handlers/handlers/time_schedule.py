from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def schedules(message: types.Message):
    with open('data/time_schedule/time_schedule.txt', 'r', encoding='UTF-8') as f:
        text = ''.join(f.readlines())

    await message.answer(text)


def register_schedules(dp: Dispatcher):
    dp.register_message_handler(schedules, Command('time_schedule'), IsPrivate())