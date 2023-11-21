from aiogram import types, Router
from aiogram.filters import Command

from tgbot.filters.is_private import IsPrivate


async def time_schedule(message: types.Message):
    photo = open('data/time_schedule/schedule.png', 'rb')
    await message.bot.send_photo(chat_id=message.from_id, photo=photo)


def register(router: Router):
    router.message.register(time_schedule, Command('time_schedule'), IsPrivate())
