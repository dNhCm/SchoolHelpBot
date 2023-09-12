from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from bot import logger
from tgbot.handlers.filters import IsPrivate
from tgbot.handlers.filters.is_admin import IsAdmin
from tgbot.misc.commands_callbacks import stopped_algorythm


async def stop(message: types.Message):
    from algorythms.subjects_algorythm.subjects import SubjectAlgorythm

    if SubjectAlgorythm.stop():
        await stopped_algorythm(message)
    else:
        await message.answer('subject and good morning algorithms have already stopped')


def register_stop(dp: Dispatcher):
    dp.register_message_handler(stop, Command('stop'), IsAdmin(), IsPrivate())