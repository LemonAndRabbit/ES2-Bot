"""Compose the messages to be a valid range value for google sheet api"""

import datetime

def compose_onetoall(source, target, constants):
    """Compose the message for onetoall"""
    values = [[source, t, *constants] for t in target]
    return values

def id_reparthenese(id):
    return f'<@{id}>'

def compose_formatted_time(ts, tz):
    """Compose the epoch time"""
    dt = datetime.datetime.fromtimestamp(ts, tz=tz)
    # dt = dt.astimezone()

    return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')