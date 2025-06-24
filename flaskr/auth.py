"""
Views for the Admin functionality.
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from flaskr.db import get_session
from flaskr.forms import UserForm
from flaskr.model import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """View for registering a user."""
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = generate_password_hash(form.password.data)
        db_session = get_session()
        db_session.add(user)

        if user.username is None:
            flash(f"User {form.username.data} is missing.")
        if user.password is None:
            flash(f"User {form.password.data} is missing.")

        try:
            db_session.commit()
        except IntegrityError:
            flash(f"User {form.username.data} is already registered.")
        else:
            return redirect(url_for("auth.login"))
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """View for logging in."""
    form = UserForm()
    if form.validate_on_submit():
        db_session = get_session()
        user = (
            db_session
            .query(User)
            .filter(User.username == form.username.data)
            .scalar())
        #current_app.logger.debug(f'{user.username}')
        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, form.password.data):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user.user_id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    """Hook that puts the logged in user into the session.""" 
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_session().query(User).filter(User.user_id == user_id).scalar()
        session['user_id'] = user_id


@bp.route('/logout')
def logout():
    """View for logging out."""
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    """Decorator that wraps views for which we need a logged in user."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def test_ci():
    pass
