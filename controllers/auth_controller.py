import logging
from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import check_password_hash, generate_password_hash
from database.migration import Employer, Organization
from controllers.ethereum_controller import assign_addresses_to_organizations
from algorithms.coins_algorithm import CoinsAlgorithm, initialize_organization_coins  # Importa la funzione per inizializzare i coins delle organizzazioni
from middlewares.validation import LengthValidator
from utilities.utilities import get_db_session, get_organization_by_id, get_employer_by_username, get_oracle_by_username, check_login_attempts, update_login_attempts, reset_login_attempts

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'), 
        LengthValidator(max_length=50, message='Username must be less than 50 characters')
    ], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'), 
        LengthValidator(max_length=162, message='Password must be less than 162 characters')
    ], render_kw={"placeholder": "Password"})

class OrganizationForm(FlaskForm):
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

def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data

        if not check_login_attempts(username):
            flash('Too many login attempts. Please try again in 30 seconds.', 'error')
            return render_template('login.html', form=form)

        session_db = get_db_session()

        try:
            oracle_user = get_oracle_by_username(session_db, username)
            employer = get_employer_by_username(session_db, username) if not oracle_user else None

            if ((oracle_user and check_password_hash(oracle_user.password, password)) or
                (employer and check_password_hash(employer.password, password))):
                if oracle_user or (employer and employer.status == 'active'):
                    session['logged_in'] = True
                    session['username'] = username

                    if employer:
                        session['user_type'] = 'employer'
                        session['user_org_id'] = employer.id_organization
                        session['user_org_type'] = get_organization_by_id(session_db, employer.id_organization).type
                    else:
                        session['user_type'] = 'oracle'

                    reset_login_attempts(username)
                    return redirect(url_for('home_route'))
                else:
                    flash('Account not yet enabled', 'error')
            else:
                flash('Invalid username or password', 'error')
                update_login_attempts(username)
        except Exception as e:
            logging.error(f'Error during login: {e}')
            flash('An error occurred during login. Please try again later.', 'error')
        finally:
            session_db.close()

    return render_template('login.html', form=form)

def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home_route'))

def signup_form():
    org_form = OrganizationForm()
    emp_form = EmployerForm()
    return render_template('signup.html', org_form=org_form, emp_form=emp_form)

def signup():
    org_form = OrganizationForm(request.form)
    emp_form = EmployerForm(request.form)

    if request.method == 'POST' and org_form.validate_on_submit() and emp_form.validate_on_submit():
        session_db = get_db_session()
        menager = CoinsAlgorithm()

        try:
            other_organizations = session_db.query(Organization).all()
            other_emp = session_db.query(Employer).all()

            if any(org_form.org_email.data.lower() == o.email.lower() for o in other_organizations):
                flash('Organization email already in use', 'wrong_org_email')
                return signup_form()
            
            if any(org_form.org_partita_iva.data == o.partita_iva for o in other_organizations):
                flash('Partita IVA already in use', 'wrong_org_partita_iva')
                return signup_form()

            if any(emp_form.emp_username.data.lower() == e.username.lower() for e in other_emp):
                flash('Username already in use', 'wrong_emp_username')
                return signup_form()
            
            if any(emp_form.emp_email.data.lower() == e.email.lower() for e in other_emp):
                flash('Email already in use', 'wrong_emp_email')
                return signup_form()

            new_org = Organization(
                name=org_form.org_name.data,
                email=org_form.org_email.data.lower(),
                address=org_form.org_address.data,
                city=org_form.org_city.data,
                cap=org_form.org_cap.data,
                telephone=org_form.org_telephone.data,
                partita_iva=org_form.org_partita_iva.data,
                ragione_sociale=org_form.org_ragione_sociale.data,
                type=org_form.org_type.data,
                description=org_form.org_description.data,
            )
            session_db.add(new_org)
            session_db.commit()

            assign_addresses_to_organizations(session_db)
            initialize_organization_coins(menager, new_org)

            new_emp = Employer(
                username=emp_form.emp_username.data,
                password=generate_password_hash(emp_form.emp_password.data),
                name=emp_form.emp_name.data,
                surname=emp_form.emp_surname.data,
                email=emp_form.emp_email.data.lower(),
                status='inactive',
                id_organization=new_org.id
            )
            session_db.add(new_emp)
            session_db.commit()

            flash('Signup process completed successfully.', 'success')
        except Exception as e:
            session_db.rollback()
            logging.error(f'Error during signup: {e}')
            flash('An error occurred during signup. Please try again later.', 'error')
        finally:
            session_db.close()

        return redirect(url_for('home_route'))

    return signup_form()

def add_employers_to_existing_org():
    session_db = get_db_session()
    organizations = session_db.query(Organization).all()
    session_db.close()

    form = AddEmployersForm()
    form.organization.choices = [(org.id, f"{org.id} - {org.name} - {org.type}") for org in organizations]

    if request.method == 'POST' and form.validate():
        organization_id = form.organization.data
        emp_usernames = request.form.getlist('emp_username')
        emp_passwords = request.form.getlist('emp_password')
        emp_names = request.form.getlist('emp_name')
        emp_surnames = request.form.getlist('emp_surname')
        emp_emails = request.form.getlist('emp_email')

        session_db = get_db_session()

        try:
            other_emp = session_db.query(Employer).all()

            if any(emp_username.lower() in [e.username.lower() for e in other_emp] for emp_username in emp_usernames):
                flash('Username already in use', 'wrong_emp_username')
                return render_template('add_employers.html', form=form, organizations=organizations)
            
            if any(emp_email.lower() in [e.email.lower() for e in other_emp] for emp_email in emp_emails):
                flash('Email already in use', 'wrong_emp_email')
                return render_template('add_employers.html', form=form, organizations=organizations)

            for i in range(len(emp_usernames)):
                new_emp = Employer(
                    username=emp_usernames[i],
                    password=generate_password_hash(emp_passwords[i]),
                    name=emp_names[i],
                    surname=emp_surnames[i],
                    email=emp_emails[i],
                    id_organization=organization_id
                )
                session_db.add(new_emp)
            
            session_db.commit()
            flash('Employers added successfully!', 'success')
        except Exception as e:
            session_db.rollback()
            logging.error(f'Error during adding employers: {str(e)}')
            flash('An error occurred while adding employers. Please try again later.', 'error')
        finally:
            session_db.close()

        return redirect(url_for('home_route'))

    return render_template('add_employers.html', form=form, organizations=organizations)

def permission_denied():
    return render_template('permission_denied.html')