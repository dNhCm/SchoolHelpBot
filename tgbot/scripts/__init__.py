import asyncio
from aiogram import Dispatcher


from .subjects import WorkOn


async def call_scripts(dp: Dispatcher):
    await WorkOn(dp).main()