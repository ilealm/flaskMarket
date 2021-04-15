from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# now I initialize the flask, and referers to the local python file I'm working with
app = Flask(__name__)  

# DB config. Note: I don't need to create the BD before, the next line creates it for me 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '9375c6484ab92cb1271e95f5'

# DB connection 
db = SQLAlchemy(app)
# Password encryption
bcrypt = Bcrypt(app)
# login mgmt
login_manager = LoginManager(app)
# especify where the login route is located, so I can use login declarators in my routes, and redirect the user when needed.
login_manager.login_view = "login_page" # expects the login route
# this is for display flash messages
login_manager.login_message_category = 'info'

from market import routes