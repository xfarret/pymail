import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DbEngine:
    engine = {}
    # session = None

    @staticmethod
    def get_engine(key, url='sqlite:///../database/emails.db'):
        if key not in DbEngine.engine:
            DbEngine.engine[key] = create_engine(url)

        return DbEngine.engine[key]

    @staticmethod
    def get_session(key='settings', url='sqlite:///../database/emails.db'):
        engine = DbEngine.get_engine(key, url)
        base = declarative_base()
        base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        DbEngine.session = DBSession()
        return DbEngine.session
