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
    chat_type = Column(String)

    def __init__(
        self,
        chat_id,
        first_name,
        last_name,
        chat_type
    ):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.chat_type = chat_type

    def __repr__(self):
        return "<User {} ({})>".format(self.first_name, self.chat_id)


Users.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def get_chat_by_userid(user_id):
    try:
        return SESSION.query(Users).get(
            str(Users.chat_id) == str(user_id)
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
    chat_type
):
    with INSERTION_LOCK:
        adder = SESSION.query(Users).get(user_id)
        if adder:
            adder.first_name = first_name
            adder.last_name = last_name
            adder.chat_type = chat_type
        else:
            adder = Users(
                user_id,
                first_name,
                last_name,
                chat_type
            )
        SESSION.add(adder)
        SESSION.commit()
