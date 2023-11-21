from aiogram import Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.enums import ParseMode

from tgbot.filters.is_private import IsPrivate


async def help_command(message: types.Message):
    text = '''What can I do?:
/subjects\_schedules - Sends photo with working schedule
/time\_schedule - Sends time schedule


Admin set:
/morning <bool(0, 1)> - Turns on/off the morning additional algorythm that sends every morning before of lessons good morning message
/stop - Pauses algorithms for sending subjects and morning at all
/resume - Resumes work of algorythm for sending subjects and morning
/skip <int(count of loop to skip)> - Skips N number of algorithm cycles
/change <str(time in format "H:mm")> <str(subject from subject list)> - Changes subject from a schedule just for a once working day
/subject\_list - Returns subject list'''
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


def register(router: Router):
    router.message.register(help_command, Command('help'), IsPrivate())
