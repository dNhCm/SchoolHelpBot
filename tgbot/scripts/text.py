
from tgbot.data.config import get_config

from . import bot


async def text(subject: list|str) -> list[int]:  # Warns about lessons, and returns the ids of the messages to delete in future
    if type(subject) is str:
        subjects = [subject]
    else: subjects = subject

    text_list = []
    for subject in subjects:
        with open(f'data/subjects/{subject}.txt', encoding='UTF-8') as f:
            text_list += ''.join(f.readlines()).split('\n')

    ids: list[int] = []
    for text in text_list:
        try:
            response = await bot.send_message(chat_id=get_config().tgbot.group_id, text=text)
        except:
            return []
        ids += [response['message_id']]

    return ids
