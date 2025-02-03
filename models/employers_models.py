from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo
from middlewares.validation import LengthValidator

class UpdateEmployerForm(FlaskForm):
    # Form per l'aggiornamento dei dati di un employer
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'), 
        LengthValidator(max_length=50, message='Name must be less than 50 characters')
    ], render_kw={"placeholder": "Name"})
    surname = StringField('Surname', validators=[
        DataRequired(message='Surname is required'), 
        LengthValidator(max_length=50, message='Surname must be less than 50 characters')
    ], render_kw={"placeholder": "Surname"})
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'), 
        Email(message='Invalid email address'), 
        LengthValidator(max_length=100, message='Email must be less than 100 characters')
    ], render_kw={"placeholder": "Email"})
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'), 
        LengthValidator(max_length=50, message='Username must be less than 50 characters')
    ], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'), 
        LengthValidator(max_length=128, message='Password must be less than 128 characters')
    ], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Confirm Password is required'), 
        EqualTo('password', message='Passwords must match'), 
        LengthValidator(max_length=128, message='Confirm Password must be less than 128 characters'),
    ], render_kw={"placeholder": "Confirm Password"})