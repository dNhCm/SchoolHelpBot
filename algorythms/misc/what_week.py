from algorythms.misc.get_next_week import next_week
from algorythms.misc.get_now import get_now


def week(subjects_schedules: dict[list[str]], current_week: str, days_step: int) -> str:  # Algorythm to know which week is now by previous, or get new one by input
    if not current_week is None:  # If we already have a current week, then we just count next one
        weekday = get_now().weekday()
        days_step -= 7 - weekday
        if days_step < 0: return current_week
        weeks_count = days_step // 7
        for time in range(weeks_count+1):
            current_week = next_week(current_week, subjects_schedules)
    else:
        # Code to get new one current week
        print('\n')
        while True:
            i = 1
            for schedule_name in subjects_schedules:
                print(f'{schedule_name} - {i}')
                i += 1

            try:
                answer = int(input("\n Введите какая неделя сейчас: "))
                if not (1 <= answer <= len(subjects_schedules)): raise Exception
                current_week = list(subjects_schedules)[answer - 1]
                break
            except:
                continue

    return current_week
