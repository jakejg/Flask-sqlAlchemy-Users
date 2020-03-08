from unittest import TestCase

from app import app
from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):
        self.user = User(first_name= "First", last_name= "Last")
        
    def tearDown(self):
        User.query.delete()
        db.session.commit()
        db.session.rollback()

    def test_update(self):
        self.user.first_name= "NewFirst"
        db.session.add(self.user)
        db.session.commit()
        updated = User.query.get(self.user.id)
        self.assertEqual(updated.first_name, "NewFirst")
    
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first": "testFirst", "last": "testLast", "url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            test_user = User.query.filter_by(first_name="testFirst").first()
            self.assertEqual(test_user.image_url, "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
            
            html = resp.get_data(as_text=True)
            self.assertIn('testFirst testLast', html)
    
    def test_show_details(self):
        db.session.add(self.user)
        db.session.commit()

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Last', html)

    def test_delete_user(self):
        db.session.add(self.user)
        db.session.commit()

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('First Last', html)
        


