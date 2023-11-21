from aiogram import types, Router
from aiogram.filters import Command

from tgbot.filters.is_private import IsPrivate
from tgbot.filters.is_admin import IsAdmin
from tgbot.routers.base.scripts.commands_callbacks import stopped_algorythm


async def stop(message: types.Message):
    from algorythms.subjects_algorythm.subjects import SubjectAlgorythm

    if SubjectAlgorythm.stop():
        await stopped_algorythm(message)
    else:
        await message.answer('subject and good morning algorithms have already stopped')


def register(router: Router):
    router.message.register(stop, Command('stop'), IsAdmin(), IsPrivate())
