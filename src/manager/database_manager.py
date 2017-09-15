import os
import sqlite3
from sqlalchemy import *
from db.engine import DbEngine


class DatabaseManager:
    __instance__ = None

    def __init__(self):
        self.tables = dict()
        self.tables['mail'] = \
            Table(
                'mail', MetaData(),
                Column('id', Integer, nullable=False, autoincrement=True, primary_key=True),
                Column('uid', Integer, nullable=False),
                Column('date_field', String, nullable=False),
                Column('timestamp', Float, nullable=False),
                Column('from_field', String, nullable=False),
                Column('reply_to', String, nullable=False),
                Column('to_field', String, nullable=False),
                Column('cc', String, nullable=True),
                Column('bcc', String, nullable=True),
                Column('message_id', String(150), nullable=False),
                Column('subject', String, nullable=True),
                Column('header', String, nullable=False),
                Column('body', LargeBinary, nullable=True),
                Column('priority', Integer, nullable=False),
                Column('content_type', String(150), nullable=True),
                Column('charset', String(50), nullable=True),
                Column('flags', String, nullable=True),
                # Column('account_id', Integer, nullable=False),
                Column('label', String, nullable=False)
            )

        self.tables['folder'] = \
            Table(
                'folder', MetaData(),
                Column('id', Integer, nullable=False, autoincrement=True, primary_key=True),
                Column('name', String, nullable=False),
                Column('parent_id', Integer, ForeignKey('folder.id')),
                Column('attributes', String, nullable=True),
                Column('unread_count', Integer, nullable=True),
            )


    @staticmethod
    def get_instance():
        """
        Singelton return AccountManager unique instance
        :return: AccountManager
        """
        if DatabaseManager.__instance__ is None:
            DatabaseManager.__instance__ = DatabaseManager()
        return DatabaseManager.__instance__

    def create_tables(self, account):
        """
        Create tables on database. If database doesn't exists, it will be created
        :param account:
        :return:
        """
        directory = '../database/' + account.email
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(directory + '/pymail.db'):
            with sqlite3.connect(directory + '/pymail.db') as conn:
                engine = DbEngine.get_engine(account.id, account.db_url)
                for table_name, table in self.tables.items():
                    table.metadata.bind = engine
                    table.create()
                    print("'" + table_name + "' created at [" + account.db_url + "]")
