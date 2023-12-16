from flask import Blueprint, request, jsonify,Response
from models import User,Post
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from flask import Flask, render_template, redirect, url_for, request
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

#from authform import RegistrationForm
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Perform form validation and user creation here
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            # Handle password mismatch error
            return render_template('register.html', error='Passwords do not match')

    return render_template('register.html', error=None)

@user_routes.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Login successful
            session['user_id'] = user.id
            #flash('Login successful', 'success')
            return redirect(url_for('user_routes.home'))
        else:
            # Login failed
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@user_routes.route('/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to access user profiles', 'error')
        return redirect(url_for('user_routes.login'))

    # Retrieve user information from the database based on the provided user_id
    user = User.query.get(user_id)

    if not user:
        flash('User not found', 'error')
        return redirect(url_for('user_routes.login'))

    # Check if the requested profile matches the logged-in user
    logged_in_user_id = session['user_id']
    if user.id != logged_in_user_id:
        flash('You can only view your own profile', 'error')
        return redirect(url_for('user_routes.login'))
    
    user_posts = Post.query.filter_by(author=user).all()

    return render_template('profile.html', user=user, user_posts=user_posts)


@user_routes.route('/home')
def home():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to access the home page', 'error')
        return redirect(url_for('user_routes.login'))

    return render_template('home.html')



   

@user_routes.route('/logout')
def logout():
    # Clear the user session
    session.pop('user_id', None)

    flash('Logout successful', 'success')
    return redirect(url_for('index'))