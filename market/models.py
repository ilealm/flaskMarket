from market import db, login_manager
from market import bcrypt
# for login mgnt
# UserMixin: this class inherits is_authenticated, is_active, is_annonymous, get_id. 
# So I don't have to implemented as it says in the docs.
# I must add it in the User class
from flask_login import UserMixin

# Login manager. This is the one that will be accesible from all pages
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




# MODELS
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    # this is the one that creates the relationship with the model, but is not stored as a column
    # backref is the field to relate to all the items the user has. Also to see the 
    # owner of specific item
    # I need lazy=True to grab all the user's items in one shot
    items = db.relationship('Item', backref='owned_user', lazy=True)

    # the next lines are for hashing the passwordjj
    # create an attribute that will be accesable from each instance. 
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):    
        # overwrite what is going to be store in password_hash
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    # to check if the psw is valid while login 
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)





class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True )    
    price = db.Column(db.Integer(), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    # relationship to the user. 'user.id' must be in lower case
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # I'm using this to return the value in name field 
    def __repr__(self):
        return f'Item {self.name}'