
from typing import Union

from . import dp


async def next_text(next_subject: Union[str, list], localized_time: str) -> list[int, str] | bool:
    if type(next_subject) is str:
        subjects = [next_subject]
    else: subjects = next_subject

    text: str
    for subject in subjects:
        with open(f'data/subjects/{subject}.txt', encoding='UTF-8') as f:
            text = ''.join(f.readlines()).split('\n')[-1]
    text = text + f'\n{localized_time}'

    bot = dp.bot
    id: int
    try: response = await bot.send_message(chat_id=bot.data['config'].tgbot.group_id, text=text)
    except: return False
    id = response['message_id']

    return [id, text]


async def change_next_text_time(text: str, id: int, localized_time: str) -> bool:
    bot = dp.bot

    text = text.split('\n')[0] + f'\n{localized_time}'

    try:
        await bot.edit_message_text(text=text, chat_id=bot.data['config'].tgbot.group_id, message_id=id)
        return True
    except: return False