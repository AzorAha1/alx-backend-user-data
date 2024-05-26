#!/usr/bin/env python3
"""this will be a class"""

from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """_summary_

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        else:
            sessionid = str(uuid4())
            self.user_id_by_session_id[sessionid] = user_id
            return sessionid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """_summary_

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
