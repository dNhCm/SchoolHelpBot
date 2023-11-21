from aiogram import types

from bot import logger
from tgbot.data.config import get_config


async def stopped_algorythm(message: types.Message):
    logger.info('subject_algorythm was stopped')
    admins = get_config().tgbot.admins
    for admin in admins:
        try:
            await message.bot.send_message(chat_id=admin, text=f'{message.from_user.id} ID user stopped work of subject sending and good morning algorithms')
        except:
            logger.warn(f'{admin} ID admin does not start chat with bot(')


async def resumed_algorythm(message: types.Message):
    logger.info('subject_algorythm was resumed')
    admins = get_config().tgbot.admins
    for admin in admins:
        try:
            await message.bot.send_message(chat_id=admin, text=f"{message.from_user.id} ID user restored the work of sending subject and good morning algorithms")
        except:
            logger.warn(f'{admin} ID admin does not start chat with bot(')


async def set_is_morning(message: types.Message, is_morning: int):
    logger.info(f'isMorning attribute value was changed to {bool(is_morning)}')
    for admin in get_config().tgbot.admins:
        try:
            await message.bot.send_message(chat_id=admin, text=f'{message.from_user.id} ID user changed morning algorythm lever to {bool(is_morning)} state.')
        except:
            logger.warn(f'{admin} ID admin does not start chat with bot(')


async def successful_change(message: types.Message, args: list[str]):
    logger.info(f'Subject was change to {args[1]} for {args[0]}')
    for admin in get_config().tgbot.admins:
        try:
            await message.bot.send_message(chat_id=admin, text=f'{message.from_user.id} ID user changed subject to {args[1]} for {args[0]}.')
        except:
            logger.warn(f'{admin} ID admin does not start chat with bot(')


async def set_skips(message: types.Message, skips:int):
    logger.info(f'Algorythm will skips {skips} days')
    for admin in get_config().tgbot.admins:
        try:
            await message.bot.send_message(chat_id=admin, text=f'{message.from_user.id} ID user set skips to {skips} days.')
        except:
            logger.warn(f'{admin} ID admin does not start chat with bot(')
