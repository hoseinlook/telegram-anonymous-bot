from datetime import datetime

import pymysql
from sqlalchemy import create_engine, Integer, Column, String, DateTime, ForeignKey, Text
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

    id = Column(Integer(), primary_key=True, autoincrement=False)
    access_token = Column(String(length=100))
    name = Column(String(length=100))
    username = Column(String(length=100))
    created_at = Column(DateTime(), default=datetime.now)

    def __init__(self, user_id, name, access_token, created_at=None, username=None):
        self.id = user_id
        self.name = name
        self.username = username
        self.access_token = access_token
        self.created_at = created_at

    def __repr__(self):
        return F"<id={str(self.id)} , name={str(self.name)}>"

    def __str__(self):
        return self.__repr__()


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    from_user_id = Column(Integer, ForeignKey(User.id))
    to_user_id = Column(Integer, ForeignKey(User.id))
    message = Column(Text(), nullable=True)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)

    def __init__(self, from_user_id: int, to_user_id: int, message: str, created_at: datetime = None):
        self.id = None
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message
        self.created_at = created_at

    def __repr__(self):
        return F"<msg-id={self.id} , from={self.from_user_id}-->to={self.to_user_id }>"
