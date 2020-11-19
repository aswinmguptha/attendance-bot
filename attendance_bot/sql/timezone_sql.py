import threading

from sqlalchemy import Column, ForeignKey, String

from attendance_bot.sql import BASE, SESSION


class TimeZone(BASE):
    __tablename__ = "time_zone"
    chat_id = Column(
        String,
        ForeignKey("users.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    time_zone = Column(String)

    def __init__(self, chat_id, time_zone):
        self.chat_id = chat_id
        self.time_zone = time_zone

    def __repr__(self):
        return "<TimeZone {} ({})>".format(self.time_zone, self.chat_id)


TimeZone.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def update_time_zone(user_id, time_zone):
    with INSERTION_LOCK:
        adder = SESSION.query(TimeZone).get(user_id)
        if adder:
            adder.time_zone = time_zone
        else:
            adder = TimeZone(user_id, time_zone)
        SESSION.add(adder)
        SESSION.commit()


def get_time_zone(user_id):
    try:
        return SESSION.query(TimeZone).get(user_id)
    finally:
        SESSION.close()
