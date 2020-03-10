from models import User, db, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
jake = User(first_name='Jake', last_name='Gerry', image_url="/static/IMG_20180726_171802235.jpg")
lauren = User(first_name='Lauren', last_name='Hebert', image_url="/static/IMG_20180428_101516870_HDR.jpg" )
bace = User(first_name='Bace', last_name='Poplawski')

# Add new objects to session, so they'll persist
db.session.add_all([jake, lauren, bace])

# Commit--otherwise, this never gets saved!
db.session.commit()

post1 = Post(title='Kiting', content= 'Kitesurfing is great!', user_id=1)
post2 = Post(title='Climbing', content= 'Climbing is great!', user_id=1)
post3 = Post(title='Kittens', content= 'Kittens is great!', user_id=1)
post4 = Post(title='Cereal', content= 'Today I ate ceral with strawberries!', user_id=2)
post5 = Post(title='Drawing', content= 'I love to draw!', user_id=2)

outdoors = Tag(name="Outdoors")
food = Tag(name="Food")
art = Tag(name="Art")
animals = Tag(name="Animals")

db.session.add_all([post1, post2, post3, post4, post5, outdoors, food, art, animals])
db.session.commit()

post_tag1 = PostTag(post_id=1, tag_id=1)
post_tag2 = PostTag(post_id=5, tag_id=3)
post_tag3 = PostTag(post_id=2, tag_id=1)

db.session.add_all([post_tag1, post_tag2, post_tag3])
db.session.commit()



