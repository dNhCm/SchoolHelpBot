
import asyncio

from aiogram import Bot, Dispatcher

from bot import building as tgbot_building, starting as tgbot_starting, logger
from algorythms.subjects_algorythm.subjects import main as algorythm_main


async def tgbot(dp: Dispatcher, bot: Bot):
    try:
        await tgbot_starting(dp, bot)
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')


async def algorythm():
    await algorythm_main()


# Main
async def main():
    dp, bot = tgbot_building()

    await asyncio.gather(
        tgbot(dp, bot),
        algorythm(),
    )

if __name__ == '__main__':
    asyncio.run(main())