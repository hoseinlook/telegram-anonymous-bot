from datetime import datetime

import pymysql
from sqlalchemy import create_engine, Integer, Column, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

pymysql.install_as_MySQLdb()

engine = create_engine(F'mysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}',
                       isolation_level="READ UNCOMMITTED",
                       )

# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


class User(Base):
    __tablename__ = 'users'

    class STATUS:
        ACTIVE = 'active'
        DEACTIVATE = 'deactivate'

    id = Column(Integer(), primary_key=True, autoincrement=False)
    access_hash = Column(String(length=100))
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    status = Column(Enum(STATUS.ACTIVE, STATUS.DEACTIVATE), nullable=False)
    username = Column(String(length=100))
    created_at = Column(DateTime(), default=datetime.now)

    def __init__(self, user_id, last_name, first_name, access_hash, status, created_at=None, username=None):
        self.id = user_id
        self.status = status
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.access_hash = access_hash
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

    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    from_user_id = Column(Integer, ForeignKey(User.id))
    to_user_id = Column(Integer, ForeignKey(User.id))
    msg_id = Column(Integer, nullable=True, default=None)
    message = Column(Text(), nullable=True)
    status = Column(Enum(STATUS.CREATED, STATUS.SENT, STATUS.FAILED, STATUS.SEEN), default=STATUS.CREATED)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)

    def __init__(self, from_user_id: int, to_user_id: int, message: str, msg_id: int, created_at: datetime = None):
        self.id = None
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message
        self.created_at = created_at
        self.msg_id = msg_id

    def __repr__(self):
        return F"<msg-id={self.id} , from={self.from_user_id}-->to={self.to_user_id}>"
