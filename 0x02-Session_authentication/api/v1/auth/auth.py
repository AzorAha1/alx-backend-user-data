#!/usr/bin/env python3
"""this is auth class"""


import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth public method"""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        if not path.endswith('/'):
            path = path + '/'
        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path = excluded_path + '/'
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        elif 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """current user"""
        return None

    def session_cookie(self, request=None):
        """session cookie"""
        if request is None:
            return None
        cookiename = os.getenv('SESSION_NAME')
        if cookiename is None:
            return None
        return request.cookies.get(cookiename)
