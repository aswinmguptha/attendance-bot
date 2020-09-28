from attendance_bot.sql.timezone_sql import get_time_zone


def into_local_time(func):
    def inner(*args, **kwargs):
        update = args[0]
        tz = get_time_zone(update.effective_chat.id)
        if tz:
            kwargs["tz"] = tz.time_zone

        return func(*args, **kwargs)

    return inner
