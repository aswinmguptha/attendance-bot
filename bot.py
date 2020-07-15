#!/usr/bin/python3

import logging
import csv
import time

import telegram
from telegram.ext import Updater, CommandHandler, run_async, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from io import StringIO, BytesIO
from datetime import datetime


class attendance_bot:
    def __init__(self, config):
        self.TOKEN = config.bot_api
    
    def initialize(self):
        updater = Updater(token=self.TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        start_handler = CommandHandler('start', self.start, Filters.private)
        dispatcher.add_handler(start_handler)
        help_handler = CommandHandler('help', self.help, Filters.private)
        dispatcher.add_handler(help_handler)
        start_attendance_handler = CommandHandler('start_attendance', self.start_attendance, Filters.group)
        mark_attendance_handler= CallbackQueryHandler(self.mark_attendance)
        end_attendance_handler = CommandHandler('end_attendance', self.end_attendance, Filters.group)
        dispatcher.add_handler(start_attendance_handler)
        dispatcher.add_handler(mark_attendance_handler)
        dispatcher.add_handler(end_attendance_handler)
        updater.start_polling()
    
    @run_async
    def start(self, update, context):
        update.message.reply_text('''Hi,
Welcome to Group Attendance Bot\. Add me to your group to mark attendance\. Send /help to know more\. 
If you found any issues or have any feature requests, head to our GitLab [issues](https://gitlab.com/keralagram/attendance-bot/-/issues) page\.''', parse_mode=telegram.ParseMode.MARKDOWN_V2)

    def help(self, update, context):
        update.message.reply_text('''For the proper working of the bot, you should add the bot to your goup and you should promote the bot as admin with delete message privilage. Once you do this you can manage the bot with following commands. All these commands can be executed for the group admins only.
        
/start_attendance - To start the attendance
/end_attendance - To end the attendance and send the result as csv
        
Please be noted that the end_attendance command will send the result as csv as a personal message to you only if you have had conversation with the bot before. Otherwise it will sent to the group.''')

    def start_attendance(self, update, context):
        original_member = context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if original_member['status'] in ('creator', 'administrator'):
            if 'flag' in context.chat_data:
                update.message.reply_text("Please close the current attendance first")
                update.message.delete()
                return
            else:
                context.chat_data['flag'] = True
                context.chat_data['list'] = []
                keyboard = [[InlineKeyboardButton("Present", callback_data='present')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                self.message = update.message.reply_text("Please mark your attendance", reply_markup=reply_markup)
                update.message.delete()
        else:
            update.message.reply_text("Only admins can execute this command")
            update.message.delete()

    @run_async
    def mark_attendance(self, update, context):
        query = update.callback_query
        choice = query.data
        if choice == 'present':
            if [i for i, v in enumerate(context.chat_data['list']) if v[1] == update.effective_user.id]:
                context.bot.answer_callback_query(callback_query_id=query.id, text="You have already maked your attendance", show_alert=True)
            else:
                _first_name = update.effective_user.first_name
                _last_name = update.effective_user.last_name or ''
                _time = datetime.now().strftime("%H:%M")
                _member = (len(context.chat_data['list']) + 1, update.effective_user.id, _first_name + ' ' + _last_name, _time)
                context.chat_data['list'].append(_member)
                context.bot.answer_callback_query(callback_query_id=query.id, text="Your attendance has been marked", show_alert=True)

    def end_attendance(self, update, context):
        original_member = context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if original_member['status'] in ('creator', 'administrator'):
            if 'flag' not in context.chat_data:
                update.message.reply_text("Please start the attendance first")
                update.message.delete()
                return
            else:
                '''if 'list' not in context.chat_data:
                    context.bot.edit_message_text(text="Attendance is over. 0 people marked attendance.",
                                                  chat_id=self.message.chat_id, message_id=self.message.message_id)
                else:'''
                context.bot.edit_message_text(text="Attendance is over. {} people marked attendance.".format(len(context.chat_data['list'])),
                                          chat_id=self.message.chat_id, message_id=self.message.message_id)
                date_and_time = datetime.now().strftime('%F-%A-%r')
                filename = f'{update.effective_chat.title}-Attendance-{date_and_time}.csv'
                caption = f'Attendees: {len(context.chat_data["list"])}\nDate: {datetime.now().strftime("%F")}\nTime: {datetime.now().strftime("%r")}'
                with StringIO() as f:
                    _writer = csv.writer(f)
                    _writer.writerow(['Serial number','user id','Name','Time'])
                    _writer.writerows(context.chat_data['list'])
                    f.seek(0)
                    f = BytesIO(f.read().encode('utf8'))
                    if len(context.chat_data['list']) > 0:
                        try:
                            context.bot.send_document(update.effective_user.id, f, filename=filename, caption=caption)
                        except Exception as e:
                            context.bot.send_message(update.effective_chat.id, str(e))
                            context.bot.send_message(update.effective_chat.id, 'Posting result in the group...')
                            f.seek(0)
                            context.bot.send_document(update.effective_chat.id, f, filename=filename, caption=caption)
                del context.chat_data['flag']
        else:
            update.message.reply_text("Only admins can execute this command")
        update.message.delete()

if __name__ == '__main__':

    attendance_checker = attendance_bot(Config)
    attendance_checker.initialize()
