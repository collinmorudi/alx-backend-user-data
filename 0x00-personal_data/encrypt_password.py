#!/usr/bin/env python3
"""
This module provides functions for securely hashing passwords
and validating password hashes.
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a salt using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The previously hashed password.
        password (str): The plain text password to verify.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
