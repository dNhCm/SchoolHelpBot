
import arrow
import datetime
from data.config import config


def where_in_time(time_schedule: list[str]) -> int: # Algorythm that finds the index of the time of the lesson that begins
    now = arrow.utcnow()

    time_zone = int(config['SCHEDULE']['time_zone'])
    times: list[arrow.Arrow] = []
    for time in time_schedule:
        times += [arrow.utcnow().replace(hour=int(time.split(':')[0])).replace(minute=int(time.split(':')[1])).shift(hours=-time_zone)]

    deltas: list[datetime.timedelta] = []
    for i, time in enumerate(times):
        deltas += [(i, time - now)]

    intend = 0
    for delta in deltas.copy():
        if delta[1].days == -1:
            deltas.pop(delta[0]-intend)
            intend += 1

    if len(deltas) == 0:
        itime = 0
    else:
        itime = deltas[0][0]

    return itime