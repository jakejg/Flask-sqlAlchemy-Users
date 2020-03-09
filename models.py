"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String,
                            nullable=False,
                            unique=True)
    last_name = db.Column(db.String(20),
                            nullable=False,
                            unique=True)
    image_url = db.Column(db.String,
                            nullable=False,
                            default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    posts = db.relationship("Post", backref="user", passive_deletes=True)

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                            nullable=False,
                            unique=True)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    # user = db.relationship('User', backref="posts", cascade="all, delete")


