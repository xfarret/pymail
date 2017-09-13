import email
import time
from sqlalchemy import Column, Integer, String, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Mail(Base):
    __tablename__ = 'mail'

    uid = Column(Integer, nullable=False, unique=True, primary_key=True)
    date_field = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    from_field = Column(String, nullable=False)
    reply_to = Column(String, nullable=False)
    to_field = Column(String, nullable=False)
    cc = Column(String, nullable=True)
    bcc = Column(String, nullable=True)
    message_id = Column(String(150), nullable=False)
    subject = Column(String, nullable=False)
    header = Column(String, nullable=False)
    body = Column(LargeBinary, nullable=True)
    priority = Column(Integer, nullable=True)
    content_type = Column(String(150), nullable=False)
    charset = Column(String(50), nullable=False)
    flags = Column(String, nullable=True)
    account_id = Column(Integer, nullable=False)
    label = Column(String, nullable=False)

    def __init__(self):
        pass
        # self.id = int(round(time.time() * 1000))

    def _get_date(self):
        return self.date_field

    def _set_date(self, date):
        self.date_field = date
        self.timestamp = time.mktime(email.utils.parsedate(date))

    date = property(_get_date, _set_date)