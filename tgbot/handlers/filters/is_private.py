from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, obj: types.Message, *args) -> bool:
        return obj.chat.type in ['private']