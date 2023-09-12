
def get_next_itime(itime: int, time_schedule: list[str]) -> int: # Tiny subjects_algorythm that count next index of the lesson
    if itime+1 >= 0 and itime+1 < len(time_schedule):
        return itime+1
    else:
        return 0