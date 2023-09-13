
from datetime import timedelta


def delta_to_seconds(delta: timedelta) -> int:
    return delta.days * 86400 + delta.seconds
