
def next_week(week: str, subjects_schedules: dict[str: list[str]]) -> str:
    weeks = list(subjects_schedules)
    index = weeks.index(week) + 1
    try: week = weeks[index]
    except: week = weeks[0]

    return week