import os
from asyncio import Task

from aiogram import types, Router
from aiogram.filters import Command

from algorythms.misc.str_time_to_arrow import str_to_arrow
from algorythms.subjects_algorythm.subjects import SubjectAlgorythm
from misc.root import get_root
from tgbot.filters.is_private import IsPrivate
from tgbot.filters.is_admin import IsAdmin
from tgbot.routers.base.scripts.commands_callbacks import successful_change


async def format_ex_msg(message: types.Message):
    await message.answer('/change <str(time in format "H:mm")> <str(subject from subject list)>', parse_mode='MARKDOWN')


async def change(message: types.Message):
    args = message.get_args().split(' ')

    # Checkpoints for correct args
    if len(args) != 2:
        await format_ex_msg(message); return
    try:
        str_to_arrow(args[0]); time = args[0]
    except:
        await format_ex_msg(message); return
    if args[1] == '[':
        subjects = [args[1][2:-2].split("', '")]
    else:
        subjects = [args[1]]
    for subject in subjects:
        if not subject in [subject[:-4] for subject in os.listdir(get_root()+'/data/subjects')]:
            await format_ex_msg(message); return

    # Change and get callback from it
    change_callback: bool | Task
    if len(subjects) == 0:
        change_callback = SubjectAlgorythm.change(time=time, subject=subjects[0])
    else: change_callback = SubjectAlgorythm.change(time=time, subject=subjects)

    # Check for answer, and feedback to user
    if type(change_callback) is bool:
        if change_callback:
            await successful_change(message, args)
        else:
            await message.answer('You had writen incorrectly time or subject')
    elif type(change_callback) is Task:
        await successful_change(message, args)
        await change_callback


def register(router: Router):
    router.message.register(change, Command('change'), IsAdmin(), IsPrivate())
