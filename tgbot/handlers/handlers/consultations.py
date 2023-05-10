from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def consults(message: types.Message):
    with open('data/consultations/consultations_schedule.txt', 'r', encoding='UTF-8') as f:
        text = ''.join(f.readlines())

    await message.answer(text)


def register_consultations(dp: Dispatcher):
    dp.register_message_handler(consults, Command('consults'), IsPrivate())