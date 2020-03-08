"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

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
    users = User.query.order_by("last_name").all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def form():
    return render_template('newuser.html')

@app.route('/users/new', methods=["POST"])
def user_form_data():
    first = request.form['first']
    last = request.form['last']
    url = request.form['url']

    if url:
        new_user = User(first_name=first, last_name=last, image_url=url)
    else:
        new_user = User(first_name=first, last_name=last)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def details(user_id):
    curr_user = User.query.get_or_404(user_id)
    posts = curr_user.posts
    return render_template('details.html', user=curr_user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit(user_id):

    curr_user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=curr_user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update(user_id):
    user = User.query.get_or_404(user_id)

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
def delete_user(user_id):
    
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    curr_user = User.query.get_or_404(user_id)
    return render_template('newpost.html', user=curr_user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form_data(user_id):

    new_post = Post(title=request.form['title'], content=request.form['content'], user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    post_id = new_post.id
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('editpost.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_data(post_id):
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    user_id =post.user_id
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')




    







