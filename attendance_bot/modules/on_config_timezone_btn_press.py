#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
from telegram import (
    CallbackQuery,
    Update
)
from telegram.ext import (
    CallbackQueryHandler,
    run_async
)

from attendance_bot import (
    dispatcher
)
from attendance_bot.helpers.get_reply_markup_for_time_zone import (
    get_time_zone_ntb
)
from attendance_bot.sql.timezone_sql import (
    get_time_zone,
    update_time_zone
)


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

    current_tz = get_time_zone(user_id)
    if not current_tz:
        update_time_zone(
            user_id,
            current_selected_tz
        )
        current_tz = get_time_zone(user_id)
    if current_tz:
        current_selected_tz = current_tz.time_zone

    query.message.edit_text(
        f"#TBD current selected tz: {current_selected_tz}",
        reply_markup=get_time_zone_ntb(0)
    )


dispatcher.add_handler(
    CallbackQueryHandler(
        change_tz_cfg_btn,
        pattern=r"config_tz"
    )
)
