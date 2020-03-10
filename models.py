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

    # relationship to tag through postTag table
    tags = db.relationship("Tag", secondary="post_tags", backref="posts")

    # separate relationship to postTag table
    post_tag = db.relationship("PostTag", backref="posts")

class PostTag(db.Model):

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50),
                            nullable=False,
                            unique=True)
    post_tag = db.relationship("PostTag", backref="tags")

