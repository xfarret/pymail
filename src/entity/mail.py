from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Mail(Base):
    __tablename__ = 'mail'

    id = Column(Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    password = Column(String(50), nullable=False)