#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
from telegram import CallbackQuery, Update
from telegram.ext import CallbackQueryHandler, run_async

from attendance_bot import dispatcher

from attendance_bot.sql.attendance_sheet_sql import mark_attendance, check_attendance


@run_async
def mark_attendance_fn(update: Update, context):
    query = update.callback_query
    choice = query.data
    if choice == "present":
        if check_attendance(update.effective_chat.id, update.effective_user.id):
            context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="You have already marked your attendance",
                show_alert=True,
            )
        else:
            _first_name = update.effective_user.first_name
            _last_name = update.effective_user.last_name or ""
            _user_name = _first_name + " " + _last_name
            _time = datetime.now().strftime("%H:%M")
            mark_attendance(
                update.effective_chat.id, update.effective_user.id, _user_name, _time
            )
            context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="Your attendance has been marked",
                show_alert=True,
            )


dispatcher.add_handler(CallbackQueryHandler(mark_attendance_fn, pattern=r"present"))
