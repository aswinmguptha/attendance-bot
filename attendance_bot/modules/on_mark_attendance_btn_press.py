#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
from telegram import (
    Update
)
from telegram.ext import (
    CallbackQueryHandler,
    run_async
)

from attendance_bot import (
    dispatcher
)


@run_async
def mark_attendance_fn(update: Update, context):
    query = update.callback_query
    choice = query.data
    if choice == 'present':
        if any(
            (
                v[1] == update.effective_user.id
                for v in context.chat_data['list']
            )
        ):
            context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="You have already marked your attendance",
                show_alert=True
            )
        else:
            _first_name = update.effective_user.first_name
            _last_name = update.effective_user.last_name or ''
            _time = datetime.now().strftime("%H:%M")
            _member = (
                len(context.chat_data['list']) + 1,
                update.effective_user.id,
                _first_name + ' ' + _last_name,
                _time
            )
            context.chat_data['list'].append(_member)
            context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="Your attendance has been marked",
                show_alert=True
            )


dispatcher.add_handler(
    CallbackQueryHandler(
        mark_attendance_fn
    )
)
