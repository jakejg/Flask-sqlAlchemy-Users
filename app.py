"""Blogly application."""
import datetime
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag

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
    """Show the 5 most recent posts"""

    posts = Post.query.order_by(Post.created_at.desc()).all()
    
    return render_template('recent.html', posts=posts)
    
@app.route('/users')
def list_users():
    """Show users in alphabetical order by last name"""

    users = User.query.order_by("last_name").all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def form():
    """Show form to create a new user"""

    return render_template('newuser.html')

@app.route('/users/new', methods=["POST"])
def user_form_data():
    """Create new users and add to databse"""

    first = request.form['first']
    last = request.form['last']
    url = request.form['url']

    if url:
        new_user = User(first_name=first, last_name=last, image_url=url)
    else:
        new_user = User(first_name=first, last_name=last)

    db.session.add(new_user)
    db.session.commit()
    
    flash("New user created!")
    return redirect('/users')

@app.route('/users/<int:user_id>')
def details(user_id):
    """Show details for current user"""

    curr_user = User.query.get_or_404(user_id)
    posts = curr_user.posts
    return render_template('details.html', user=curr_user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit(user_id):
    """Show form to edit a current user"""

    curr_user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=curr_user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update(user_id):
    """Update user"""

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
    """Delete user"""
    
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Show form to add a post"""

    curr_user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by("name").all()
    return render_template('newpost.html', user=curr_user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form_data(user_id):
    """Create post and save to database"""

    new_post = Post(title=request.form['title'], content=request.form['content'], user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    add_to_post_tags_table(new_post, Tag, "tag_ids")

    post_id = new_post.id
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post details"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template('post.html',post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit a post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by("name").all()
    curr_tags =  post.tags

    return render_template('editpost.html', post=post, tags=tags, curr_tags=curr_tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_data(post_id):
    """Update post"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']
    request.form.getlist("tag_id")

    post.tags = [Tag.query.get(tag_id) for tag_id in request.form.getlist("tag_id")]
        
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete post"""
    
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.errorhandler(404) 
def not_found(e):  
    """Custom 404 not found page"""

    return render_template("404.html") 

@app.route('/tags')
def tag_list():
    """Show all tags"""
    tags = Tag.query.order_by("name").all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show tag details"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tagdetails.html', tag=tag, posts=posts)

@app.route('/tags/new')
def show_add_tag_form():
    """Show form to create a tag"""

    posts = Post.query.all()
    return render_template('addTagForm.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def tag_form_data():
    """Create tag"""

    new_tag = Tag(name=request.form["name"])

    db.session.add(new_tag)
    db.session.commit()

    add_to_post_tags_table(new_tag, Post, "post_ids")
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show form to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('editTagForm.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag_form_data(tag_id):
    """Update a tag"""

    tag = Tag.query.get_or_404(tag_id)
    
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """ Delete a tag"""
    
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')



def add_to_post_tags_table(object1, type1, query):
    """Add a row to the post_tags_table """

    ids = request.form.getlist(query)
    for id in ids:
        tag_or_post_object = type1.query.get(id)
        if type1 == Post:
            tag_or_post_object.post_tag.append(PostTag(post_id=int(id), tag_id=object1.id))
        else:
            tag_or_post_object.post_tag.append(PostTag(post_id=object1.id, tag_id=int(id)))
    db.session.commit()




    







