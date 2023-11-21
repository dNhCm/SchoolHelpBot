
from aiogram import types, Router
from aiogram.filters import Command

from tgbot.filters.is_private import IsPrivate
from tgbot.filters.is_admin import IsAdmin
from tgbot.routers.base.scripts.commands_callbacks import resumed_algorythm


async def resume(message: types.Message):
    from algorythms.subjects_algorythm.subjects import SubjectAlgorythm

    if SubjectAlgorythm.resume():
        await resumed_algorythm(message)
    else:
        await message.answer('subject and good morning algorithm have already working!')


def register(router: Router):
    router.message.register(resume, Command('resume'), IsAdmin(), IsPrivate())
