import asyncio
import json
from asyncio import Task
from datetime import timedelta

from arrow import Arrow

from algorythms.misc.delta_to_seconds import delta_to_seconds
from algorythms.misc.get_now import get_now
from algorythms.misc.humanize_delta import humanize_delta
from bot import logger
from data.config import config
from algorythms.misc.what_week import week as what_week
from algorythms.misc.str_time_to_arrow import str_to_arrow
from algorythms.morning_algorythm.morning import main as morning_main
from misc.root import get_root


class SubjectAlgorythm:
    week: str = None  # Current work week
    schedule: list[dict[str: Arrow, str: str | list[str]]] = []  # List of lessons where time and subject as well for current weekday
    next_schedule: list[dict[str: Arrow, str: Arrow, str: str]] = []  # List of lessons where send time, subject time and subject for sending a message prematurely saying when this subject will be, for current weekday
    subject_tasks: list[Task]
    next_subject_tasks: list[Task]

    subjects_schedules: dict[str: list[str]]
    time_schedule: list[str]

    isStopped: bool = False
    change_info: list[dict[str: str, str: str]]  # Here incomes lesson which require urgent removal from next_subject_task, this does not concern subjects_task, because if lesson message has already been sent, then it's impossible to change the lesson itself during the lesson (logic)

    @classmethod
    def preparing(cls, days_step: int = 0) -> None:
        """
        The algorithm with which each work cycle begins
        Here updates (clears) change_info, subject_tasks, next_subject_tasks datas
        Here getting new schedule for current weekday, and if today is no lessons, then day will be skipped (for this preparing has day_step parameter)


        :param: cls.schedule : [[time: Arrow, subject: str]]; Example: Arrow, "art"
        :param: cls.next_schedule : [[Arrow => subject: str]]; Example: Arrow, "math"
        :return:
        """

        # Getting subjects_schedules and time_schedule
        project_path = get_root()
        data_path = project_path+'/data'
        cls.subjects_schedules = json.load(open(data_path+"/subjects_schedules/schedules.json"))
        cls.time_schedule = json.load(open(data_path+"/time_schedule/schedule.json"))

        # Clearing
        cls.schedule: list[dict[str: Arrow, str: str]] = []  # [{'time': Arrow, 'subject': str}]
        cls.next_schedule: list[dict[str: Arrow, str: Arrow, str: str]] = []  # [{'send_time': Arrow, 'next_subject_time': Arrow, 'subject': str}]

        # Get week and weekday
        cls.week = what_week(cls.subjects_schedules, cls.week, days_step)
        current_weekday = get_now().weekday() + days_step
        current_weekday = current_weekday - 7 * (current_weekday // 7)

        # Preparing cls.schedule
        for time, subject in zip(cls.time_schedule, cls.subjects_schedules[cls.week][current_weekday]):
            arrow_time = str_to_arrow(time)
            cls.schedule += [{'time': arrow_time.shift(days=days_step), 'subject': subject}]

        for lesson in cls.schedule.copy():
            if lesson["subject"] == "none":
                cls.schedule.remove(lesson)

        if len(cls.schedule) == 0:
            cls.preparing(days_step+1)
            return

        # Getting weeks in contracting like we have ["A", "B", "C"] list of weeks, and now "B" week, then current_weeks will be ["B", "C", "A", "B"]
        weeks = list(cls.subjects_schedules)
        current_weeks: list = []
        # if today is Sunday, then we will take not "B", but next week that "C" in our situation
        if current_weekday == 6:
            try:
                current_weeks += [weeks[weeks.index(cls.week) + 1]]
            except IndexError:
                current_weeks += weeks[0]
        else:
            current_weeks += [cls.week]
        # We fill our contracted list, and if in the end is not our week, then assign our week to the end
        for time in range(len(weeks) - 1):
            index = weeks.index(current_weeks[-1]) + 1
            try:
                current_weeks += [weeks[index]]
            except IndexError:
                index = 0
                current_weeks += [weeks[index]]
        else:
            if current_weeks[-1] != cls.week:
                current_weeks += [cls.week]

        """Getting weekdays for every week in contracting, in type of [[2 ... 6 - For example from Wednesday, so to Sunday] - for B, [0 ... 6] - for C, [0 ... 6] - for A, [0, 1 - dats from B week that remaining] - for B again]"""
        weekdays: list[list] = [[] for _ in range(len(current_weeks))]

        for weekday in range(current_weekday + 1, 7):
            weekdays[0] += [weekday]

        for weekday in range(0, current_weekday + 1):
            weekdays[-1] += [weekday]

        for current_weekdays in weekdays:
            if len(current_weekdays) == 0:
                for weekday in range(7):
                    current_weekdays += [weekday]

        isBreak = False
        for week_i, current_weekdays in enumerate(weekdays):
            for weekday in current_weekdays:
                for i, subject in enumerate(cls.subjects_schedules[current_weeks[week_i]][weekday]):
                    if subject != "none":
                        days_sum = 0
                        for week in range(len(current_weeks[:week_i])):
                            for _ in weekdays[week]:
                                days_sum += 1
                        else:
                            days_sum += current_weekdays.index(weekday) + 1
                        cls.schedule += [
                            {"time": str_to_arrow(cls.time_schedule[i]).shift(days=days_sum+days_step), "subject": subject}]
                        isBreak = True
                    if isBreak:
                        break
                if isBreak:
                    break
            if isBreak:
                break
        else:
            logger.warn("No subjects in subject schedule")

        # Preparing cls.next_schedule
        cls.next_schedule = []

        for lessoni in range(len(cls.schedule)-1, 0, -1):
            lesson = cls.schedule[lessoni]
            lesson_before = cls.schedule[lessoni-1]

            cls.next_schedule.insert(0, {"send_time": lesson_before['time'], "subject_time": lesson['time'], "subject": lesson['subject']})

        # Preparing of tasks
        cls.subject_tasks = []
        cls.next_subject_tasks = []
        cls.change_info = []

        # Info about schedules for debugging
        logger.info(f"cls.schedule: {cls.schedule}")
        logger.info(f"cls.next_schedule: {cls.next_schedule}")

    @classmethod
    async def subject_manager(cls) -> None:  # Manager of sending subject messages
        for lesson in cls.schedule:
            cls.subject_tasks += [asyncio.create_task(cls.subject(
                lesson['time'], lesson['subject']),
                name=f"subject : {lesson['time'].format('H:mm')} : {lesson['subject']}"
            )]

        # Awaiting every task in time
        i_intend = 0
        for lesson, task_i in zip(cls.schedule, range(len(cls.subject_tasks.copy()))):
            time = lesson['time']

            # Wait to await...
            now_time = get_now()
            subject_advance_time = int(config["SCHEDULE"]["subject_advance_time"])
            delta = time.shift(minutes=-subject_advance_time) - now_time

            if delta.days < 0:
                if (time - now_time).days < 0:
                    task = cls.subject_tasks[task_i - i_intend]
                    cls.subject_tasks.remove(task)
                    i_intend += 1
                    continue
                else:
                    delta = timedelta()

            await asyncio.sleep(delta_to_seconds(delta))

            # Getting and removing task from list, because it will be awaited or was cancelled
            task = cls.subject_tasks[task_i - i_intend]
            cls.subject_tasks.remove(task)
            i_intend += 1
            # Awaiting if task isn't cancelled...
            if not task.cancelled():
                await task

    @staticmethod
    async def subject(time: Arrow, subject: str) -> bool:  # Text subject messages, and after of some time delete them
        from tgbot.scripts.text import text
        from tgbot.scripts.delete_messages import delete_messages

        # Waiting to start...
        now_time = get_now()
        subject_advance_time = int(config["SCHEDULE"]["subject_advance_time"])
        delta = time.shift(minutes=-subject_advance_time) - now_time

        if delta.days < 0:
            if (time - now_time).days < 0:
                return False
            else:
                delta = timedelta()

        await asyncio.sleep(delta_to_seconds(delta))

        # Additional breakpoint if algorythm is stopped
        if SubjectAlgorythm.isStopped:
            return False

        # Text
        ids: list = await text(subject)

        # Breakpoint if it can't to send
        if len(ids) == 0:
            return False

        # Waiting to delete...
        now_time = get_now()
        deleting_subject_delay = int(config["SCHEDULE"]["deleting_subject_delay"])
        delta = time.shift(minutes=deleting_subject_delay) - now_time

        if delta.days < 0:
            delta = timedelta()

        await asyncio.sleep(delta_to_seconds(delta))

        # Delete itself...
        await delete_messages(ids)

        return True

    @classmethod
    async def next_subject_manager(cls) -> None:  # Manager which is responsible for warning the subsequent lesson
        for lesson in cls.next_schedule:
            cls.next_subject_tasks += [asyncio.create_task(
                cls.next_subject(lesson['send_time'], lesson['subject_time'], lesson["subject"]),
                name=f"next_subject : {lesson['send_time'].format('H:mm')} : {lesson['subject_time'].format('H:mm')} : {lesson['subject']}"
            )]

        # Awaiting every task in time
        i_intend = 0
        for lesson, task_i in zip(cls.next_schedule, range(len(cls.next_subject_tasks.copy()))):
            send_time = lesson['send_time']
            subject_time = lesson['subject_time']

            # Waiting to await...
            now_time = get_now()
            delta = send_time - now_time

            if delta.days < 0:
                if (subject_time - now_time).days < 0:
                    task = cls.next_subject_tasks[task_i - i_intend]
                    cls.next_subject_tasks.remove(task)
                    i_intend += 1
                    continue
                else:
                    delta = timedelta()

            await asyncio.sleep(delta_to_seconds(delta))

            # Getting and removing task from list, because it will be awaited or was cancelled
            task = cls.next_subject_tasks[task_i - i_intend]
            cls.next_subject_tasks.remove(task)
            i_intend += 1
            # Awaiting if task isn't cancelled...
            if not task.cancelled():
                await task

    @staticmethod
    async def next_subject(send_time: Arrow, subject_time: Arrow, subject: str) -> bool:  # Texts, updates every minute to know how much time is left to wait, and after waits when lesson will be finished and delete itself
        from tgbot.scripts.next_text import next_text, change_next_text_time
        from tgbot.scripts.delete_messages import delete_messages

        # Waiting to start...
        now_time = get_now()
        delta = send_time - now_time

        if delta.days < 0:
            if (subject_time - now_time).days < 0:
                return False
            else:
                delta = timedelta()

        await asyncio.sleep(delta_to_seconds(delta))

        # Additional breakpoint if algorythm is stopped
        if SubjectAlgorythm.isStopped:
            return False

        # Get humanized time
        delta = subject_time - get_now()
        localized_time = humanize_delta(delta)

        # Text it
        msg_id, text = await next_text(subject, localized_time)

        # Breakpoint if it can't to send
        if type(text) is bool:
            if not text:
                return False

        # Updating every minute to know how much time is left to wait
        while True:
            await asyncio.sleep(30)

            # Checkpoint if it is on the change_info list. if it is, then delete itself
            for change_task in SubjectAlgorythm.change_info:
                if change_task['time'] == subject_time.format('H:mm') and change_task['subject'] == subject:
                    SubjectAlgorythm.change_info.remove(change_task)
                    await delete_messages([msg_id])
                    return True

            # Update humanized time to new one
            delta = subject_time - get_now()
            localized_time = humanize_delta(delta)
            await change_next_text_time(text, msg_id, localized_time)

            # If lesson has already started then stop loop
            if delta.days < 0:
                break

        # Getting time to wait for finishing of lesson
        now_time = get_now()
        deleting_time = subject_time.shift(minutes=int(config['SCHEDULE']['deleting_subject_delay']))
        delta = deleting_time - now_time
        if delta.days < 0:
            delta = timedelta()

        # Waiting...
        await asyncio.sleep(delta_to_seconds(delta))

        # Deleting itself
        await delete_messages([msg_id])

        return True

    @classmethod
    def stop(cls) -> bool:
        if not cls.isStopped:
            cls.isStopped = True
            return True
        return False

    @classmethod
    def resume(cls) -> bool:
        if cls.isStopped:
            cls.isStopped = False
            return True
        return False

    @staticmethod
    async def skip(skips: int):
        arrow_time = get_now().shift(days=skips).replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
        seconds = delta_to_seconds(arrow_time - get_now())

        SubjectAlgorythm.stop()
        await asyncio.sleep(seconds)
        SubjectAlgorythm.resume()

    @classmethod
    def change(cls, time: str, subject: str | list[str]) -> bool | Task:  # Algorythm which urgently changes a subject at an appointed time from time schedule
        # Find task to change
        for i, task in enumerate(cls.subject_tasks):
            task_time = task.get_name().split(' : ')[1]
            if task_time == time:
                # Cancel task, and create a new one for the same time only with changed subject
                arrow_time: Arrow = cls.schedule[len(cls.schedule)-len(cls.subject_tasks)+i]['time']
                cls.subject_tasks[i].cancel()
                cls.subject_tasks[i] = task.get_loop().create_task(
                    cls.subject(time=arrow_time, subject=subject),
                    name=f"subject : {arrow_time.format('H:mm')} : {subject}"
                )

                # Getting next_task and next_subject too
                next_i = i-1
                next_task = cls.next_subject_tasks.copy()[next_i]
                next_subject = cls.next_schedule[len(cls.next_schedule)-len(cls.next_subject_tasks)+next_i]
                # If index of next_i is not -1, then cancel next_task and create new one for the same time, but with another subject. and if next_i is -1, it means that next_subject messages had already sent, so we add to change_info new order for current next_task, and create new one with different.
                if next_i != -1:
                    if next_task.get_name().split(' : ')[2] == time:
                        cls.next_subject_tasks[next_i].cancel()
                        cls.next_subject_tasks[next_i] = next_task.get_loop().create_task(
                            cls.next_subject(send_time=next_subject['send_time'], subject_time=next_subject['subject_time'], subject=subject),
                            name=f"next_subject : {next_subject['send_time']} : {next_subject['subject_time']} : {subject}"
                        )
                else:
                    cls.change_info += [{'time': time, 'subject': next_subject['subject']}]
                    task = next_task.get_loop().create_task(
                        cls.next_subject(send_time=next_subject['send_time'], subject_time=next_subject['subject_time'], subject=subject),
                        name=f"next_subject : {next_subject['send_time']} : {next_subject['subject_time']} : {subject}"
                    )
                    return task
                return True
        # if there is no task with this time, then return False
        return False

    @classmethod
    async def main(cls):
        while True:
            cls.preparing()

            await asyncio.gather(
                morning_main(cls.week, cls.schedule),
                cls.subject_manager(),
                cls.next_subject_manager(),
            )


async def main():
    await SubjectAlgorythm.main()
