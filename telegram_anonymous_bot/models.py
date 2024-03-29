from datetime import datetime

import pymysql
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Text, Enum,BIGINT
from sqlalchemy.dialects.postgresql.base import PGDialect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

pymysql.install_as_MySQLdb()

PGDialect._get_server_version_info = lambda *args: (9, 2)
engine = create_engine(F'{config.SQL_TYPE}://{config.SQL_USER}:{config.SQL_PASSWORD}@{config.SQL_HOST}:{config.SQL_PORT}/{config.SQL_DB}',
                       )

# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


session_factory()


class User(Base):
    __tablename__ = 'users'

    class STATUS:
        ACTIVE = 'active'
        DEACTIVATE = 'deactivate'

    id = Column(BIGINT(), primary_key=True, autoincrement=False)
    access_hash = Column(String(length=100))
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    status = Column(Enum(STATUS.ACTIVE, STATUS.DEACTIVATE, name="status_s"), nullable=False)
    username = Column(String(length=100))
    created_at = Column(DateTime(), default=datetime.now)

    def __init__(self, user_id, last_name, first_name, access_hash, status, created_at=None, username=None):
        self.id = user_id
        self.status = status
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.access_hash = str(access_hash)
        self.created_at = created_at

    def __repr__(self):
        return F"<id={str(self.id)} , name={str(self.name)}>"

    def __str__(self):
        return self.__repr__()


class Message(Base):
    __tablename__ = 'messages'

    class STATUS:
        CREATED = 'created'
        SENT = "sent"
        SEEN = "seen"
        FAILED = "failed"

    id = Column(BIGINT(), primary_key=True, autoincrement=True, nullable=False)
    from_user_id = Column(BIGINT, ForeignKey(User.id))
    to_user_id = Column(BIGINT, ForeignKey(User.id))
    msg_id = Column(BIGINT, nullable=True, default=None)
    msg_from_bot_id = Column(BIGINT, nullable=True, default=None)
    message = Column(Text(), nullable=True)
    status = Column(Enum(STATUS.CREATED, STATUS.SENT, STATUS.FAILED, STATUS.SEEN, name='status_m'), default=STATUS.CREATED)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)

    def __init__(self, from_user_id: int, to_user_id: int, message: str, msg_id: int, created_at: datetime = None, msg_from_bot_id=None):
        self.id = None
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message
        self.created_at = created_at
        self.msg_id = msg_id
        self.msg_from_bot_id = msg_from_bot_id

    def __repr__(self):
        return F"<msgORM-id={self.id} msg_source_id={self.msg_id} msg_from_bot_id={self.msg_from_bot_id} , from={self.from_user_id}-->to={self.to_user_id}>"


class Action(Base):
    __tablename__ = 'actions'

    id = Column(BIGINT(), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BIGINT, ForeignKey(User.id))
    action = Column(Text(), nullable=False)
    msg_id = Column(BIGINT(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)

    def __init__(self, user_id: int, action: str, msg_id: int):
        self.user_id = user_id
        self.action = action
        self.msg_id = msg_id
