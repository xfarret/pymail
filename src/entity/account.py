from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import imaplib

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'
    __imap_account__ = None
    __logged__ = False

    id = Column(Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    password = Column(String(50), nullable=False)
    imap_server = Column(String, nullable=False)
    imap_port = Column(Integer, nullable=True)
    smtp_server = Column(String, nullable=True)
    smtp_port = Column(Integer, nullable=True)

    def login(self):
        if not self.__logged__:
            self.__imap_account__ = imaplib.IMAP4_SSL(self.imap_server)
            typ, dat = self.__imap_account__.login(self.email, self.password)
            if typ == 'OK':
                self.__logged__ = True
        return self.__imap_account__

    def logout(self):
        if self.__logged__:
            self.__imap_account__.logout()
            self.__imap_account__ = None
            self.__logged__ = False

    def is_logged(self):
        if self.__imap_account__ is None:
            return False
        return True

    def _get_db_url(self):
        return 'sqlite:///../database/' + self.email + '/pymail.db'

    db_url = property(_get_db_url)
