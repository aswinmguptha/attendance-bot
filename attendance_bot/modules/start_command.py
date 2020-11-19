#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters, run_async

from attendance_bot import dispatcher, i18n
from attendance_bot.helpers.wrappers import localize


@run_async
@localize
def start_fn(update: Update, context):
    update.message.reply_sticker("CAADAgADQwoAAowucAAB9YyW9ZZhYnMWBA")
    update.message.reply_markdown(i18n.t("bot_welcome"))


dispatcher.add_handler(CommandHandler("start", start_fn, Filters.private))
