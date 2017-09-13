from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

from db.engine import DbEngine

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

    # def __init__(self):
    #     pass
        # self.account = account
        # self.account_id = account.id

    # def create(self):
    #     session = DbEngine.get_session()
    #     try:
    #         session.add(self)
    #         session.commit()
    #     except:
    #         return False
    #     finally:
    #         session.close()
    #
    # def remove(self):
    #     pass
    #
    # def exists(self, account, name):
    #     labels = []
    #     session = DbEngine.get_session()
    #     for folder in session.query(Folder).filter(Folder.name == name and Folder.account_id == account.id):
    #         labels.append(folder)
    #     session.close()
    #     return labels
