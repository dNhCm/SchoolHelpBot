import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config

logger = logging.getLogger(__name__)


def building() -> list[Dispatcher, Bot]:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    bot = Bot(token=config.tgbot.bot_token, parse_mode='HTML')
    bot['config'] = config
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    from tgbot.handlers import register as register_all_handlers
    register_all_handlers(dp)
    from tgbot.scripts import register as register_scripts
    register_scripts(dp)

    return [dp, bot]


async def starting(dp: Dispatcher, bot: Bot) -> bool:
    # start
    try:
        await dp.start_polling()
        return True
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        return False


async def main():
    dp, bot = building()
    await starting(dp, bot)
