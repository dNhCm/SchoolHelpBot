
import arrow

from bot import logger


def we_in_time(schedules: list[list[str]]) -> str:  # Algorythm that give to know which time from schedule is the next one
  now = arrow.utcnow()
  now_hour = now.__getattr__('hour')
  now_minute = now.__getattr__('minute')

  times = [time for schedule in schedules for time in schedule]
  hours = [int(time.split(':')[0]) for time in times]
  minutes = [int(time.split(':')[1]) for time in times]

  ihours = []
  isNowHour = False
  for i, hour in enumerate(hours):
    if not isNowHour:
      if now_hour < hour:
        ihours += [i]
        break

    if now_hour == hour:
      isNowHour = True
      ihours += [i]
      continue

  if len(ihours) == 1 and now_hour < hours[ihours[0]]:
    next_time = times[ihours[0]]
  else:
    minutes = [minute - 5 for minute in minutes[ihours[0]:ihours[-1] + 1]]
    iminute = []
    for i, minute in enumerate(minutes):
      if now_minute <= minute:
        iminute += [i]
        break

    if len(iminute) == 0:
      next_time = times[ihours[-1] + 1]
    else:
      next_time = times[ihours[0] + iminute[0]]

  logger.info(f'WorkOn(...).next_time: {next_time}')
  return next_time