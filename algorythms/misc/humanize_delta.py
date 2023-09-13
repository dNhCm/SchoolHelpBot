
from datetime import timedelta

from algorythms.misc.delta_to_seconds import delta_to_seconds
from data.config import config


def humanize_delta(delta: timedelta) -> str:
    # Converting seconds to days, hours and minutes
    seconds = delta_to_seconds(delta)
    days = seconds // 86400
    hours = (seconds - days * 86400) // 3600
    minutes = (seconds - days * 86400 - hours * 3600) // 60

    # Getting localization for humanization
    localizations = config['LOCALIZATION']

    granularity: list[str] = [] # Humanized attributes

    # Humanize days number if it's not 0
    if days != 0:
        if days == 1:
            days = f"{days} {localizations['one_day']}"
        elif days <= 4:
            days = f"{days} {localizations['few_days']}"
        else:
            days = f"{days} {localizations['many_days']}"
        granularity += [days]

    # Humanize hours number if it's not 0
    if hours != 0:
        if hours == 1:
            hours = f"{hours} {localizations['one_hour']}"
        elif hours <= 4:
            hours = f"{hours} {localizations['few_hours']}"
        else:
            hours = f"{hours} {localizations['many_hours']}"
        granularity += [hours]

    # Humanize minutes number
    if minutes == 1:
        minutes = f"{minutes} {localizations['one_minute']}"
    elif 0 < minutes <= 4:
        minutes = f"{minutes} {localizations['few_minutes']}"
    else:
        minutes = f"{minutes} {localizations['many_minutes']}"
    granularity += [minutes]

    # Postprocessing our data in a bunch
    localized_text = localizations['will_be_in'] + ': '
    # Checking that in seconds its now
    if seconds < 0 or (len(granularity) == 1 and (delta.seconds - (delta.seconds // 3600) * 3600) // 60 == 0):
        return localized_text + localizations['now']
    # If this is not now, but time is lower than 60 minutes (so only minutes will be writen)
    elif len(granularity) == 1:
        return localized_text + granularity[0] + f" (±1 {localizations['one_minute']})"
    # And if we have also or additionally hours or days
    return localized_text + ', '.join(granularity[:-1]) + " та " + granularity[-1] + f" (±1 {localizations['one_minute']})"
