import time
from datetime import timedelta


def uptime(start_time):
    delta = timedelta(seconds=time.time() - start_time)
    total_minutes, seconds = divmod(delta.seconds, 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{delta.days}д. {hours}ч. {minutes}м. {seconds}c."
