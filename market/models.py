from market import db

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