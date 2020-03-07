"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/users')
    
@app.route('/users')
def list_users():
    users = Users.query.order_by("last_name").all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def form():
    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def form_data():
    first = request.form['first']
    last = request.form['last']
    url = request.form['url']

    if url:
        new_user = Users(first_name=f"{first}", last_name=f"{last}", image_url=f"{url}")
    else:
        new_user = Users(first_name=f"{first}", last_name=f"{last}")

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def details(user_id):
    curr_user = Users.query.get_or_404(user_id)
    return render_template('details.html', user=curr_user)

@app.route('/users/<int:user_id>/edit')
def edit(user_id):

    curr_user = Users.query.get_or_404(user_id)
    return render_template('edit.html', user=curr_user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update(user_id):
    user = Users.query.get_or_404(user_id)

    user.first_name = request.form['first']
    user.last_name = request.form['last']

    if request.form['url']:
        user.image_url = request.form['url']
    else:
        user.image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete(user_id):
    
    Users.query.filter_by(id = user_id).delete()
    db.session.commit()
    
    return redirect('/users')

    







