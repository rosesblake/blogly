"""Blogly application."""
#even the example project in course didnt run because of app_context(which was not mentioned), took me hours to figure out.
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User

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
    return render_template('details.html', user=user)

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


# connect_db(app)
# db.create_all()
