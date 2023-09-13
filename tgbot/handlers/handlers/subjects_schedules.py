from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def subjects_schedules(message: types.Message):
    photo = open('data/subjects_schedules/schedules.png', 'rb')
    await message.bot.send_photo(chat_id=message.from_id, photo=photo)


def register_subjects_schedules(dp: Dispatcher):
    dp.register_message_handler(subjects_schedules, Command('subjects_schedules'), IsPrivate())