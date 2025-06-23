"""
Initialising and accessing the database.
"""
import sqlite3
from datetime import datetime
import click
from flask import current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_app(app):
    """ Initialise the app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_session():
    """ Get a reference to the Flask session."""
    if 'db_session' not in g:
        engine = create_engine(f"sqlite:///{current_app.config['DATABASE']}")
        session = sessionmaker()
        session.configure(bind=engine)
        g.db_session = session()

    return g.db_session

def get_db():
    """
    Get a connection to the database from the global environment,
    creating and storing it if it does not exist.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Remove the connection to the database from the global environment
    and close it.
    """
    # pylint: disable=unused-argument
    db = g.pop('db', None)

    if db is not None:
        db.close()

def close_session(e=None):
    """
    Remove the handle to the SQLAlchemy session from the global
    environment and close it.
    """
    # pylint: disable=unused-argument
    db_session = g.pop('db_session', None)

    if db_session is not None:
        db_session.close()

def init_db():
    """ Initialise the database."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
