"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class Users(db.Model):

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
