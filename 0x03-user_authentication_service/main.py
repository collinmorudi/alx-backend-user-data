#!/usr/bin/env python3
"""End-to-end integration tests for the user authentication service."""


import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def test_register_user(email: str, password: str) -> None:
    """Test user registration endpoint."""
    url = f"{BASE_URL}/users"
    body = {'email': email, 'password': password}

    # Successful registration
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    # Duplicate registration
    response = requests.post(url, data=body)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def test_login_wrong_password(email: str, password: str) -> None:
    """Test login with incorrect password."""
    url = f"{BASE_URL}/sessions"
    body = {'email': email, 'password': password}
    response = requests.post(url, data=body)
    assert response.status_code == 401


def test_login(email: str, password: str) -> str:
    """Test successful user login."""
    url = f"{BASE_URL}/sessions"
    body = {'email': email, 'password': password}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def test_profile_unlogged() -> None:
    """Test accessing user profile while not logged in."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def test_profile_logged(session_id: str) -> None:
    """Test accessing user profile while logged in."""
    url = f"{BASE_URL}/profile"
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def test_logout(session_id: str) -> None:
    """Test user logout."""
    url = f"{BASE_URL}/sessions"
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 302  # Expect a redirect after logout


def test_reset_password_token(email: str) -> str:
    """Test requesting a password reset token."""
    url = f"{BASE_URL}/reset_password"
    body = {'email': email}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    assert "reset_token" in response.json()
    return response.json().get('reset_token')


def test_update_password(email: str, reset_token: str,
                         new_password: str) -> None:
    """Test updating a user's password."""
    url = f"{BASE_URL}/reset_password"
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    test_register_user(EMAIL, PASSWD)
    test_login_wrong_password(EMAIL, NEW_PASSWD)
    test_profile_unlogged()
    session_id = test_login(EMAIL, PASSWD)
    test_profile_logged(session_id)
    test_logout(session_id)
    reset_token = test_reset_password_token(EMAIL)
    test_update_password(EMAIL, reset_token, NEW_PASSWD)
    test_login(EMAIL, NEW_PASSWD)
