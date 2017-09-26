from sqlalchemy import *
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

Base = declarative_base()


class Folder(Base):
    __tablename__ = 'folder'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('folder.id'))
    # last_seen_total = Column(Integer, nullable=True)
    # uid_validity = Column(Integer, nullable=True)
    # uid_next = Column(Integer, nullable=True)
    attributes = Column(String, nullable=True)
    unread_count = Column(Integer, nullable=True)

    parent = relation('Folder', remote_side=[id])

    @staticmethod
    def get_id(session, name):
        try:
            result = session.query(Folder.id).filter( Folder.name == name).one()

            if not result:
                return None

            return result[0]
        except:
            return None
