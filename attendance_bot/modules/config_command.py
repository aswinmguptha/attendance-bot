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
from attendance_bot.sql.users_sql import (
    get_chat_by_userid,
    add_user
)


@run_async
def config_command_fn(update: Update, context):
    keyboard = []
    keyboard.append([InlineKeyboardButton(
        text="Language",
        callback_data="config_lang"
    )])
    keyboard.append([InlineKeyboardButton(
        text="Timezone",
        callback_data="config_tz"
    )])
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_details = get_chat_by_userid(update.effective_chat.id)
    message_text = "Please select the appropriate buttons:"
    if user_details:
        message_text += f"<b>Language</b>: {user_details.language_code}\n"
    # message_text += f"<b>Timezone</b>: {}\n"
    update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup
    )


dispatcher.add_handler(
    CommandHandler(
        "config",
        config_command_fn
    )
)
