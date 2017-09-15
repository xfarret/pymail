import email
import time
from sqlalchemy import Column, Integer, String, Float, LargeBinary
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.declarative import declarative_base
from manager.encoder_manager import EncoderManager

Base = declarative_base()


class Mail(Base):
    __tablename__ = 'mail'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    uid = Column(Integer, nullable=False)
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
    # account_id = Column(Integer, nullable=False)
    label = Column(String, nullable=False)

    def __init__(self):
        pass
        # self.id = int(round(time.time() * 1000))

    def mail_from_bytes(self, bytes_data, uid):
        msg = email.message_from_bytes(bytes_data)

        self.uid = uid
        self.date = msg['date']
        self.to_field = EncoderManager.imap8859decode(msg['to'])
        self.from_field = EncoderManager.imap8859decode(msg['from'])
        self.reply_to = EncoderManager.imap8859decode(msg['reply-to'])
        self.cc = 'None'
        self.bcc = 'None'
        self.message_id = msg['message-id']
        self.subject = EncoderManager.imap8859decode(msg['subject'])
        self.header = 'None'
        self.content_type = msg.get_content_type()
        self.body = {}
        if msg.is_multipart():
            for payload in msg.get_payload():
                self.body[payload.get_content_type()] = payload.get_payload()
        else:
            self.body[self.content_type] = msg.get_payload()
        self.priority = msg['priority']
        self.charset = msg.get_content_charset()

        return self

    def _get_date(self):
        return self.date_field

    def _set_date(self, date):
        self.date_field = date
        self.timestamp = time.mktime(email.utils.parsedate(date))

    def persist(self, session):
        try:
            session.add(self)
            session.commit()
        except StatementError as e:
            # session.close()
            print(e)
            return False

        # session.close()
        return True

    def delete(self, session):
        try:
            session.delete(self)
            session.commit()
        except StatementError as e:
            # session.close()
            print (e)
            return False

        # session.close()
        return True

    date = property(_get_date, _set_date)
