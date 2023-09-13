
import arrow
from arrow import Arrow

from data.config import config


def get_now() -> Arrow:
    return arrow.utcnow().shift(hours=int(config["SCHEDULE"]['time_zone']))
