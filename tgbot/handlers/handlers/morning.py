from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from bot import logger
from tgbot.handlers.filters import IsPrivate
from tgbot.handlers.filters.is_admin import IsAdmin
from tgbot.misc.commands_callbacks import set_is_morning


async def format_ex_msg(message: types.Message):
    await message.answer('/morning <bool(0, 1)>', parse_mode='MARKDOWN')


async def morning(message: types.Message):
    from algorythms.morning_algorythm.morning import MorningAlgorythm

    args = message.get_args().split(' ')

    # Checkpoints for arg
    if len(args) != 1: return
    try:
        is_morning = int(args[0])
    except:
        await format_ex_msg(message); return
    if not is_morning in [0, 1]:
        await format_ex_msg(message); return

    # Set isMorning attribute and feedback to user
    MorningAlgorythm.set_is_morning(bool(is_morning))
    await set_is_morning(message, is_morning)








def register_morning(dp: Dispatcher):
    dp.register_message_handler(morning, Command('morning'), IsAdmin(), IsPrivate())