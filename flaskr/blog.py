from flask import (
    Blueprint, g, redirect, render_template, url_for, flash, session
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
    """Home page of the site."""
    db_session = get_session()
    posts = db_session.query(Post).order_by(desc(Post.created))
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """View for creating a post, redirects to index on success."""
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

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """View for updating a post."""
    form = PostForm()
    db_session = get_session()
    post = db_session.query(Post).filter(Post.post_id == id).scalar()
    if post and post.user_id != session['user_id']:
        return render_template('errors/404.html'), 404
    if form.validate_on_submit() and post:
        title = form.title.data
        body = form.body.data
        db_session = get_session()
        post.title = title
        post.body = body
        db_session.commit()
        return redirect(url_for('blog.index'))
    elif post:
        form.title.data = post.title
        form.body.data  = post.body
        return render_template('blog/update.html', title='Update', id=id, form=form)
    else:
        flash('Invalid id')
        return render_template('errors/404.html'), 404
        

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """View for removing a post."""
    db_session = get_session()
    post = db_session.query(Post).filter(Post.post_id == id).scalar()
    if not post or post.user_id != session['user_id']:
        return render_template('errors/404.html'), 404
    else:
        db_session.delete(post)
        db_session.commit()
        return redirect(url_for('blog.index'))
