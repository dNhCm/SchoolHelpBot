
import asyncio

from aiogram import Bot, Dispatcher

from bot import build as tgbot_build, start as tgbot_start, logger
from algorythms.subjects_algorythm.subjects import main as algorythm_main


async def tgbot(dp: Dispatcher, bot: Bot):
    try:
        await tgbot_start(dp, bot)
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot was stopped!')


async def algorythm():
    await algorythm_main()


# Main
async def main():
    dp, bot = tgbot_build()

    await asyncio.gather(
        tgbot(dp, bot),
        algorythm(),
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Script was stopped!')
