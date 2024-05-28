#!/usr/bin/env python3
"""DB module
"""


import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """filter user"""
        try:
            firstuser = self.__session.query(User).filter_by(**kwargs).one()
            return firstuser
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> User:
        """update user"""
        user = self.find_user_by(id=user_id)
        if user:
            try:
                for key, value in kwargs.items():
                    if not hasattr(user, key):
                        raise ValueError
                    setattr(user, key, value)
                self._session.commit()
                return None
            except Exception:
                return Exception

    def _hash_pasword(self, password):
        """hash password
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        return bcrypt.hashpw(password=password)
