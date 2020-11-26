#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, Filters

from attendance_bot import dispatcher, i18n

from attendance_bot.sql.locks_sql import check_lock, toggle_lock
from attendance_bot.helpers.wrappers import localize


@localize
def start_attendance_fn(update: Update, context):
    original_member = context.bot.get_chat_member(
        update.effective_chat.id, update.effective_user.id
    )
    if original_member.status in ("creator", "administrator"):
        if check_lock(update.effective_chat.id):
            update.message.reply_text(i18n.t("please_close_attendance"))
            update.message.delete()
            return
        else:
            keyboard = [
                [InlineKeyboardButton(i18n.t("present"), callback_data="present")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            attendance_msg = update.message.reply_text(
                i18n.t("please_mark_attendance"), reply_markup=reply_markup
            )
            toggle_lock(update.effective_chat.id, attendance_msg.message_id)
            update.message.delete()
    else:
        update.message.reply_text(i18n.t("forbidden"))
        update.message.delete()


dispatcher.add_handler(
    CommandHandler("start_attendance", start_attendance_fn, Filters.group)
)
