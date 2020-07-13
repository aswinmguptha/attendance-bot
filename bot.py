#!/usr/bin/python3

import logging
import csv
import time

from telegram.ext import Updater, CommandHandler, run_async, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from io import StringIO, BytesIO
from datetime import datetime


class attendance_bot:
    def __init__(self, config):
        self.TOKEN = config.bot_api
        self.flag = 0
    
    def initialize(self):
        updater = Updater(token=self.TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        start_attendance_handler = CommandHandler('start_attendance', self.start_attendance)
        mark_attendance_handler= CallbackQueryHandler(self.mark_attendance)
        end_attendance_handler = CommandHandler('end_attendance', self.end_attendance)
        dispatcher.add_handler(start_attendance_handler)
        dispatcher.add_handler(mark_attendance_handler)
        dispatcher.add_handler(end_attendance_handler)
        updater.start_polling()
    
    @run_async
    def start(self, update, context):
        update.message.reply_text("Welcome")

    def start_attendance(self, update, context):
        self.flag += 1
        if self.flag != 1:
            update.message.reply_text("Please close the current attendance first")
            update.message.delete()
            return
        context.chat_data['list'] = []
        original_member = context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if original_member['status'] in ('creator', 'administrator'):
            keyboard = [[InlineKeyboardButton("Present", callback_data='present')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            self.message = update.message.reply_text("Please mark your attendance", reply_markup=reply_markup)
        else:
            update.message.reply_text("Only admins can execute this command")

        update.message.delete()

    @run_async
    def mark_attendance(self, update, context):
        query = update.callback_query
        choice = query.data
        if choice == 'present':
            _first_name = update.effective_user.first_name
            _last_name = update.effective_user.last_name or ''
            _time = datetime.now().strftime("%H:%M")
            _member = (len(context.chat_data['list']) + 1, update.effective_user.id, _first_name + ' ' + _last_name, _time)
            context.chat_data['list'].append(_member)
            context.bot.answer_callback_query(callback_query_id=query.id, text="Your attendance has been marked", show_alert=True)

    def end_attendance(self, update, context):
        original_member = context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if original_member['status'] in ('creator', 'administrator'):
            context.bot.edit_message_text(text="Attendance is over. {} people(s) marked attendance.".format(len(context.chat_data['list'])),
                                          chat_id=self.message.chat_id, message_id=self.message.message_id)
            date_and_time = datetime.now().strftime('%F-%A-%r')
            filename = f'{update.effective_chat.title}-Attendance-{date_and_time}.csv'
            caption = f'Attendees: {len(context.chat_data["list"])}\nDate: {datetime.now().strftime("%F")}\nTime: {datetime.now().strftime("%r")}'
            with StringIO() as f:
                _writer = csv.writer(f)
                _writer.writerows(context.chat_data['list'])
                f.seek(0)
                f = BytesIO(f.read().encode('utf8'))
                try:
                    context.bot.send_document(update.effective_user.id, f, filename=filename, caption=caption)
                except Exception as e:
                    context.bot.send_message(update.effective_chat.id, str(e))
                    context.bot.send_message(update.effective_chat.id, 'Posting result in the group...')
                    f.seek(0)
                    context.bot.send_document(update.effective_chat.id, f, filename=filename, caption=caption)

        self.flag = 0
        update.message.delete()

if __name__ == '__main__':

    attendance_checker = attendance_bot(Config)
    attendance_checker.initialize()
