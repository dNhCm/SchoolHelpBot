from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandHelp

from tgbot.handlers.filters import IsPrivate


async def help(message: types.Message):
    await message.answer('''
What can I do?:
/subjects_schedules - Sends photo with working schedule
/time_schedule - Sends time schedule


Admin set:
/morning <bool(0, 1)> - Turns on/off the morning additional algorythm that sends every morning before of lessons good morning message
/stop - Pauses algorithms for sending subjects and morning at all
/resume - Resumes work of algorythm for sending subjects and morning
/skip <int(count of loop to skip)> - Skips N number of algorithm cycles
/set <str(time in format "H:mm")> <str(subject from subject list)> - Changes subject from a schedule just for a once working day
/subject_list - Returns subject list
''')


def register_help(dp: Dispatcher):
    dp.register_message_handler(help, CommandHelp(), IsPrivate())