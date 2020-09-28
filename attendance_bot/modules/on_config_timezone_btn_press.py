#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
from telegram import CallbackQuery, Update
from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    Filters,
    run_async,
)
from timezonefinder import TimezoneFinder

from attendance_bot import dispatcher
from attendance_bot.helpers.get_reply_markup_for_time_zone import get_time_zone_ntb
from attendance_bot.sql.timezone_sql import get_time_zone, update_time_zone
from attendance_bot.sql.locks_sql import check_lock

INPUT_LOC = range(1)


@run_async
def change_tz_cfg_btn(update: Update, context):
    query = update.callback_query
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differently
    # (and we can only answer once),
    # so we don't always answer here.
    query.answer()

    user_id = query.message.chat.id
    current_selected_tz = "Asia/Kolkata"

    if check_lock(user_id):
        query.message.reply_text(
            "Can not change timezone while attendance is in progress"
        )
        return ConversationHandler.END

    current_tz = get_time_zone(user_id)
    if not current_tz:
        update_time_zone(user_id, current_selected_tz)
        current_tz = get_time_zone(user_id)
    if current_tz:
        current_selected_tz = current_tz.time_zone

    query.message.edit_text(
        f"Send your location. To cancel, press /cancel\n\nCurrent Timezone: {current_selected_tz}",
    )

    return INPUT_LOC


def input_loc_fn(update: Update, context):
    print(update)
    tf = TimezoneFinder()
    location = update.message.location
    latitude, longitude = location.latitude, location.longitude
    timezone_new = tf.timezone_at(lng=longitude, lat=latitude)
    update_time_zone(update.effective_chat.id, timezone_new)
    update.message.reply_text(f"Timezone set to {timezone_new}")
    return ConversationHandler.END


def done_fn(update, context):
    update.message.reply_text("Operation cancelled")
    return ConversationHandler.END


# dispatcher.add_handler(CallbackQueryHandler(change_tz_cfg_btn, pattern=r"config_tz"))
dispatcher.add_handler(
    ConversationHandler(
        entry_points=[CallbackQueryHandler(change_tz_cfg_btn, pattern=r"config_tz")],
        states={
            INPUT_LOC: [MessageHandler(Filters.location, input_loc_fn)],
        },
        fallbacks=[CommandHandler("cancel", done_fn)],
    )
)
