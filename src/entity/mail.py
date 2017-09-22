import email
import time
import json
from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import LargeBinary

from manager.encoder_manager import EncoderManager

Base = declarative_base()


class Mail(Base):
    __tablename__ = 'mail'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    uid = Column(Integer, unique=True, nullable=False)
    date_field = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    from_field = Column(String, nullable=False)
    reply_to = Column(String, nullable=True)
    to_field = Column(String, nullable=False)
    cc = Column(String, nullable=True)
    bcc = Column(String, nullable=True)
    message_id = Column(String(150), nullable=False)
    subject = Column(String, nullable=False)
    header = Column(String, nullable=False)
    body_format = Column(LargeBinary, nullable=True)
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
        if msg['to'] is not None:
            self.to_field = EncoderManager.imap8859decode(msg['to'])
        else:
            self.to_field = EncoderManager.imap8859decode(msg['delivered-to'])
        self.from_field = EncoderManager.imap8859decode(msg['from'])
        self.reply_to = EncoderManager.imap8859decode(msg['reply-to'])
        self.cc = 'None'
        self.bcc = 'None'
        self.message_id = msg['message-id']
        self.subject = EncoderManager.imap8859decode(msg['subject'])
        self.header = 'None'
        self.content_type = msg.get_content_type()
        body = {}
        if msg.is_multipart():
            for payload in msg.get_payload():
                if payload.get_content_type() == 'multipart/alternative' or \
                        payload.get_content_type() == 'text/plain' or \
                        payload.get_content_type() == 'text/html':
                    body = Mail.payload_to_string(payload)
        else:
            body[self.content_type] = msg.get_payload()
        self.body = body
        self.priority = msg['priority']
        self.charset = msg.get_content_charset()

        return self

    @staticmethod
    def payload_to_string(payload):
        body = {}

        if isinstance(payload, str):
            return payload

        if isinstance(payload, list):
            for msg_payload in payload:
                return Mail.payload_to_string(msg_payload.get_payload())
                # return body[msg_payload.get_content_type()] = content

        if isinstance(payload.get_payload(), str):
            body[payload.get_content_type()] = payload.get_payload()
            return body

        if isinstance(payload.get_payload(), email.message.Message):
                return body.update(Mail.payload_to_string(payload.get_payload()))
        else:
            if payload.get_content_type() == 'multipart/alternative':
                for msg_payload in payload.get_payload():
                    if isinstance(msg_payload.get_payload(), str):
                        body[msg_payload.get_content_type()] = msg_payload.get_payload()
                    else:
                        body[msg_payload.get_content_type()] = Mail.payload_to_string(msg_payload.get_payload())

        return body

    def _get_date(self):
        return self.date_field

    def _set_date(self, date):
        self.date_field = date
        self.timestamp = time.mktime(email.utils.parsedate(date))

    def _get_body(self):
        return json.loads(self.body_format).decode()

    def _set_body(self, value):
        self.body_format = json.dumps(value).encode()

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

    @staticmethod
    def get_mail(session, uid):
        try:
            obj = session.query(Mail).filter(Mail.uid == uid).one()

            return obj
        except StatementError as e:
            print(e)
            return False

    @staticmethod
    def get_last(session):
        try:
            obj = session.query(Mail).order_by(Mail.id.desc()).first()

            return obj
        except StatementError as e:
            print(e)
            return False

    date = property(_get_date, _set_date)
    body = property(_get_body, _set_body)

    @staticmethod
    def get_uids(session):
        try:
            uids = session.query(Mail.uid).all()
            # return uids
            result = list()

            for uid in uids:
                result.append(uid[0])

            return result
        except StatementError as e:
            print(e)
            return False
