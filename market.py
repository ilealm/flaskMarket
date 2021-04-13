from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# now I initialize the flask, and referers to the local python file I'm working with
app = Flask(__name__)  

# DB config. Note: I don't need to create the BD before, the next line creates it for me 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

# MODELS
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True )    
    price = db.Column(db.Integer(), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)

    # I'm using this to return the value in name field 
    def __repr__(self):
        return f'Item {self.name}'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
  items = Item.query.all()
  return render_template('market.html', items=items)