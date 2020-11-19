#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, Filters, run_async

from attendance_bot import dispatcher, i18n
from attendance_bot.sql.users_sql import get_chat_by_userid, add_user
from attendance_bot.helpers.wrappers import localize
from attendance_bot.custom.filters import Filter


@run_async
@localize
def config_command_fn(update: Update, context):
    keyboard = []
    keyboard.append(
        [InlineKeyboardButton(text=i18n.t("language"), callback_data="config_lang")]
    )
    keyboard.append(
        [InlineKeyboardButton(text=i18n.t("timezone"), callback_data="config_tz")]
    )
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
    message_text = i18n.t("main_menu")
    update.message.reply_text(text=message_text, reply_markup=reply_markup, reply_to_message_id=None)


dispatcher.add_handler(
    CommandHandler("config", config_command_fn, filters=Filter.admin)
)
