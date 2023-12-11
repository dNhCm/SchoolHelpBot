
_sm_current = "time_schedule"


def sm_current(new_current: str = None) -> str:
    global _sm_current
    if new_current:
        _sm_current = new_current
    return _sm_current
