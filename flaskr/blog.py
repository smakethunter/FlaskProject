from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required, load_logged_in_user

from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')

def index():

    db = get_db()
    posts = db.execute('''SELECT p.id,
                       p.title,
                       p.body,
                       p.created,
                       p.author_id,
                       username
                       FROM post as p
                       INNER JOIN user u 
                       ON u.id = p.author_id
                       ORDER BY p.created DESC
                       ''').fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create')
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("""
                        INSERT INTO post (author_id, title, body)  
                        VALUES (?,?,?)
                        """, (g.user['id'], title, body))
            db.commit()
            return redirect(url_for('blog/create.html'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute("""
                            SELECT p.id, p.title,p.body,p.author_id, u.username 
                            FROM post as p
                            INNER JOIN user u on p.author_id = u.id
                            WHERE p.id = ?
                            """,
                            (id,)).fetchone()
    if post is None:
        abort(404,f"Post {id} doesn't exist")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

@bp.route('/int/<int:id>/update', methods = ('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))