
from aiogram import types
from aiogram.filters import BaseFilter


class IsPrivate(BaseFilter):
    async def __call__(self, obj: types.Message, *args, **kwargs) -> bool:
        return obj.chat.type in ['private']
