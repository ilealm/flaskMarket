from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# now I initialize the flask, and referers to the local python file I'm working with
app = Flask(__name__)  

# DB config. Note: I don't need to create the BD before, the next line creates it for me 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '9375c6484ab92cb1271e95f5'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from market import routes