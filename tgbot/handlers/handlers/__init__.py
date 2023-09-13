from aiogram import Dispatcher

from .start import register_start
from .help import register_help
from .time_schedule import register_time_schedule
from .subjects_schedules import register_subjects_schedules
from .about import register_about
from .test import register_test
from .subject_list import register_subject_list
from .stop import register_stop
from .resume import register_resume
from .morning import register_morning
from .change import register_change
from .skip import register_skip


def register(dp: Dispatcher):
    register_start(dp)
    register_help(dp)
    register_time_schedule(dp)
    register_subjects_schedules(dp)
    register_about(dp)
    register_test(dp)
    register_subject_list(dp)
    register_stop(dp)
    register_resume(dp)
    register_morning(dp)
    register_change(dp)
    register_skip(dp)