from telegram import Chat
from telegram.ext.filters import BaseFilter


class Filter(object):
    class _Group(BaseFilter):
        def filter(self, message):
            if message.chat.type not in [Chat.GROUP, Chat.SUPERGROUP]:
                message.reply_text("Run this command in a group!")
            return message.chat.type in [Chat.GROUP, Chat.SUPERGROUP]

    group = _Group()
