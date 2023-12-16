# post_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import Post,User  # Import the Post model
from db import db  # Import the database instance

post_routes = Blueprint('post_routes', __name__, template_folder='templates')

@post_routes.route('/create_post', methods=['GET', 'POST'])
def create_post():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to create a post', 'error')
        return redirect(url_for('user_routes.login'))

    if request.method == 'POST':
        content = request.form['content']

        # Retrieve user information from the database based on the logged-in user
        user_id = session['user_id']
        user = User.query.get(user_id)

        if user:
            # Create a new post
            new_post = Post(content=content, author=user)
            db.session.add(new_post)
            db.session.commit()

            flash('Post created successfully', 'success')
            return redirect(url_for('user_routes.home'))  # Redirect to the home page or another appropriate page

    return render_template('create_post.html')


