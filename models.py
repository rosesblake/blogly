"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    image_url = db.Column(db.String(), nullable=True)
    #relationship
    user_posts = db.relationship('Post', backref='user')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

def connect_db(app):
    db.app = app
    db.init_app(app)

