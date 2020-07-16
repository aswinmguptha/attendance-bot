import threading

from sqlalchemy import (
    Column,
    UnicodeText,
    String
)

from attendance_bot.sql import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    chat_id = Column(String, primary_key=True)
    first_name = Column(UnicodeText)
    last_name = Column(UnicodeText)
    language_code = Column(String)
    chat_type = Column(String)

    def __init__(
        self,
        user_id,
        first_name,
        last_name,
        language_code,
        chat_type
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code
        self.chat_type = chat_type

    def __repr__(self):
        return "<User {} ({})>".format(self.username, self.user_id)


Users.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def get_chat_by_userid(user_id):
    try:
        return SESSION.query(Users).get(
            Users.user_id == str(user_id)
        )
    finally:
        SESSION.close()


def del_user(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(Users).get(user_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
            return True
    return False


def add_user(
    user_id,
    first_name,
    last_name,
    language_code,
    chat_type
):
    with INSERTION_LOCK:
        adder = SESSION.query(Users).get(user_id)
        if adder:
            adder.first_name = first_name
            adder.last_name = last_name
            adder.language_code = language_code
            adder.chat_type = chat_type
        else:
            adder = Users(
                user_id,
                first_name,
                last_name,
                language_code,
                chat_type
            )
        SESSION.add(adder)
        SESSION.commit()


def update_language(
    user_id,
    language_code
):
    with INSERTION_LOCK:
        adder = SESSION.query(Users).get(user_id)
        if adder:
            adder.language_code = language_code
        SESSION.add(adder)
        SESSION.commit()
