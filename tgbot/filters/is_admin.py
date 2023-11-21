from aiogram import types
from aiogram.filters import BaseFilter

from tgbot.data.config import get_config


class IsAdmin(BaseFilter):
    async def __call__(self, obj: types.Message, *args, **kwargs) -> bool:
        return obj.from_user.id in get_config().tgbot.admins
