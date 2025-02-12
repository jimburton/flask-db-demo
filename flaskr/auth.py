import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.forms import UserForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = UserForm()
    #print(f"Form submitted and valid:{form.validate_on_submit()}")
    if form.validate_on_submit():
        db = get_db()
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (form.username.data, generate_password_hash(form.password.data)),
            )
            db.commit()
        except db.IntegrityError:
            flash(f"User {form.username.data} is already registered.")
        else:
            return redirect(url_for("auth.login"))

    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = UserForm()
    if form.validate_on_submit():
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (form.username.data,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], form.password.data):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
