import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from bot import logger
from tgbot.handlers.filters import IsPrivate
from tgbot.handlers.filters.is_admin import IsAdmin
from tgbot.misc.commands_callbacks import resumed_algorythm


async def resume(message: types.Message):
    from algorythms.subjects_algorythm.subjects import SubjectAlgorythm

    if SubjectAlgorythm.resume():
        await resumed_algorythm(message)
    else:
        await message.answer('subject and good morning algorithm have already working!')


def register_resume(dp: Dispatcher):
    dp.register_message_handler(resume, Command('resume'), IsAdmin(), IsPrivate())