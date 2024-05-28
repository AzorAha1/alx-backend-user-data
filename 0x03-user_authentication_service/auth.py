#!/usr/bin/env python3
"""this is the hash password method"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)
