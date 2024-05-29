#!/usr/bin/env python3
"""this is the hash password method"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)


def _generate_uuid():
    """generate uuid

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """_summary_
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            User: _description_
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashpassword = _hash_password(password=password)
            return self._db.add_user(email=email, hashed_password=hashpassword)
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """valid login"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False
