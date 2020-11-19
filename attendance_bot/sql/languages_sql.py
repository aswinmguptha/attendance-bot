import threading

from sqlalchemy import Column, ForeignKey, String

from attendance_bot.sql import BASE, SESSION


class LanguageCode(BASE):
    __tablename__ = "language_code"
    chat_id = Column(
        String,
        ForeignKey("users.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    language_code = Column(String)

    def __init__(self, chat_id, language_code):
        self.chat_id = chat_id
        self.language_code = language_code

    def __repr__(self):
        return "<Language {} ({})>".format(self.language_code, self.chat_id)


LanguageCode.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def update_language(user_id, language_code):
    with INSERTION_LOCK:
        adder = SESSION.query(LanguageCode).get(user_id)
        if adder:
            adder.language_code = language_code
        else:
            adder = LanguageCode(user_id, language_code)
        SESSION.add(adder)
        SESSION.commit()


def get_language(user_id):
    try:
        return SESSION.query(LanguageCode).get(user_id)
    finally:
        SESSION.close()
