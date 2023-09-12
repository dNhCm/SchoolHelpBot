import os

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from misc.get_project_path import get_project_path
from tgbot.handlers.filters import IsPrivate
from tgbot.handlers.filters.is_admin import IsAdmin


async def subject_list(message: types.Message):
    subjects = os.listdir(get_project_path() + "\\data\\subjects")
    for i, subject in enumerate(subjects):
        subjects[i] = subject[:-4]
    subjects = '\n'.join(subjects)

    await message.answer(text=subjects)


def register_subject_list(dp: Dispatcher):
    dp.register_message_handler(subject_list, Command('subject_list'),IsAdmin(), IsPrivate())