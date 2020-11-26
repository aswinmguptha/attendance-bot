import threading

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm.exc import NoResultFound
from attendance_bot.sql import BASE, SESSION


class AttendanceSheet(BASE):
    __tablename__ = "attendance_sheets"
    _id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(
        String, ForeignKey("users.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    user_id = Column(Integer)
    user_name = Column(String)
    time = Column(String)

    def __init__(self, chat_id, user_id, user_name, time):
        self.chat_id = chat_id
        self.user_id = user_id
        self.user_name = user_name
        self.time = time


AttendanceSheet.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def mark_attendance(chat_id, user_id, user_name, time):
    with INSERTION_LOCK:
        try:
            is_marked = (
                SESSION.query(AttendanceSheet)
                .filter(
                    AttendanceSheet.chat_id == chat_id,
                    AttendanceSheet.user_id == user_id,
                )
                .one()
            )
            return False
        except NoResultFound:
            is_marked = AttendanceSheet(chat_id, user_id, user_name, time)
            SESSION.add(is_marked)
            SESSION.commit()
            return True


def check_attendance(chat_id, user_id):
    with INSERTION_LOCK:
        try:
            is_marked = (
                SESSION.query(AttendanceSheet)
                .filter(
                    AttendanceSheet.chat_id == chat_id,
                    AttendanceSheet.user_id == user_id,
                )
                .one()
            )
            return True
        except NoResultFound:
            return False


def get_attendance_results(chat_id):
    with INSERTION_LOCK:
        return (
            SESSION.query(AttendanceSheet)
            .filter(AttendanceSheet.chat_id == chat_id)
            .all()
        )


# NOTE Optimize this
def clear_attendance_sheet(chat_id):
    with INSERTION_LOCK:
        chat_sheets = (
            SESSION.query(AttendanceSheet)
            .filter(AttendanceSheet.chat_id == chat_id)
            .all()
        )
        if chat_sheets:
            for sheet in chat_sheets:
                SESSION.delete(sheet)
            SESSION.commit()
            return True
        else:
            return False
