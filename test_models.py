from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserTests(TestCase):

    def setUp(self):
        self.user = User(first_name= "First", last_name= "Last")
        db.session.add(self.user)
        db.session.commit()
        
        
    def tearDown(self):
        Post.query.delete()
        User.query.delete()
        db.session.commit()
        db.session.rollback()
    
    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "First Last")
    
    def test_default_image_url(self):
        test_user = User.query.get(self.user.id)
        self.assertEqual(test_user.image_url, "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")

class PostTests(TestCase):
    
    def test_foreign_key(self):
        self.post = Post(title="test post", content="test description", user_id=self.user.id)
        db.session.add(self.post)
        db.session.commit()
        test_user = User.query.get(self.user.id)
        test_post = Post.query.get(self.post.id)
        self.assertEqual(test_user.id, test_post.user_id)
    
    def test_relationship(self):
        self.post = Post(title="test post", content="test description", user_id=self.user.id)
        db.session.add(self.post)
        db.session.commit()
        test_user = User.query.get(self.user.id)
        all_posts = test_user.posts
        self.assertEqual(len(all_posts), 1)

    



