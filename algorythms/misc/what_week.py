from algorythms.misc.get_next_week import next_week
from algorythms.misc.get_now import get_now


def week(subjects_schedules: dict[list[str]], current_week: str, days_step: int) -> str:  # Algorythm to know which week is now by previous, or get new one by input
    if current_week is not None:  # If we already have a current week, then we just count next one
        weekday = get_now().weekday()
        days_step -= 7 - weekday
        if days_step < 0:
            return current_week
        weeks_count = days_step // 7
        for time in range(weeks_count+1):
            current_week = next_week(current_week, subjects_schedules)
    else:
        return list(subjects_schedules)[0]

    return current_week
