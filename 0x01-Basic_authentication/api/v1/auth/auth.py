#!/usr/bin/env python3
"""Authentication module for the API."""


import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Base authentication class for the API.

    Provides methods for checking authentication requirements
    and extracting authorization headers.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a given path requires authentication.

        Args:
            path: The path to check.
            excluded_paths: A list of paths that are excluded from authentication.
                Paths can include wildcards:
                    - '*' matches any characters (e.g., '/api/v1/*' matches all paths under '/api/v1/')
                    - '/' at the end acts as a wildcard for the next path segment (e.g., '/api/v1/' matches '/api/v1/users')

        Returns:
            True if the path requires authentication, False otherwise.
        """
        if path and excluded_paths:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                # Build a regular expression pattern from the exclusion path
                if exclusion_path.endswith('*'):
                    pattern = f'{exclusion_path[:-1]}.*'  # Match any characters after the *
                elif exclusion_path.endswith('/'):
                    pattern = f'{exclusion_path[:-1]}/.*'  # Match any characters after the /
                else:
                    pattern = f'{exclusion_path}/.*'  # Match any characters in the next segment

                # Check if the path matches the pattern
                if re.match(pattern, path):
                    return False  # Path is excluded
        return True  # Path requires authentication

    def authorization_header(self, request=None) -> str:
        """Gets the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            The value of the Authorization header, or None if not present.
        """
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current authenticated user.

        Args:
            request: The Flask request object.

        Returns:
            The User object representing the current user, or None if not authenticated.
        """
        return None  # This will be implemented in subclasses
