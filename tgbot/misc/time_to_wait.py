
import arrow


def wait(next_time: str) -> int:  # Algorythm that count how much time the script will sleep to send a link to lesson after
    now = arrow.utcnow()

    hour = int(next_time.split(':')[0])
    minute = int(next_time.split(':')[1])
    if minute-5 < 0:
        minute += 55
        hour = int(next_time.split(':')[0]) - 1
    else: minute -= 5

    next_time = arrow.Arrow(
        year = now.__getattr__('year'),
        month = now.__getattr__('month'),
        day = now.__getattr__('day'),
        hour = hour,
        minute = minute
    )

    delta = next_time - now
    delta = delta.seconds

    return delta