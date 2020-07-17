#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
from datetime import datetime
from io import StringIO, BytesIO
from telegram import Update
from telegram.ext import CommandHandler

from attendance_bot import dispatcher

from attendance_bot.custom.filters import Filter


def end_attendance_fn(update: Update, context):
    if "flag" not in context.chat_data:
        update.message.reply_text(
            "Please start the attendance first", reply_to_message_id=None
        )
        return
    else:
        """if "list" not in context.chat_data:
            context.bot.edit_message_text(
                text="Attendance is over. 0 people marked attendance.",
                chat_id=context.chat_data["message"].chat_id,
                message_id=context.chat_data["message"].message_id
            )
        else:"""
        context.bot.edit_message_text(
            text="Attendance is over. {} people marked attendance.".format(
                len(context.chat_data["list"])
            ),
            chat_id=context.chat_data["message"].chat_id,
            message_id=context.chat_data["message"].message_id,
        )

        date_and_time = datetime.now().strftime("%F-%A-%r")
        filename = f"{update.effective_chat.title}-Attendance-{date_and_time}.csv"
        caption = f'Attendees: {len(context.chat_data["list"])}\nDate: {datetime.now().strftime("%F")}\nTime: {datetime.now().strftime("%r")}'

        with StringIO() as f:
            _writer = csv.writer(f)
            _writer.writerow(["Serial number", "user id", "Name", "Time"])
            _writer.writerows(context.chat_data["list"])
            f.seek(0)
            f = BytesIO(f.read().encode("utf8"))
            if len(context.chat_data["list"]) > 0:
                try:
                    context.bot.send_document(
                        update.effective_user.id, f, filename=filename, caption=caption,
                    )
                except Exception as e:
                    context.bot.send_message(update.effective_chat.id, str(e))
                    context.bot.send_message(
                        update.effective_chat.id, "Posting result in the group..."
                    )
                    f.seek(0)
                    context.bot.send_document(
                        update.effective_chat.id, f, filename=filename, caption=caption,
                    )
        del context.chat_data["flag"]


dispatcher.add_handler(
    CommandHandler("end_attendance", end_attendance_fn, Filter.group & Filter.admin)
)
