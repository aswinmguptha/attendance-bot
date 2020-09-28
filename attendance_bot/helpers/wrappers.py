from attendance_bot import i18n

from attendance_bot.sql.timezone_sql import get_time_zone
from attendance_bot.sql.languages_sql import get_language


def into_local_time(func):
    def inner(*args, **kwargs):
        update = args[0]
        tz = get_time_zone(update.effective_chat.id)
        if tz:
            kwargs["tz"] = tz.time_zone

        return func(*args, **kwargs)

    return inner


def localize(func):
    def inner(*args, **kwargs):
        update = args[0]
        lang = get_language(update.effective_chat.id)
        if lang:
            i18n.set("locale", lang.language_code)
        return func(*args, **kwargs)

    return inner
