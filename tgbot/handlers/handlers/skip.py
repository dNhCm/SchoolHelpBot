from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from tgbot.handlers.filters import IsPrivate
from tgbot.handlers.filters.is_admin import IsAdmin
from tgbot.misc.commands_callbacks import set_skips


async def format_ex_msg(message: types.Message):
    await message.answer('/skip <int(count of loop to skip)>')


async def skip(message: types.Message):
    from algorythms.subjects_algorythm.subjects import SubjectAlgorythm

    args = message.get_args()
    try: skips = int(args)
    except: await format_ex_msg(message); return

    await set_skips(message, skips)
    await SubjectAlgorythm.skip(skips)


def register_skip(dp: Dispatcher):
    dp.register_message_handler(skip, Command('skip'), IsAdmin(), IsPrivate())