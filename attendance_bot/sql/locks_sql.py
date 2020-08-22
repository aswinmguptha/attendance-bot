import threading

from sqlalchemy import Column, ForeignKey, String

from attendance_bot.sql import BASE, SESSION


class Lock(BASE):
    __tablename__ = "locks"
    chat_id = Column(
        String,
        ForeignKey("users.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    message_id = Column(String)

    def __init__(self, chat_id, message_id):
        self.chat_id = chat_id
        self.message_id = message_id


Lock.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def toggle_lock(chat_id, message_id=None):
    with INSERTION_LOCK:
        is_locked = SESSION.query(Lock).get(chat_id)
        if is_locked:
            SESSION.delete(is_locked)
            SESSION.commit()
            return False
        else:
            is_locked = Lock(chat_id, message_id)
            SESSION.add(is_locked)
            SESSION.commit()
            return True


def check_lock(chat_id):
    with INSERTION_LOCK:
        is_locked = SESSION.query(Lock).get(chat_id)
        if is_locked:
            return is_locked
        else:
            return False
