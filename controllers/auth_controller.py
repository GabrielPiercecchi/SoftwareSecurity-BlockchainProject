import logging
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from database.migration import Employer, Organization
from models.auth_model import LoginForm, OrganizationForm, EmployerForm, AddEmployersForm
from controllers.ethereum_controller import assign_addresses_to_organizations
from algorithms.coins_algorithm import CoinsAlgorithm, initialize_organization_coins  # Importa la funzione per inizializzare i coins delle organizzazioni
from utilities.utilities import get_db_session, get_organization_by_id, get_employer_by_username, get_oracle_by_username, check_login_attempts, update_login_attempts, reset_login_attempts
from messages.messages import (
    LOGIN_ATTEMPTS_EXCEEDED, INVALID_USERNAME_OR_PASSWORD, ACCOUNT_NOT_ENABLED, LOGIN_ERROR,
    LOGOUT_SUCCESS, ORG_EMAIL_IN_USE, ORG_PARTITA_IVA_IN_USE, EMP_USERNAME_IN_USE, EMP_EMAIL_IN_USE,
    SIGNUP_SUCCESS, SIGNUP_ERROR, ADD_EMPLOYERS_USERNAME_IN_USE, ADD_EMPLOYERS_EMAIL_IN_USE,
    ADD_EMPLOYERS_SUCCESS, ADD_EMPLOYERS_ERROR
)

def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data

        if not check_login_attempts(username):
            flash(LOGIN_ATTEMPTS_EXCEEDED, 'error')
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
                    flash(ACCOUNT_NOT_ENABLED, 'error')
            else:
                flash(INVALID_USERNAME_OR_PASSWORD, 'error')
                update_login_attempts(username)
        except Exception as e:
            logging.error(f'Error during login: {e}')
            flash(LOGIN_ERROR, 'error')
        finally:
            session_db.close()

    return render_template('login.html', form=form)

def logout():
    session.clear()
    flash(LOGOUT_SUCCESS, 'success')
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
        manager = CoinsAlgorithm()

        try:
            other_organizations = session_db.query(Organization).all()
            other_emp = session_db.query(Employer).all()

            if any(org_form.org_email.data.lower() == o.email.lower() for o in other_organizations):
                flash(ORG_EMAIL_IN_USE, 'wrong_org_email')
                return signup_form()
            
            if any(org_form.org_partita_iva.data == o.partita_iva for o in other_organizations):
                flash(ORG_PARTITA_IVA_IN_USE, 'wrong_org_partita_iva')
                return signup_form()

            if any(emp_form.emp_username.data.lower() == e.username.lower() for e in other_emp):
                flash(EMP_USERNAME_IN_USE, 'wrong_emp_username')
                return signup_form()
            
            if any(emp_form.emp_email.data.lower() == e.email.lower() for e in other_emp):
                flash(EMP_EMAIL_IN_USE, 'wrong_emp_email')
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
            initialize_organization_coins(manager, new_org)

            # Aggiungi tutti gli impiegati
            emp_usernames = request.form.getlist('emp_username')
            emp_passwords = request.form.getlist('emp_password')
            emp_names = request.form.getlist('emp_name')
            emp_surnames = request.form.getlist('emp_surname')
            emp_emails = request.form.getlist('emp_email')

            for i in range(len(emp_usernames)):
                new_emp = Employer(
                    username=emp_usernames[i],
                    password=generate_password_hash(emp_passwords[i]),
                    name=emp_names[i],
                    surname=emp_surnames[i],
                    email=emp_emails[i].lower(),
                    status='inactive',
                    id_organization=new_org.id
                )
                session_db.add(new_emp)

            session_db.commit()

            flash(SIGNUP_SUCCESS, 'success')
        except Exception as e:
            session_db.rollback()
            logging.error(f'Error during signup: {e}')
            flash(SIGNUP_ERROR, 'error')
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

    if request.method == 'POST' and form.validate_on_submit():
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
                flash(ADD_EMPLOYERS_USERNAME_IN_USE, 'wrong_emp_username')
                return render_template('add_employers.html', form=form, organizations=organizations)
            
            if any(emp_email.lower() in [e.email.lower() for e in other_emp] for emp_email in emp_emails):
                flash(ADD_EMPLOYERS_EMAIL_IN_USE, 'wrong_emp_email')
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
            flash(ADD_EMPLOYERS_SUCCESS, 'success')
        except Exception as e:
            session_db.rollback()
            logging.error(f'Error during adding employers: {str(e)}')
            flash(ADD_EMPLOYERS_ERROR, 'error')
        finally:
            session_db.close()

        return redirect(url_for('home_route'))

    return render_template('add_employers.html', form=form, organizations=organizations)

def permission_denied():
    return render_template('permission_denied.html')