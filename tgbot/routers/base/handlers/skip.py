from aiogram import types, Router
from aiogram.filters import Command

from tgbot.filters.is_private import IsPrivate
from tgbot.filters.is_admin import IsAdmin
from tgbot.routers.base.scripts.commands_callbacks import set_skips


async def format_ex_msg(message: types.Message):
    await message.answer('/skip <int(count of loop to skip)>', parse_mode='MARKDOWN')


async def skip(message: types.Message):
    from algorythms.subjects_algorythm.subjects import SubjectAlgorythm

    args = message.get_args()
    try: skips = int(args)
    except: await format_ex_msg(message); return

    await set_skips(message, skips)
    await SubjectAlgorythm.skip(skips)


def register(router: Router):
    router.message.register(skip, Command('skip'), IsAdmin(), IsPrivate())
