import os

from aiogram import types, Router
from aiogram.filters import Command

from misc.root import get_root
from tgbot.filters.is_private import IsPrivate
from tgbot.filters.is_admin import IsAdmin


async def subject_list(message: types.Message):
    subjects = os.listdir(get_root() + "/data/subjects")
    for i, subject in enumerate(subjects):
        subjects[i] = subject[:-4]
    subjects = '\n'.join(subjects)

    await message.answer(text=subjects)


def register(router: Router):
    router.message.register(subject_list, Command('subject_list'),IsAdmin(), IsPrivate())
