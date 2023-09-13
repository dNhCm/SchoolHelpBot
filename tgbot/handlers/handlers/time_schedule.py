from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def time_schedule(message: types.Message):
    photo = open('data/time_schedule/schedule.png', 'rb')
    await message.bot.send_photo(chat_id=message.from_id, photo=photo)


def register_time_schedule(dp: Dispatcher):
    dp.register_message_handler(time_schedule, Command('time_schedule'), IsPrivate())