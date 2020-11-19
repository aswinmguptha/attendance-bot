#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, run_async

from attendance_bot import dispatcher

from attendance_bot.custom.filters import Filter


@run_async
def help_fn(update: Update, context):
    update.message.reply_text(
        r"""For the proper working of the bot, you should add the bot to your group and you should promote the bot as admin with delete messages privilage\. Here are the available commands\. Please note that the commands having 📤 emoji can be executed in bot's personalmessage only and commands having 👮 emoji can be executed by group admins in their group only\.

📤 /help \- To display this text
👮 /start\_attendance \- To start the attendance
👮 /end\_attendance \- To end the attendance and send the result as csv
👮 /config \- To configure the timezone and language

Please be noted that the end\_attendance command will send the result in csv format as a personal message to you only if you have had conversation with the bot before\. Otherwise it will sent to the group\.

If you found any issues or have any feature requests, head to our GitLab [issues](https://gitlab.com/keralagram/attendance-bot/-/issues) page\.""",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


dispatcher.add_handler(CommandHandler("help", help_fn, Filter.private))
