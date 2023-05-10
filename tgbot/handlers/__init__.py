from aiogram import Dispatcher

from .middlewares import register as register_middlewares
from .filters import register as register_filters
from .handlers import register as register_handlers

def register(dp: Dispatcher):
    register_middlewares(dp)
    register_filters(dp)
    register_handlers(dp)