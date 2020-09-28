#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, Filters, run_async

from attendance_bot import dispatcher
from attendance_bot.sql.users_sql import get_chat_by_userid, add_user


@run_async
def config_command_fn(update: Update, context):
    keyboard = []
    keyboard.append(
        [InlineKeyboardButton(text="Language", callback_data="config_lang")]
    )
    keyboard.append([InlineKeyboardButton(text="Timezone", callback_data="config_tz")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_details = get_chat_by_userid(update.effective_chat.id)
    if not user_details:
        chat_type = update.effective_chat.type
        if chat_type == "private":
            add_user(
                update.effective_user.id,
                update.effective_user.first_name,
                update.effective_user.last_name or "",
                chat_type,
            )
        else:
            add_user(
                update.effective_chat.id, update.effective_chat.title, "", chat_type
            )
        user_details = get_chat_by_userid(update.effective_chat.id)
    message_text = "Please select the appropriate buttons:"
    update.message.reply_text(text=message_text, reply_markup=reply_markup)


dispatcher.add_handler(CommandHandler("config", config_command_fn))
