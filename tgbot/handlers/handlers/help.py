from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandHelp

from tgbot.handlers.filters import IsPrivate


async def help(message: types.Message):
    await message.answer('''Що цій бот вміє:
/schedule - Розклад пар А та Б неділь
/schedules - Розклади часу пар, очних та консультацій
/offline - Розклад пар очних заннять
/consults - Розклад пар консультацій''')


def register_help(dp: Dispatcher):
    dp.register_message_handler(help, CommandHelp(), IsPrivate())