from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsAdmin(BoundFilter):
    async def check(self, obj: types.Message, *args) -> bool:
        return obj.from_user.id in obj.bot.data['config'].tgbot.admins