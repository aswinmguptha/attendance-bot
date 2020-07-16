#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler

from attendance_bot import dispatcher

from attendance_bot.custom.filters import Filter


def start_attendance_fn(update: Update, context):
    original_member = context.bot.get_chat_member(
        update.effective_chat.id, update.effective_user.id
    )
    if original_member.status in ("creator", "administrator"):
        if "flag" in context.chat_data:
            update.message.reply_text("Please close the current attendance first")
            update.message.delete()
            return
        else:
            context.chat_data["flag"] = True
            context.chat_data["list"] = []
            keyboard = [[InlineKeyboardButton("Present", callback_data="present")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.chat_data["message"] = update.message.reply_text(
                "Please mark your attendance", reply_markup=reply_markup
            )
            update.message.delete()
    else:
        update.message.reply_text("Only admins can execute this command")
        update.message.delete()


dispatcher.add_handler(
    CommandHandler("start_attendance", start_attendance_fn, Filter.group)
)
