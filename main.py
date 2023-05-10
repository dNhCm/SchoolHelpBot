
import asyncio
from bot import main as tgbot_main, logger


def start_tgbot():
    try:
        asyncio.run(tgbot_main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')


# Main
def main():
    start_tgbot()


if __name__ == '__main__':
    main()
