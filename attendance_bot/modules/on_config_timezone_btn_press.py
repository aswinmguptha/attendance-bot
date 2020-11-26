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

from attendance_bot import dispatcher, i18n
from attendance_bot.sql.timezone_sql import get_time_zone, update_time_zone
from attendance_bot.sql.locks_sql import check_lock
from attendance_bot.helpers.wrappers import localize

INPUT_LOC = range(1)


@run_async
@localize
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
            i18n.t("can_not_change_while_in_progress", entity=i18n.t("timezone"))
        )
        return ConversationHandler.END

    current_tz = get_time_zone(user_id)
    if not current_tz:
        update_time_zone(user_id, current_selected_tz)
        current_tz = get_time_zone(user_id)
    if current_tz:
        current_selected_tz = current_tz.time_zone

    query.message.edit_text(
        i18n.t("send_location", current_tz=current_selected_tz),
    )

    return INPUT_LOC


def input_loc_fn(update: Update, context):
    tf = TimezoneFinder()
    location = update.message.location
    latitude, longitude = location.latitude, location.longitude
    timezone_new = tf.timezone_at(lng=longitude, lat=latitude)
    update_time_zone(update.effective_chat.id, timezone_new)
    update.message.reply_text(i18n.t("timezone_set_to", timezone_new=timezone_new))
    return ConversationHandler.END


def done_fn(update, context):
    update.message.reply_text(i18n.t("cancelled"))
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
