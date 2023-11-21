import importlib
import os

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from misc.root import get_root, get_abspath
from tgbot.data.config import get_config

scheduler: AsyncIOScheduler


def register_scheduler(bot: Bot):
    global scheduler
    scheduler = AsyncIOScheduler(timezone=get_config().misc.tz)

    path = get_abspath(__file__)
    tasks = list(map(lambda x: x[:-3], os.listdir('/'.join(path))))
    tasks.remove('__init__')
    tasks.remove('__pycach')

    package = ".".join(path[len(get_root().split('/')):])
    for module in tasks:
        import_register = importlib.import_module(f'.{module}', package=package).register
        import_register(scheduler, bot)

    scheduler.start()
