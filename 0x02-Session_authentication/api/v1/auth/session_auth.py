#!/usr/bin/env python3
"""this will be a class"""

from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        else:
            sessionid = str(uuid4())
            self.user_id_by_session_id[sessionid] = user_id
            return sessionid
