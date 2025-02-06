import logging
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from database.migration import Employer, Organization
from models.auth_model import LoginForm, OrganizationForm, EmployerForm, AddEmployersForm
from controllers.ethereum_controller import assign_addresses_to_organizations
from algorithms.coins_algorithm import CoinsAlgorithm, initialize_organization_coins  # Importa la funzione per inizializzare i coins delle organizzazioni
from utilities.utilities import get_db_session, get_organization_by_id, get_employer_by_username, get_oracle_by_username, check_login_attempts, update_login_attempts, reset_login_attempts
from middlewares.validation import PhoneNumberValidator
from messages.messages import (
    LOGIN_ATTEMPTS_EXCEEDED, INVALID_USERNAME_OR_PASSWORD, ACCOUNT_NOT_ENABLED, LOGIN_ERROR,
    LOGOUT_SUCCESS, ORG_EMAIL_IN_USE, ORG_PARTITA_IVA_IN_USE, EMP_USERNAME_IN_USE, EMP_EMAIL_IN_USE,
    SIGNUP_SUCCESS, SIGNUP_ERROR, ADD_EMPLOYERS_USERNAME_IN_USE, ADD_EMPLOYERS_EMAIL_IN_USE,
    ADD_EMPLOYERS_SUCCESS, ADD_EMPLOYERS_ERROR, DUPLICATE_EMP_USERNAME, DUPLICATE_EMP_EMAIL
)

def login():
    if session.get('logged_in'):
        return redirect(url_for('home_route'))
    # Gestisce il login degli utenti
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data

        # Controlla i tentativi di login
        if not check_login_attempts(username):
            flash(LOGIN_ATTEMPTS_EXCEEDED, 'login_error')
            return render_template('login.html', form=form)

        session_db = get_db_session()

        try:
            oracle_user = get_oracle_by_username(session_db, username)
            employer = get_employer_by_username(session_db, username) if not oracle_user else None

            # Verifica le credenziali dell'utente
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
                    flash(ACCOUNT_NOT_ENABLED, 'login_error')
            else:
                flash(INVALID_USERNAME_OR_PASSWORD, 'login_error')
                update_login_attempts(username)
        except Exception as e:
            logging.error(f'Error during login: {e}')
            flash(LOGIN_ERROR, 'login_error')
        finally:
            session_db.close()

    return render_template('login.html', form=form)

def logout():
    # Gestisce il logout degli utenti
    session.clear()
    flash(LOGOUT_SUCCESS, 'success')
    return redirect(url_for('home_route'))

def signup_form():
    # Mostra il modulo di registrazione
    org_form = OrganizationForm()
    emp_form = EmployerForm()
    return render_template('signup.html', org_form=org_form, emp_form=emp_form)

def signup():
    if session.get('logged_in'):
        return redirect(url_for('home_route'))

    # Gestisce la registrazione di nuove organizzazioni e impiegati
    org_form = OrganizationForm(request.form)
    emp_form = EmployerForm(request.form)

    if request.method == 'POST' and org_form.validate_on_submit() and emp_form.validate_on_submit():
        session_db = get_db_session()
        manager = CoinsAlgorithm()

        try:
            other_organizations = session_db.query(Organization).all()
            other_emp = session_db.query(Employer).all()

            # Verifica se l'email o la partita IVA dell'organizzazione sono già in uso
            org_email_in_use = any(org_form.org_email.data.lower() == o.email.lower() for o in other_organizations)
            org_partita_iva_in_use = any(org_form.org_partita_iva.data == o.partita_iva for o in other_organizations)

            # Aggiungi tutti gli impiegati
            emp_usernames = [username.lower() for username in request.form.getlist('emp_username')]
            emp_passwords = request.form.getlist('emp_password')
            emp_names = request.form.getlist('emp_name')
            emp_surnames = request.form.getlist('emp_surname')
            emp_emails = [email.lower() for email in request.form.getlist('emp_email')]

            # Verifica se ci sono duplicati nella lista degli impiegati
            duplicate_emp_username = len(emp_usernames) != len(set(emp_usernames))
            duplicate_emp_email = len(emp_emails) != len(set(emp_emails))

            # Verifica se il nome utente o l'email dell'impiegato sono già in uso nel database
            emp_username_in_use = any(emp_username in [e.username.lower() for e in other_emp] for emp_username in emp_usernames)
            emp_email_in_use = any(emp_email in [e.email.lower() for e in other_emp] for emp_email in emp_emails)

            # Controllo unico per tutti gli errori
            if org_email_in_use:
                flash(ORG_EMAIL_IN_USE, 'wrong_org_email')
                return signup_form()
            if org_partita_iva_in_use:
                flash(ORG_PARTITA_IVA_IN_USE, 'wrong_org_partita_iva')
                return signup_form()
            if duplicate_emp_username:
                flash(DUPLICATE_EMP_USERNAME, 'wrong_emp_username')
                return signup_form()
            if duplicate_emp_email:
                flash(DUPLICATE_EMP_EMAIL, 'wrong_emp_email')
                return signup_form()
            if emp_username_in_use:
                flash(EMP_USERNAME_IN_USE, 'wrong_emp_username')
                return signup_form()
            if emp_email_in_use:
                flash(EMP_EMAIL_IN_USE, 'wrong_emp_email')
                return signup_form()

            # Crea una nuova organizzazione
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

            # Assegna indirizzi blockchain alle organizzazioni e inizializza i coin
            assign_addresses_to_organizations(session_db)
            initialize_organization_coins(manager, new_org)

            for i in range(len(emp_usernames)):
                new_emp = Employer(
                    username=emp_usernames[i],
                    password=generate_password_hash(emp_passwords[i]),
                    name=emp_names[i],
                    surname=emp_surnames[i],
                    email=emp_emails[i],
                    status='inactive',
                    id_organization=new_org.id
                )
                session_db.add(new_emp)

            session_db.commit()
            session_db.close()
            flash(SIGNUP_SUCCESS, 'success')
        except Exception as e:
            session_db.rollback()
            session_db.close()
            logging.error(f'Error during signup: {e}')
            flash(SIGNUP_ERROR, 'error')

        return redirect(url_for('home_route'))

    return signup_form()

def add_employers_to_existing_org():
    if session.get('logged_in'):
        return redirect(url_for('home_route'))

    # Aggiunge impiegati a un'organizzazione esistente
    session_db = get_db_session()
    organizations = session_db.query(Organization).all()
    session_db.close()

    form = AddEmployersForm()
    form.organization.choices = [(org.id, f"{org.id} - {org.name} - {org.type}") for org in organizations]

    if request.method == 'POST' and form.validate_on_submit():
        organization_id = form.organization.data
        emp_usernames = [username.lower() for username in request.form.getlist('emp_username')]
        emp_passwords = request.form.getlist('emp_password')
        emp_names = request.form.getlist('emp_name')
        emp_surnames = request.form.getlist('emp_surname')
        emp_emails = [email.lower() for email in request.form.getlist('emp_email')]

        # Verifica se ci sono duplicati nella lista degli impiegati
        if len(emp_usernames) != len(set(emp_usernames)):
            flash(DUPLICATE_EMP_USERNAME, 'wrong_emp_username')
            return render_template('add_employers.html', form=form, organizations=organizations)
        if len(emp_emails) != len(set(emp_emails)):
            flash(DUPLICATE_EMP_EMAIL, 'wrong_emp_email')
            return render_template('add_employers.html', form=form, organizations=organizations)

        session_db = get_db_session()

        try:
            other_emp = session_db.query(Employer).all()

            # Verifica se il nome utente o l'email dell'impiegato sono già in uso
            if any(emp_username in [e.username.lower() for e in other_emp] for emp_username in emp_usernames):
                flash(ADD_EMPLOYERS_USERNAME_IN_USE, 'wrong_emp_username')
                return render_template('add_employers.html', form=form, organizations=organizations)
            
            # Verifica se l'email dell'impiegato è già in uso
            if any(emp_email in [e.email.lower() for e in other_emp] for emp_email in emp_emails):
                flash(ADD_EMPLOYERS_EMAIL_IN_USE, 'wrong_emp_email')
                return render_template('add_employers.html', form=form, organizations=organizations)

            # Aggiungi i nuovi impiegati
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
            session_db.close()
            flash(ADD_EMPLOYERS_SUCCESS, 'success')
        except Exception as e:
            session_db.rollback()
            session_db.close()
            logging.error(f'Error during adding employers: {str(e)}')
            flash(ADD_EMPLOYERS_ERROR, 'error')

        return redirect(url_for('home_route'))

    return render_template('add_employers.html', form=form, organizations=organizations)

def permission_denied():
    # Mostra la pagina di permesso negato
    return render_template('permission_denied.html')