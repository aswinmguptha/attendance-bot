#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import attendance_bot

from datetime import datetime
from pathlib import Path
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, run_async

from mwt import MWT

from attendance_bot import dispatcher, i18n
from attendance_bot.sql.languages_sql import get_language, update_language
from attendance_bot.sql.locks_sql import check_lock
from attendance_bot.helpers.wrappers import localize


@MWT(60 * 5)
def gen_locale_keyboard():
    keyboard = []
    language_list = {}
    count = 0
    temp = []
    files = os.listdir(os.path.join((Path(attendance_bot.__file__).parent).parent, "locale"))
    files.remove("README.md")
    for _file in files:
        count += 1
        with open(os.path.join(os.path.join((Path(attendance_bot.__file__).parent).parent, "locale"), _file), "r") as f:
            data = json.load(f)
            temp.append(
                InlineKeyboardButton(
                    f'{data["lang_info"]["name"]} {data["lang_info"]["icon"]}',
                    callback_data="config_ind_lang_" + data["lang_info"]["short"],
                )
            )
            language_list[data["lang_info"]["short"]] = (
                data["lang_info"]["name"] + " " + data["lang_info"]["icon"]
            )
        if count % 3 == 0:
            keyboard.append(temp)
            temp = []
        elif count == len(files):
            keyboard.append(temp)
    return InlineKeyboardMarkup(keyboard), language_list


@run_async
@localize
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
    if current_language:
        current_selected_language = current_language.language_code
    else:
        update_language(user_id, current_selected_language)
        current_language = current_selected_language

    keyboard, language_list = gen_locale_keyboard()

    query.message.edit_text(
        i18n.t(
            "locale_menu",
            current_language=language_list[current_selected_language],
        ),
        parse_mode="MARKDOWN",
        reply_markup=keyboard,
    )


@run_async
@localize
def change_language_individual(update: Update, context):
    update_language(update.effective_chat.id, context.match.group(1))
    context.bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=i18n.t("success"),
        show_alert=True,
    )
    update.effective_message.delete()


dispatcher.add_handler(
    CallbackQueryHandler(change_language_cfg_btn, pattern=r"config_lang")
)
dispatcher.add_handler(
    CallbackQueryHandler(change_language_individual, pattern=r"config_ind_lang_(.+)")
)
