import sqlite3
from datetime import datetime
import click
from flask import current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_session():
    if 'db_session' not in g:
        engine = create_engine(f"sqlite:///{current_app.config['DATABASE']}")
        Session = sessionmaker()
        Session.configure(bind=engine)
        g.db_session = Session()
        
    return g.db_session
        
def get_db():
    if 'db' not in g:
        print(current_app.config['DATABASE'])
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
 
    if db is not None:
        db.close()

def close_session(e=None):
    db_session = g.pop('db_session', None)

    if db_session is not None:
        db_session.close()

def init_db():
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
