from aiogram import types, Router
from aiogram.filters import Command

from tgbot.filters.is_private import IsPrivate


async def subjects_schedules(message: types.Message):
    photo = open('data/subjects_schedules/schedules.png', 'rb')
    await message.bot.send_photo(chat_id=message.from_id, photo=photo)


def register(router: Router):
    router.message.register(subjects_schedules, Command('subjects_schedules'), IsPrivate())
