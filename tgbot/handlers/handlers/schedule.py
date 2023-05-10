from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate


async def schedule(message: types.Message):
    photo = open('data/schedule/schedule.png', 'rb')
    await message.bot.send_photo(chat_id=message.chat.id, photo=photo)


def register_schedule(dp: Dispatcher):
    dp.register_message_handler(schedule, Command('schedule'), IsPrivate())