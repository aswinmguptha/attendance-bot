#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import pytz
from datetime import datetime
from io import StringIO, BytesIO
from telegram import Update
from telegram.ext import CommandHandler, Filters

from attendance_bot import dispatcher, i18n

from attendance_bot.sql.locks_sql import check_lock, toggle_lock
from attendance_bot.sql.attendance_sheet_sql import (
    get_attendance_results,
    clear_attendance_sheet,
)
from attendance_bot.helpers.wrappers import into_local_time, localize


@into_local_time
@localize
def end_attendance_fn(update: Update, context, tz=pytz.UTC.zone):
    tz = pytz.timezone(tz)
    original_member = context.bot.get_chat_member(
        update.effective_chat.id, update.effective_user.id
    )
    if original_member.status in ("creator", "administrator"):
        is_locked = check_lock(update.effective_chat.id)
        if not is_locked:
            update.message.reply_text(i18n.t("please_start_attendance"))
            update.message.delete()
            return
        else:
            results = get_attendance_results(update.effective_chat.id)
            try:
                context.bot.edit_message_text(
                text=i18n.t("attendance_over", total=len(results)),
                chat_id=is_locked.chat_id,
                message_id=is_locked.message_id,
                )
            except Exception as e:
                pass
            date_and_time = datetime.now(tz).strftime("%F-%A-%r")
            filename = f"{update.effective_chat.title}-Attendance-{date_and_time}.csv"
            caption = f'Attendees: {len(results)}\nDate: {datetime.now(tz).strftime("%F")}\nTime: {datetime.now(tz).strftime("%I:%M %p")} {tz.zone}'

            with StringIO() as f:
                _writer = csv.writer(f)
                _writer.writerow(
                    [
                        i18n.t("serial_number"),
                        i18n.t("user_id"),
                        i18n.t("name"),
                        f"{i18n.t('time')} ({tz.zone})",
                    ]
                )
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
                            update.effective_chat.id, i18n.t("posting_result_in_group")
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
        update.message.reply_text(i18n.t("forbidden"))
    update.message.delete()


dispatcher.add_handler(
    CommandHandler("end_attendance", end_attendance_fn, Filters.group)
)
