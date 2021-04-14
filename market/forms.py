from flask_wtf import FlaskForm
# I need to import the fields I'm going to need
from wtforms import StringField, PasswordField, SubmitField
# to add form validations
from wtforms.validators import Length, EqualTo, Email, DataRequired #, email_validator


# Register form
class RegisterForm(FlaskForm):
    # to be able to use validators, I need to import wtforms. If I want to add more than 1 validator, then add []
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    # I don't need to add the validator to psw2 bc it must be = to psw1
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1', message='Passwords must match'), DataRequired()])
    submit = SubmitField(label='Create Account')
