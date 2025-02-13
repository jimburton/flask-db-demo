from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from sqlalchemy import desc
from sqlalchemy.sql.functions import now
from flaskr.auth import login_required
from flaskr.db import get_session
from flaskr.forms import PostForm
from flaskr.model import Post

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db_session = get_session()
    posts = db_session.query(Post).order_by(desc(Post.created))
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.body = form.body.data
        post.user_id = g.user.user_id
        post.created = now()
        db_session = get_session()
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('blog.index'))

    return render_template('blog/create.html', form=form)

def get_post(id, check_author=True):
    post = get_session().query(Post).filter(Post.post_id == id).scalar()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.user_id != g.user.user_id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db_session = get_session()
            post = db_session.query(Post).filter(Post.post_id == id).scalar()
            post.title = title
            post.body = body
            db_session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db_session = get_session()
    post = db_session.query(Post).filter(Post.post_id == id).scalar()
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for('blog.index'))
