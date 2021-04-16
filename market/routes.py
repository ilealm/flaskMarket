from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User

from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
# for login/logout Makes acccesible from other pages, eg. base.html
# I can also use the declarator loggin_required to force routes to be logged
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
# this will take the user auto to login page. I need to configure in __init__ where to go
@login_required
def market_page():
    # the next line is for the modal windows
    purchase_form = PurchaseItemForm()

    # this give me a dict with the values of the instance
    # print(purchase_form.__dict__)
    # then, I can access the elements like a dict
    # print(purchase_form['submit'])
    # I need to have imported request
    # print(request.form.get('purchased_item'))

    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            # validate budget
            if current_user.can_purchase(p_item_object):
              # assign the product to the logged user
              # p_item_object.owner = current_user.id
              # current_user.budget -= p_item_object.price
              # db.session.commit()
              p_item_object.buy(current_user)

              flash(f"Congratulations! You purchased {p_item_object.name}", category='success')
            else:
              flash(f"Not enough fonds to buy {p_item_object.name}.", category='danger')
        
        return redirect(url_for('market_page'))

    if request.method == 'GET':
        # items = Item.query.all()
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # I need to have the form imported in order to be able to use it
    form = RegisterForm()
    # this function will execute 2 actions: 1) validate_ any fields that I have in forms, and
    # 2) then execute the on_submit function
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              # password_hash =  form.password1.data   )
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        # log the new user
        login_user(user_to_create)
        # inform the user is logged
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')

        return redirect(url_for('market_page'))

    # form.errors is a dictionary that has all the fails on the form validations declared in the form (form.py/RegisterForm)
    if form.errors != {}:
        for err_msg in form.errors.values():
            # print(f'There was an error with creating a user: {err_msg}')
            # I can add a category of the flash BC maybe I just want to inform
            # I'm sending the category "danger" BC bootstraps have one, So that I can customize the message
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    # this function will execute 2 actions: 1) validate_ any fields that I have in forms, and
    # 2) then execute the on_submit function
    if form.validate_on_submit():
        # step 1: check if the user exists
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        # step 2: check if the password is correct
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again',
                  category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    # built in fun in flask to logout users
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
