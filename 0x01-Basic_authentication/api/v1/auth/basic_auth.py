#!/usr/bin/env python3
"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""


from typing import TypeVar
from .auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """_summary_

    Args:
        Auth (_type_): _description_
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extract base64 authorization header

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        header = authorization_header.split(' ')
        if header[0] != 'Basic':
            return None
        else:
            return header[1]

    def decode_base64_authorization_header(self, base64_authorization_header):
        """decode base64 authorization header

        Args:
            base64_authorization_header (_type_): _description_
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encodebytes = base64_authorization_header.encode('utf-8')
            decodedbytes = base64.b64decode(encodebytes)
            decodedtext = decodedbytes.decode('utf-8')
            return decodedtext
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):  # type: ignore
        """EXTRACT USER CRED
        Args:
            self (_type_): _description_
            str (_type_): _description_
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        usremail, usrpassword = decoded_base64_authorization_header.split(':')
        return (usremail, usrpassword)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):  # type: ignore
        """user object from credentials

        Args:
            self (_type_): _description_
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
