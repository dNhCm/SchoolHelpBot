
from aiogram import Dispatcher

dp: Dispatcher
def register(dispatcher: Dispatcher):
    global dp
    dp = dispatcher