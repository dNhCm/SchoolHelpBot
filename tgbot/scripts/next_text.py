import asyncio
from typing import Union, Optional

from misc.root import get_root
from . import bot
from ..data.config import get_config


async def next_text(next_subject: Union[str, list], localized_time: str) -> list[Optional[int], str | bool]:
    if type(next_subject) is str:
        subjects = [next_subject]
    else:
        subjects = next_subject

    subject_list: list[str] = []
    for subject in subjects:
        with open(f'{get_root()}/data/subjects/{subject}.txt', encoding='UTF-8') as f:
            subject_list += [''.join(f.readlines()).split('\n')[-1]]
    for i, subject in enumerate(subject_list.copy()):
        if subject == '':
            subject_list.pop(i)
    if len(subject_list) == 0:
        return [None, False]

    text: str = ''
    for subject in subject_list:
        text = text + subject + ' '
    text = text + f'\n{localized_time}'

    id: int
    try:
        response = await bot.send_message(chat_id=get_config().tgbot.group_id, text=text)
    except:
        return [None, False]
    id = response.message_id

    return [id, text]


async def change_next_text_time(text: str, id: int, localized_time: str) -> bool:
    text = text.split('\n')[0] + f'\n{localized_time}'

    try:
        await bot.edit_message_text(text=text, chat_id=get_config().tgbot.group_id, message_id=id)
        return True
    except:
        return False
