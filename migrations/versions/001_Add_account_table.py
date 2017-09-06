from sqlalchemy import *

meta = MetaData()

account = Table(
    'account', meta,
    Column('id', Integer, nullable=False, unique=True, autoincrement=True, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('firstname', String(100), nullable=False),
    Column('lastname', String(100), nullable=False),
    Column('email', String(150), unique=True, nullable=False),
    Column('password', String(100), nullable=False)
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    account.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    account.drop()
