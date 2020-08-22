#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
from datetime import datetime
from io import StringIO, BytesIO
from telegram import Update
from telegram.ext import CommandHandler, Filters

from attendance_bot import dispatcher

from attendance_bot.sql.locks_sql import check_lock, toggle_lock
from attendance_bot.sql.attendance_sheet_sql import (
    get_attendance_results,
    clear_attendance_sheet,
)


def end_attendance_fn(update: Update, context):
    original_member = context.bot.get_chat_member(
        update.effective_chat.id, update.effective_user.id
    )
    if original_member.status in ("creator", "administrator"):
        is_locked = check_lock(update.effective_chat.id)
        if not is_locked:
            update.message.reply_text("Please start the attendance first")
            update.message.delete()
            return
        else:
            """if "list" not in context.chat_data:
                context.bot.edit_message_text(
                    text="Attendance is over. 0 people marked attendance.",
                    chat_id=context.chat_data["message"].chat_id,
                    message_id=context.chat_data["message"].message_id
                )
            else:"""
            results = get_attendance_results(update.effective_chat.id)
            context.bot.edit_message_text(
                text=f"Attendance is over. {len(results)} people marked attendance.",
                chat_id=is_locked.chat_id,
                message_id=is_locked.message_id,
            )

            date_and_time = datetime.now().strftime("%F-%A-%r")
            filename = f"{update.effective_chat.title}-Attendance-{date_and_time}.csv"
            caption = f'Attendees: {len(results)}\nDate: {datetime.now().strftime("%F")}\nTime: {datetime.now().strftime("%r")}'

            with StringIO() as f:
                _writer = csv.writer(f)
                _writer.writerow(["Serial number", "user id", "Name", "Time"])
                for index, result in enumerate(results, start=1):
                    _writer.writerow(
                        [index, result.user_id, result.user_name, result.time]
                    )
                f.seek(0)
                f = BytesIO(f.read().encode("utf8"))
                if len(results) > 0:
                    try:
                        context.bot.send_document(
                            update.effective_user.id,
                            f,
                            filename=filename,
                            caption=caption,
                        )
                    except Exception as e:
                        context.bot.send_message(update.effective_chat.id, str(e))
                        context.bot.send_message(
                            update.effective_chat.id, "Posting result in the group..."
                        )
                        f.seek(0)
                        context.bot.send_document(
                            update.effective_chat.id,
                            f,
                            filename=filename,
                            caption=caption,
                        )
            toggle_lock(update.effective_chat.id)
            clear_attendance_sheet(update.effective_chat.id)
    else:
        update.message.reply_text("Only admins can execute this command")
    update.message.delete()


dispatcher.add_handler(
    CommandHandler("end_attendance", end_attendance_fn, Filters.group)
)
