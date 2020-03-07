from models import Users, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Users.query.delete()

# Add pets
jake = Users(first_name='Jake', last_name='Gerry', image_url="/static/IMG_20180726_171802235.jpg")
lauren = Users(first_name='Lauren', last_name='Hebert', image_url="/static/IMG_20180428_101516870_HDR.jpg" )
bace = Users(first_name='Bace', last_name='Poplawski')


# Add new objects to session, so they'll persist
db.session.add(jake)
db.session.add(lauren)
db.session.add(bace)

# Commit--otherwise, this never gets saved!
db.session.commit()
