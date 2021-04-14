from market import app
from flask import render_template, redirect, url_for
from market.models import Item, User

from market.forms import RegisterForm
from market import db


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
  items = Item.query.all()
  return render_template('market.html', items=items)


@app.route('/register', methods=['GET','POST'])
def register_page():
    # I need to have the form imported in order to be able to use it
    form = RegisterForm()
    # validations for when the user is submitting in the form. 
    # This happens when the user has submitted in the submit btn of the form
    if form.validate_on_submit():
      user_to_create = User(username = form.username.data, 
                            email_address =  form.email_address.data,
                            password_hash =  form.password1.data   )
      db.session.add(user_to_create)
      db.session.commit()
      return redirect(url_for('market_page'))

    # form.errors is a dictionary that has all the fails on the form validations declared in the form (form.py/RegisterForm)
    if form.errors != {}: 
      for err_msg in form.errors.values():
        print(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)