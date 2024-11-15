#!/usr/bin/env python3
"""Basic authentication module for the API."""


import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Handles Basic Authentication for the API."""

    def _extract_base64_token(self, authorization_header: str) -> str:
        """Extracts the Base64 token from the Authorization header.

        Args:
            authorization_header: The Authorization header from the request.

        Returns:
            The Base64-encoded token, or None if not found.
        """
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            match = re.fullmatch(pattern, authorization_header.strip())
            if match:
                return match.group('token')
        return None

    def _decode_base64_token(self, base64_token: str) -> str:
        """Decodes a Base64-encoded authentication token.

        Args:
            base64_token: The Base64-encoded token.

        Returns:
            The decoded token as a string, or None if decoding fails.
        """
        if isinstance(base64_token, str):
            try:
                decoded_bytes = base64.b64decode(base64_token, validate=True)
                return decoded_bytes.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def _extract_credentials(self, decoded_token: str) -> Tuple[str, str]:
        """Extracts username and password from the decoded token.

        Args:
            decoded_token: The decoded authentication token.

        Returns:
            A tuple containing the username and password,
            or (None, None) if extraction fails.
        """
        if isinstance(decoded_token, str):
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            match = re.fullmatch(pattern, decoded_token.strip())
            if match:
                return match.group('user'), match.group('password')
        return None, None

    def _find_user(self, email: str, password: str) -> TypeVar('User'):
        """Retrieves a user based on email and password.

        Args:
            email: The user's email address.
            password: The user's password.

        Returns:
            The User object if found and password matches,
            otherwise None.
        """
        if isinstance(email, str) and isinstance(password, str):
            try:
                users = User.search({'email': email})
            except Exception:  # Consider a more specific exception
                return None
            if users and users[0].is_valid_password(password):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the authenticated user from the request.

        Args:
            request: The incoming HTTP request.

        Returns:
            The User object if authenticated, otherwise None.
        """
        auth_header = self.authorization_header(request)
        base64_token = self._extract_base64_token(auth_header)
        decoded_token = self._decode_base64_token(base64_token)
        email, password = self._extract_credentials(decoded_token)
        return self._find_user(email, password)
