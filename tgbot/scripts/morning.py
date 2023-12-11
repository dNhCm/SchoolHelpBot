from random import choice

from data.config import config
from tgbot.data.config import get_config

from . import bot


async def morning(week: str, weekday: int) -> bool:
    localization = config['LOCALIZATION']
    localized_week = localization['week']
    weekday = config['LOCALIZATION']['weekdays'][1:-1].split('", "')[weekday]
    good_morning = choice(config['LOCALIZATION']['good_morning'][1:-1].split('", "'))

    text = good_morning + '\n' + localized_week + ' ' + week + '\n' + weekday + '!'
    print(text)

    try:
        await bot.send_message(chat_id=get_config().tgbot.group_id, text=text)
    except:
        return False

    return True
