#!/usr/bin/env python3
"""this is the hash password method"""
import bcrypt
from db import DB
from user import User


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
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        session = self._db._session

        user = session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError(f'User {email} already exists')
        hashpassword = _hash_password(password=password)
        newuser = self._db.add_user(email=email, hashed_password=hashpassword)
        session.add(newuser)
        session.commit()
        return user
