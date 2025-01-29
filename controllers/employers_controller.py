from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash
from database.migration import Employer
from middlewares.validation import LengthValidator
from utilities.utilities import get_db_session, get_employer_by_username, get_organization_by_employer

class UpdateEmployerForm(FlaskForm):
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


def employer_home():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    session_db.close()
    return render_template('employer_home.html', employer=employer, organization=organization)


def employer_update_personal_data():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    form = UpdateEmployerForm()

    if request.method == 'GET':
        if not employer:
            flash('Employer not found.', 'error')
            return redirect(url_for('employer_home_route'))
        
        # Populate the form with the employer data
        form.name.data = employer.name
        form.surname.data = employer.surname
        form.email.data = employer.email
        form.username.data = employer.username
        form.password.data = employer.password
        form.confirm_password.data = employer.password
        
        return render_template('employer_update_personal_data.html', form=form, employer=employer)   
    
    if request.method == 'POST' and form.validate_on_submit():
        other_employers = session_db.query(Employer).filter(Employer.id != employer.id).all()

        if any(form.username.data.lower() == e.username for e in other_employers):
            flash('Username already in use', 'wrong_username')
            return render_template('employer_update_personal_data.html', form=form, employer=employer)

        if any(form.email.data.lower() == e.email for e in other_employers):
            flash('Email already in use', 'wrong_email')
            return render_template('employer_update_personal_data.html', form=form, employer=employer)

        if employer:
            employer.name = form.name.data
            employer.surname = form.surname.data
            employer.email = form.email.data.lower()
            employer.username = form.username.data.lower()

            if form.password.data:
                employer.password = generate_password_hash(form.password.data)

            session_db.commit()
            session['username'] = employer.username  # Aggiorna l'username nella sessione
            flash('Data updated successfully!', 'success')
            return redirect(url_for('employer_home_route'))
    
        else:
            flash('Failed to update personal data.', 'error')
            return redirect(url_for('employer_home_route'))
    
    return render_template('employer_update_personal_data.html', form=form, employer=employer)