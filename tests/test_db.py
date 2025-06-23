"""
Test the database.
"""
import sqlite3

import pytest
# pylint: disable=import-error,too-few-public-methods
from flaskr.db import get_db


def test_get_close_db(app):
    """ Test we can get a connection to the database and close it."""
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    """ Test the command for initialising the database."""
    class Recorder:
        """ Mock object for the db."""
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
