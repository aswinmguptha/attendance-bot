#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters, run_async

from attendance_bot import dispatcher, i18n
from attendance_bot.sql.users_sql import get_chat_by_userid, add_user
from attendance_bot.helpers.wrappers import localize


@run_async
@localize
def start_fn(update: Update, context):
    user_details = get_chat_by_userid(update.effective_user.id)
    if not user_details:
        chat_type = update.effective_chat.type
        if chat_type == "private":
            add_user(
                update.effective_user.id,
                update.effective_user.first_name,
                update.effective_user.last_name or "",
                chat_type,
            )
        else:
            add_user(
                update.effective_chat.id, update.effective_chat.title, "", chat_type
            )
    update.message.reply_sticker("CAADAgADQwoAAowucAAB9YyW9ZZhYnMWBA")
    update.message.reply_markdown(i18n.t("bot_welcome"))


dispatcher.add_handler(CommandHandler("start", start_fn, Filters.private))
