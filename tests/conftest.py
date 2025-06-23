"""
Configure the test suite.
"""
import os
import tempfile

import pytest
# pylint: disable=import-error,redefined-outer-name
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    """ Create a test app."""
    db_fd, db_path = tempfile.mkstemp()

    the_app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test',
        'WTF_CSRF_ENABLED': False,
    })
    #app.test_client_class = FlaskClient

    with the_app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield the_app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """ Create a test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """ Create a test runner."""
    return app.test_cli_runner()

class AuthActions:
    """ Create a client that can authenticate itself."""
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        """ Log in as test user."""
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password},
            follow_redirects = True
        )

    def logout(self):
        """ Log out the current user."""
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """ Get a client that can authenticate itself."""
    return AuthActions(client)
