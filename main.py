from flask import Flask, request, Response,jsonify,render_template
from werkzeug.utils import secure_filename
from models import User, Post
from db import db_init, db
from user_routes import user_routes

from post_routes import post_routes
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Tanmay!2'
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(post_routes, url_prefix='/post')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinmay1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


@app.route('/')
def index():
   return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,port = 8000)