import abc

from sqlalchemy import and_
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session
import sqlalchemy.exc
from .models import Message, User, session_factory


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class BaseRepository(abc.ABC):
    class _Model(abc.ABC):
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("specify your model class ( _Model =...)")

    def __init__(self):
        self.session: Session = session_factory()

    def insert(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            pass
        except DataError as e:
            self.session.rollback()
            raise e

    def insert_many(self, obj_list):
        for obj in obj_list:
            self.session.add(obj)
        self.session.commit()

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()

    def delete_many(self, obj_list):
        for obj in obj_list:
            self.session.delete(obj)
        self.session.commit()

    def commit(self):
        self.session.commit()

    def all(self):
        return self.session.query(self._Model).all()


@singleton
class UserRepository(BaseRepository):
    _Model = User

    def get_user_with_id(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()


@singleton
class MessageRepository(BaseRepository):
    _Model = Message

    def get_with_message_id (self,message_id):
        return self.session.query(Message).filter(Message.id == message_id).first()

    def all_unseen_messages(self, user_id):
        return self.session.query(Message).filter(and_(Message.to_user_id == user_id, Message.status == Message.STATUS.SENT))


if __name__ == '__main__':
    UserRepository()
