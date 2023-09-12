from typing import Union

from . import dp


async def delete_messages(ids: Union[list[int], None]):
    bot = dp.bot
    if not type(ids) is None:
        for id in ids:
            await bot.delete_message(chat_id=bot.data['config'].tgbot.group_id, message_id=id)