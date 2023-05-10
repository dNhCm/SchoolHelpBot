from aiogram import Dispatcher

from .start import register_start
from .help import register_help
from .consultations import register_consultations
from .schedule import register_schedule
from .schedules import register_schedules
from .offline import register_offline
from .about import register_about
from .test import register_test


def register(dp: Dispatcher):
    register_start(dp)
    register_consultations(dp)
    register_help(dp)
    register_schedule(dp)
    register_schedules(dp)
    register_offline(dp)
    register_about(dp)
    register_test(dp)