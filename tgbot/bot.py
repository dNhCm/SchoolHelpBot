import asyncio
from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis import Redis

from misc.logger import logger
from tgbot.data.config import get_config


def build() -> [Bot, Dispatcher]:
    config = get_config()

    bot = Bot(
        token=config.tgbot.token
    )

    if config.tgbot.use_redis:
        redis = Redis(
            host=config.redis.host,
            port=config.redis.port,
            password=config.redis.password
        )
        storage = RedisStorage(redis)
    else:
        storage = MemoryStorage()

    dp = Dispatcher(
        storage=storage
    )

    from tgbot.scripts import register_scripts
    register_scripts(bot, dp)
    from tgbot.utils.scheduler import register_scheduler
    register_scheduler(bot)
    from tgbot.routers import register_routers
    register_routers(dp)

    return [bot, dp]


async def start(bot: Bot, dp: Dispatcher):
    from tgbot.utils.menu.commands import register_my_commands

    from tgbot.models import connect_models
    await connect_models()

    try:
        await register_my_commands(bot)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


async def main():
    bot, dp = build()
    await start(bot, dp)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, CancelledError):
        logger.warn('Bot was stopped')
