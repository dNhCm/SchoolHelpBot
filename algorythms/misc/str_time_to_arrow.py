from arrow import Arrow

from algorythms.misc.get_now import get_now


def str_to_arrow(time: str, additional_time_info: Arrow = None) -> Arrow:  # Just converter
    arrow_time = get_now()
    if not additional_time_info is None:
        year = additional_time_info.__getattr__("year")
        month = additional_time_info.__getattr__("month")
        day = additional_time_info.__getattr__("day")
        arrow_time = arrow_time.replace(year=year).replace(day=day).replace(month=month)
    arrow_time = arrow_time.replace(hour=int(time.split(':')[0])).replace(minute=int(time.split(':')[1])).replace(second=0).replace(microsecond=0)

    return arrow_time