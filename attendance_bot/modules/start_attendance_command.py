#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler

from attendance_bot import dispatcher

from attendance_bot.custom.filters import Filter


def start_attendance_fn(update: Update, context):
    if "flag" in context.chat_data:
        update.message.reply_text(
            "Please close the current attendance first", reply_to_message_id=None
        )
        return
    else:
        context.chat_data["flag"] = True
        context.chat_data["list"] = []
        context.chat_data["start_user"] = update.message.from_user
        keyboard = [[InlineKeyboardButton("Present", callback_data="present")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.chat_data["message"] = update.message.reply_text(
            "Please mark your attendance",
            reply_to_message_id=None,
            reply_markup=reply_markup,
        )


dispatcher.add_handler(
    CommandHandler("start_attendance", start_attendance_fn, Filter.group & Filter.admin)
)
