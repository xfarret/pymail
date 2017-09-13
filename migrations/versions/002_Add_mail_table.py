from sqlalchemy import *

meta = MetaData()

mail = Table(
    'mail', meta,
    Column('uid', Integer, nullable=False, unique=True, primary_key=True),
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
    Column('account_id', Integer, nullable=False),
    Column('label', String, nullable=False)
)

# Column('charset', String(100), nullable=True),


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    mail.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    mail.drop()
