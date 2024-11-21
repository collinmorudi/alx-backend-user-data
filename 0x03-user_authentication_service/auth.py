#!/usr/bin/env python3
"""A module for authentication-related routines."""


import bcrypt
from uuid import uuid4
from typing import Union

from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID (Universally Unique Identifier).

    Returns:
        str: A string representation of the UUID.
    """
    return str(uuid4())


class Auth:
    """Provides methods for user authentication and session management.

    Attributes:
        _db (DB): An instance of the DB class for database operations.
    """

    def __init__(self):
        """Initialize a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a new session for a user.

        Args:
            email (str): The user's email address.

        Returns:
            Union[str, None]: The session ID if successful, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
        self, session_id: str
    ) -> Union[User, None]:
        """Retrieve a user based on their session ID.

        Args:
            session_id (str): The user's session ID.

        Returns:
            Union[User, None]: The User object if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session.

        Args:
            user_id (int): The ID of the user.
        """
        if user_id is not None:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a password reset token for a user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If no user with the given email exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password.

        Args:
            reset_token (str): The password reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_password_hash = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=new_password_hash, reset_token=None
            )
        except NoResultFound:
            raise ValueError()
