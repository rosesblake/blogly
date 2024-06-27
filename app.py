"""Blogly application."""
#even the example project in course didnt run because of app_context(which was not mentioned), took me hours to figure out.
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize SQLAlchemy and connect to app
db.init_app(app)
debug = DebugToolbarExtension(app)
#cant run without this context push
app.app_context().push()

#main users list page
@app.route('/')
def users_list():
    """show home page with list of users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/<int:user_id>')
def get_details(user_id):
    """show more details when clicking a user's name"""
    user = User.query.get_or_404(user_id)
    posts = user.user_posts
    return render_template('details.html', user=user, posts=posts)

@app.route('/create-user', methods=['GET'])
def create_user():
    """get html for form to create user"""
    return render_template('new-user.html')

@app.route('/create-user', methods=['POST'])
def create_new_user():
    """create new user based off of form input and redirect to details of new user"""
    # grab input fields 
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('img-url')

    # create new user to add to db 
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')

@app.route('/edit-user/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    """Get HTML for form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/edit-user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    """Update existing user based off of form input and redirect to details of updated user"""
    user = User.query.get_or_404(user_id)
    
    # grab input fields and directly change values
    user.first_name = request.form.get('edit-first-name')
    user.last_name = request.form.get('edit-last-name')
    user.image_url = request.form.get('edit-img-url')
    
    db.session.commit()

    return redirect(f'/{user.id}')

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete the user with the given user_id and redirect to home"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """display post"""
    post = db.session.get(Post, post_id)
    user_id = post.user.id
    return render_template('post-details.html', post=post, user_id=user_id)

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """show form to add new post for user"""
    user = User.query.get_or_404(user_id)
    return render_template('add-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """make post request with post input fields"""
    user = User.query.get_or_404(user_id)
    # Create a new Post object
    new_post = Post(
        title=request.form.get('title'),
        content=request.form.get('content'),
        user_id=user.id  # Assign the user_id to link the post to the user
    )
    
    # Add the new post to the db
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user.id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_submit(post_id):
    post = Post.query.get_or_404(post_id)

    post.title = request.form.get('title-edit')
    post.content = request.form.get('content-edit')

    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the user with the given user_id and redirect to home"""
    post = Post.query.get_or_404(post_id)
    user = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/{user}')
# connect_db(app)
# db.create_all()
