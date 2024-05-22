#!/usr/bin/env python3
"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""


from .auth import Auth


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
