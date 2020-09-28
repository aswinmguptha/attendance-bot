from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.filters import BaseFilter

from attendance_bot import BOT_USERNAME, updater
from attendance_bot.custom.jobs import schedule_delete


class Filter(object):
    class _Group(BaseFilter):
        def filter(self, message):
            if message.chat.type not in [Chat.GROUP, Chat.SUPERGROUP]:
                message.reply_text("Run this command in a group!")
                return False
            return True

    group = _Group()

    class _Private(BaseFilter):
        def filter(self, message):
            if message.chat.type != Chat.PRIVATE:
                reply_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Click Here", url=f"https://t.me/{BOT_USERNAME}"
                            )
                        ]
                    ]
                )
                msg = message.reply_text(
                    "Run this command in PM!", reply_markup=reply_keyboard
                )
                schedule_delete(message.chat.id, msg.message_id, 10)
                message.delete()
                return False
            message.delete()
            return True

    private = _Private()

    class _Admin(BaseFilter):
        def filter(self, message):
            sender = updater.bot.get_chat_member(message.chat.id, message.from_user.id)
            print(sender.status)
            if sender.status not in ["creator", "administrator"]:
                msg = message.reply_text("Only admins can execute this command")
                schedule_delete(message.chat.id, msg.message_id, 10)
                try:
                    message.delete()
                except:
                    pass
                return False
            try:
                message.delete()
            except:
                pass
            return True

    admin = _Admin()
