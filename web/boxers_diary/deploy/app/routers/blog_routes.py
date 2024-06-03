from flask import Blueprint, render_template

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blog/boxing')
def boxing():
    posts = [
        {"title": "Boxing Post 1", "content": "Content for boxing post 1", "user_id": 1},
        {"title": "Boxing Post 2", "content": "Content for boxing post 2", "user_id": 2},
    ]
    return render_template('blog.html', title="Бокс", posts=posts)

@blog_bp.route('/blog/swimming')
def swimming():
    posts = [
        {"title": "Swimming Post 1", "content": "Content for swimming post 1", "user_id": 1},
        {"title": "Swimming Post 2", "content": "Content for swimming post 2", "user_id": 2},
    ]
    return render_template('blog.html', title="Плаванье", posts=posts)

@blog_bp.route('/blog/chess')
def chess():
    posts = [
        {"title": "Chess Post 1", "content": "Content for chess post 1", "user_id": 1},
        {"title": "Chess Post 2", "content": "Content for chess post 2", "user_id": 2},
    ]
    return render_template('blog.html', title="Шахматы", posts=posts)

