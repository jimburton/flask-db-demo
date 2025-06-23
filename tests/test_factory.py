"""
Test the app factory.
"""
# pylint: disable=import-error
from flaskr import create_app


def test_config():
    """ Test the app factory config."""
    assert not create_app().testing
    assert create_app({'TESTING': True,
                       'WTF_CSRF_ENABLED': False}).testing
