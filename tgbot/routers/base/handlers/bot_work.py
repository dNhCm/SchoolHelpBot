
from aiogram import Router, Bot

from misc.logger import logger
from tgbot.data.config import get_config


async def startup(bot: Bot):
    admins = get_config().tgbot.admins
    for admin in admins:
        try:
            await bot.send_message(
                chat_id=admin,
                text="Bot was started!"
            )
        except Exception as ex:
            logger.warning(f"!!! {admin} id admin doesn't start chat with me !!! [{ex}]")



async def shutdown(bot: Bot):
    admins = get_config().tgbot.admins
    for admin in admins:
        try:
            await bot.send_message(
                chat_id=admin,
                text="Bot was stopped!"
            )
        except Exception as ex:
            logger.warning(f"!!! {admin} id admin doesn't start chat with me !!! [{ex}]")


def register(router: Router):
    router.startup.register(startup)
    router.shutdown.register(shutdown)
