from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User

from market.forms import RegisterForm, LoginForm
from market import db
# for login
from flask_login import login_user



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
    # this function will execute 2 actions: 1) validate_ any fields that I have in forms, and 
    # 2) then execute the on_submit function
    if form.validate_on_submit():
      user_to_create = User(username = form.username.data, 
                            email_address =  form.email_address.data,
                            # password_hash =  form.password1.data   )
                            password =  form.password1.data   )
      db.session.add(user_to_create)
      db.session.commit()
      return redirect(url_for('market_page'))

    # form.errors is a dictionary that has all the fails on the form validations declared in the form (form.py/RegisterForm)
    if form.errors != {}: 
      for err_msg in form.errors.values():
        # print(f'There was an error with creating a user: {err_msg}')
        # I can add a category of the flash BC maybe I just want to inform
        # I'm sending the category "danger" BC bootstraps have one, So that I can customize the message
        flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    # this function will execute 2 actions: 1) validate_ any fields that I have in forms, and 
    # 2) then execute the on_submit function
    if form.validate_on_submit():
      # step 1: check if the user exists
      attempted_user = User.query.filter_by(username=form.username.data).first()
      # step 2: check if the password is correct
      if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
      else:
          flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)