
from aiogram import Dispatcher


from .is_private import IsPrivate


def register(dp: Dispatcher):
    dp.bind_filter(IsPrivate)