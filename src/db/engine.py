from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DbEngine:
    engine = None
    session = None

    @staticmethod
    def get_engine(url='sqlite:///../database/emails.db'):
        # sqlite => sqlite:///sqlalchemy_example.db
        if not DbEngine.engine:
            DbEngine.engine = create_engine(url)

        return DbEngine.engine

    @staticmethod
    def get_session(url='sqlite:///../database/emails.db'):
        engine = DbEngine.get_engine(url)
        base = declarative_base()
        base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        DbEngine.session = DBSession()
        return DbEngine.session
