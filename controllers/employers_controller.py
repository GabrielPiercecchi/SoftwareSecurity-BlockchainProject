from typing import NotRequired
from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash
from database.database import DBIsConnected
from database.migration import Employer, Organization

class UpdateEmployerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    surname = StringField('Surname', validators=[DataRequired()], render_kw={"placeholder": "Surname"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match' )], render_kw={"placeholder": "Confirm Password"})


def employer_home():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    session_db.close()
    return render_template('employer_home.html', employer=employer, organization=organization)



def employer_update_personal_data():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    employer = session_db.query(Employer).filter_by(username=username).first()
    session_db.close()


    form = UpdateEmployerForm()
    
    if request.method == 'GET':

        if not employer:
            session_db.close()
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
        employer = session_db.query(Employer).filter_by(username=username).first()
        other_employers = session_db.query(Employer).filter(Employer.id != employer.id).all()

        if any(form.username.data == e.username for e in other_employers):
            flash('Username already in use', 'wrong_username')
            session_db.close()
            return render_template('employer_update_personal_data.html', form=form, employer=employer)

        if  any(form.email.data == e.email for e in other_employers):
            flash('Email already in use', 'wrong_email')
            session_db.close()
            return render_template('employer_update_personal_data.html', form=form, employer=employer)


        if employer:
            employer.name = form.name.data
            employer.surname = form.surname.data
            employer.email = form.email.data
            employer.username = form.username.data

            if form.password.data:
                employer.password = generate_password_hash(form.password.data)


            session_db.commit()
            session['username'] = employer.username  # Aggiorna l'username nella sessione
            session_db.close()
            print('Data updated successfully!', 'success')
            return redirect(url_for('employer_home_route'))
    
        else:
            session_db.close()
            print('Failed to update personal data.', 'error')
            return redirect(url_for('employer_home_route'))
    
    return render_template('employer_update_personal_data.html', form=form, employer=employer)