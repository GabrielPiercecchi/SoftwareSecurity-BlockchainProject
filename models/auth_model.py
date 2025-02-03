from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from middlewares.validation import LengthValidator

class LoginForm(FlaskForm):
    # Form per il login
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'), 
        LengthValidator(max_length=50, message='Username must be less than 50 characters')
    ], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'), 
        LengthValidator(max_length=162, message='Password must be less than 162 characters')
    ], render_kw={"placeholder": "Password"})

class OrganizationForm(FlaskForm):
    # Form per la registrazione di una nuova organizzazione
    org_name = StringField('Organization Name', validators=[
        DataRequired(message='Organization Name is required'), 
        LengthValidator(max_length=100, message='Organization Name must be less than 100 characters')
    ], render_kw={"placeholder": "Organization Name"})
    org_email = StringField('Organization Email', validators=[
        DataRequired(message='Organization Email is required'), 
        Email(message='Invalid email address'), 
        LengthValidator(max_length=100, message='Organization Email must be less than 100 characters')
    ], render_kw={"placeholder": "Organization@Email"})
    org_address = StringField('Address', validators=[
        DataRequired(message='Address is required'), 
        LengthValidator(max_length=255, message='Address must be less than 255 characters')
    ], render_kw={"placeholder": "Address"})
    org_city = StringField('City', validators=[
        DataRequired(message='City is required'), 
        LengthValidator(max_length=100, message='City must be less than 100 characters')
    ], render_kw={"placeholder": "City"})
    org_cap = StringField('CAP', validators=[
        DataRequired(message='CAP is required'), 
        LengthValidator(max_length=10, message='CAP must be less than 10 characters')
    ], render_kw={"placeholder": "CAP"})
    org_telephone = StringField('Telephone', validators=[
        DataRequired(message='Telephone is required'), 
        LengthValidator(max_length=20, message='Telephone must be less than 20 characters')
    ], render_kw={"placeholder": "Telephone"})
    org_partita_iva = StringField('Partita IVA', validators=[
        DataRequired(message='Partita IVA is required'), 
        LengthValidator(max_length=20, message='Partita IVA must be less than 20 characters')
    ], render_kw={"placeholder": "Partita IVA"})
    org_ragione_sociale = StringField('Ragione Sociale', validators=[
        DataRequired(message='Ragione Sociale is required'), 
        LengthValidator(max_length=100, message='Ragione Sociale must be less than 100 characters')
    ], render_kw={"placeholder": "Ragione Sociale"})
    org_type = RadioField('Type', choices=[
        ('farmer', 'Farmer'), 
        ('seller', 'Seller'), 
        ('producer', 'Producer'), 
        ('carrier', 'Carrier')
    ], validators=[DataRequired(message='Type is required')], default='farmer')
    org_description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'), 
        LengthValidator(max_length=255, message='Description must be less than 255 characters')
    ], render_kw={"placeholder": "Description"})

class EmployerForm(FlaskForm):
    # Form per la registrazione di un nuovo employer
    emp_username = StringField('Username', validators=[
        DataRequired(message='Username is required'), 
        LengthValidator(max_length=50, message='Username must be less than 50 characters')
    ], render_kw={"placeholder": "Username"})
    emp_password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'), 
        LengthValidator(max_length=162, message='Password must be less than 162 characters')
    ], render_kw={"placeholder": "Password"})
    emp_confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Confirm Password is required'), 
        EqualTo('emp_password', message='Passwords must match'), 
        LengthValidator(max_length=162, message='Confirm Password must be less than 162 characters')
    ], render_kw={"placeholder": "Confirm Password"})
    emp_name = StringField('Name', validators=[
        DataRequired(message='Name is required'), 
        LengthValidator(max_length=50, message='Name must be less than 50 characters')
    ], render_kw={"placeholder": "Name"})
    emp_surname = StringField('Surname', validators=[
        DataRequired(message='Surname is required'), 
        LengthValidator(max_length=50, message='Surname must be less than 50 characters')
    ], render_kw={"placeholder": "Surname"})
    emp_email = StringField('Email', validators=[
        DataRequired(message='Email is required'), 
        Email(message='Invalid email address'), 
        LengthValidator(max_length=100, message='Email must be less than 100 characters')
    ], render_kw={"placeholder": "Employer@Email"})

class AddEmployersForm(FlaskForm):
    # Form per aggiungere employer a un'organizzazione esistente
    organization = SelectField('Organization', choices=[], validators=[DataRequired(message='Organization is required')])
    emp_username = StringField('Username', validators=[
        DataRequired(message='Username is required'), 
        LengthValidator(max_length=50, message='Username must be less than 50 characters')
    ], render_kw={"placeholder": "Username"})
    emp_password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'), 
        LengthValidator(max_length=162, message='Password must be less than 162 characters')
    ], render_kw={"placeholder": "Password"})
    emp_confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Confirm Password is required'), 
        EqualTo('emp_password', message='Passwords must match'), 
        LengthValidator(max_length=162, message='Confirm Password must be less than 162 characters')
    ], render_kw={"placeholder": "Confirm Password"})
    emp_name = StringField('Name', validators=[
        DataRequired(message='Name is required'), 
        LengthValidator(max_length=50, message='Name must be less than 50 characters')
    ], render_kw={"placeholder": "Name"})
    emp_surname = StringField('Surname', validators=[
        DataRequired(message='Surname is required'), 
        LengthValidator(max_length=50, message='Surname must be less than 50 characters')
    ], render_kw={"placeholder": "Surname"})
    emp_email = StringField('Email', validators=[
        DataRequired(message='Email is required'), 
        Email(message='Invalid email address'), 
        LengthValidator(max_length=100, message='Email must be less than 100 characters')
    ], render_kw={"placeholder": "Employer@Email"})