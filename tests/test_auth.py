"""
Test the authentication functionality.
"""
import pytest
from flask import g, session
# pylint: disable=import-error,unused-argument
from flaskr.db import get_db


def test_register(client, app):
    """ Test that we can register a new user."""
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
        , follow_redirects=True)
    assert response.request.path == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Please fill in this field.'),
    ('a', '', b'Please fill in this field.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    """ Test the input validation on the register form."""
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert response.request.path == "/auth/register"

def test_login(client, auth):
    """ Test that we can log in."""
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.request.path == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user.username == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    """ Test the input validation on the login page."""
    response = auth.login(username, password)
    assert response.request.path == "/auth/login"

def test_logout(client, auth):
    """ Test that we can log out."""
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session
