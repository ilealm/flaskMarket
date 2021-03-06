from flask_wtf import FlaskForm
# I need to import the fields I'm going to need
from wtforms import StringField, PasswordField, SubmitField
# to add form validations
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


# Register form
class RegisterForm(FlaskForm):
    # I need to validate unique fields before trying to add it to the table
    # Flask will execute this functions auto on form.validate_on_submit()
    # I just NEED TO ADD "validate_" and the field to validate
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    # to be able to use validators, I need to import wtforms. If I want to add more than 1 validator, then add []
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    # I don't need to add the validator to psw2 bc it must be = to psw1
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1', message='Passwords must match'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')



# classes displayed on the modal windows
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')



class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
