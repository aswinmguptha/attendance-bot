#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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
def config_command_fn(update: Update, context):
    keyboard = []
    keyboard.append([InlineKeyboardButton(
        text="Change Language",
        callback_data="config_lang"
    )])
    keyboard.append([InlineKeyboardButton(
        text="Change Timezone",
        callback_data="config_tz"
    )])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text="buttons",
        reply_markup=reply_markup
    )


dispatcher.add_handler(
    CommandHandler(
        "config",
        config_command_fn
    )
)
