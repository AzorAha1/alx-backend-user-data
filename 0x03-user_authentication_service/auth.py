#!/usr/bin/env python3
"""this is the hash password method"""
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
            newuser = self._db.add_user(email=email, hashed_password=hashpassword)
            return newuser
        else:
            raise ValueError(f'User {email} already exists')
