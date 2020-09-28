#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
from telegram import CallbackQuery, Update
from telegram.ext import CallbackQueryHandler, run_async

from attendance_bot import dispatcher
from attendance_bot.sql.languages_sql import get_language, update_language


@run_async
def change_language_cfg_btn(update: Update, context):
    query = update.callback_query
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differently
    # (and we can only answer once),
    # so we don't always answer here.
    query.answer()

    user_id = query.message.chat.id
    current_selected_language = "en"

    current_language = get_language(user_id)
    if not current_language:
        update_language(user_id, current_selected_language)
        current_language = get_language(user_id)
    if current_language:
        current_selected_language = current_language.language_code

    query.message.edit_text(
        f"#TBD current selected language: {current_selected_language}"
    )


dispatcher.add_handler(
    CallbackQueryHandler(change_language_cfg_btn, pattern=r"config_lang")
)
