"""Blogly application."""
#even the example project in course didnt run because of app_context(which was not mentioned), took me hours to figure out.
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = post.tags
    user_id = post.user.id
    return render_template('post-details.html', post=post, user_id=user_id, tags=tags)

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """show form to add new post for user"""
    user = User.query.get_or_404(user_id)
    tags = db.session.query(Tag).all()
    return render_template('add-post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """make post request with post input fields"""
    user = User.query.get_or_404(user_id)
    tags_ids = request.form.getlist('tags')
    # Create a new Post object
    new_post = Post(
        title=request.form.get('title'),
        content=request.form.get('content'),
        user_id=user.id  # Assign the user_id to link the post to the user
    )
    #loop through tag ids and append all tag info to the new post before committing
    for tag_id in tags_ids:
        tag = Tag.query.get(tag_id)
        if tag:
            new_post.tags.append(tag)
    
    # Add the new post to the db
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user.id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """get edit post form and show on page"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_submit(post_id):
    """submit edit to db from edit post form"""
    post = Post.query.get_or_404(post_id)
    tags_ids = request.form.getlist('tags')

    post.title = request.form.get('title-edit')
    post.content = request.form.get('content-edit')
    #clear current tags and re-loop, then append to post
    post.tags.clear()
    for tag_id in tags_ids:
        tag = Tag.query.get(tag_id)
        if tag:
            post.tags.append(tag)

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

@app.route('/tags')
def show_tags():
    """show tag list"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-details.html', tag=tag)

@app.route('/tags/new')
def create_tag_form():
    """show create tag form"""
    return render_template('create-tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag_submit():
    """submit request to add new tag to db"""
    name = request.form.get('add-tag')
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """show create tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit-tag.html', tag=tag)

#want to know how i can keep the same list order when I edit the tag, so it doesnt re-append to the end.
@app.route('//tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_submit(tag_id):
    """submit request to add new tag to db"""
    tag = db.session.get(Tag, tag_id)
    name = request.form.get('edit-tag')
    tag.name = name
    db.session.commit()
    return redirect('/tags')
# connect_db(app)
# db.create_all()
