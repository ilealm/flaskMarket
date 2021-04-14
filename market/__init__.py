from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# now I initialize the flask, and referers to the local python file I'm working with
app = Flask(__name__)  

# DB config. Note: I don't need to create the BD before, the next line creates it for me 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '9375c6484ab92cb1271e95f5'

db = SQLAlchemy(app)

from market import routes