from unittest import TestCase

from app import app
from models import db, Users

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserTests(TestCase):

    def setUp(self):
        self.user = Users(first_name= "First", last_name= "Last")
        
    
    def tearDown(self):
        Users.query.delete()
        db.session.rollback()
    
    def test_get_full_name(self):
        self.assertEquals(self.user.get_full_name(), "First Last")
    
    def test_default_image_url(self):
        db.session.add(self.user)
        db.session.commit()
        test_user = Users.query.get(self.user.id)
        self.assertEquals(test_user.image_url, "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")

    



