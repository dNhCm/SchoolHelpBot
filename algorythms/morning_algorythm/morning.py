import asyncio
import json
from datetime import timedelta

from arrow import Arrow

from data.config import config

from algorythms.misc.delta_to_seconds import delta_to_seconds
from algorythms.misc.get_now import get_now
from misc.get_project_path import get_project_path


class MorningAlgorythm:

    isMorning: bool = True  # Attribute which answers whether the whole algorithm will work

    @classmethod
    def set_is_morning(cls, is_morning: bool):
        cls.isMorning = is_morning

    @classmethod
    async def morning(cls, week: str, current_schedule: list[dict['time': Arrow, 'subject': str]]) -> bool:
        from tgbot.scripts.morning import morning

        # Getting time_schedule
        project_path = get_project_path()
        data_path = project_path + '\\data'
        time_schedule = json.load(open(data_path + "\\time_schedule\\schedule.json"))

        # Getting times when need to send good morning
        subject_advance_time = int(config['SCHEDULE']['subject_advance_time'])
        times: list[Arrow] = [current_schedule[0], current_schedule[-1]]
        for i, time in enumerate(times): times[i] = time['time'].shift(minutes=-subject_advance_time-5)

        # Sending algorythm
        for send_time in times:
            # Getting how much time to wait
            delta = send_time - get_now()
            if delta.days < 0:
                if (send_time.shift(minutes=subject_advance_time) - get_now()).days < 0: return False
                else: delta = timedelta()

            # Waiting and sending
            await asyncio.sleep(delta_to_seconds(delta))

            if not await morning(week, get_now().weekday()): return False

        return True


async def main(week: str, current_schedule: list[dict['time': Arrow, 'subject': str]]):
    if MorningAlgorythm.isMorning:
        await MorningAlgorythm.morning(week, current_schedule)
