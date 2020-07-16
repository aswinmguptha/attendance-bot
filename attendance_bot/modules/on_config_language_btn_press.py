#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
from telegram import (
    CallbackQuery,
    Update
)
from telegram.ext import (
    CallbackQueryHandler,
    run_async
)

from attendance_bot import (
    dispatcher
)


@run_async
def mark_attendance_fn(update: Update, context):
    query = update.callback_query
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differently
    # (and we can only answer once),
    # so we don't always answer here.
    query.answer()
    



dispatcher.add_handler(
    CallbackQueryHandler(
        mark_attendance_fn,
        pattern=r"config_lang"
    )
)
