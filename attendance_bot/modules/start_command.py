#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import (
    ParseMode,
    Update
)
from telegram.ext import (
    CommandHandler,
    Filters,
    run_async
)

from attendance_bot import (
    dispatcher
)


@run_async
def start_fn(update: Update, context):
    update.message.reply_text(
        r'''Hi,
Welcome to Group Attendance Bot\. Add me to your group to mark attendance\. Send /help to know more\.''',
        parse_mode=ParseMode.MARKDOWN_V2
    )


dispatcher.add_handler(
    CommandHandler(
        "start",
        start_fn,
        Filters.private
    )
)
