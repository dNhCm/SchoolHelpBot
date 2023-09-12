from algorythms.misc.get_next_week import next_week
from algorythms.misc.get_now import get_now


def week(subjects_schedules: dict[list[str]], week: str, days_step: int) -> str:
    if not week is None:
        weekday = get_now().weekday()
        days_step -= 7 - weekday
        if days_step < 0: return week
        weeks_count = days_step // 7
        for time in range(weeks_count+1):
            week = next_week(week, subjects_schedules)
    else:
        print('\n')
        while True:
            i = 1
            for schedule_name in subjects_schedules:
                print(f'{schedule_name} - {i}')
                i += 1

            try:
                answer = int(input("\n Введите какая неделя сейчас: "))
                if not (answer >= 1 and answer <= len(subjects_schedules)): raise Exception
                week = list(subjects_schedules)[answer-1]
                break
            except:
                continue

    return week