from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from database.migration import Employer
from models.employers_models import UpdateEmployerForm
from utilities.utilities import get_db_session, get_employer_by_username, get_organization_by_employer
from messages.messages import LOGIN_REQUIRED, EMPLOYER_NOT_FOUND, USERNAME_ALREADY_IN_USE, EMAIL_ALREADY_IN_USE, DATA_UPDATED_SUCCESSFULLY, FAILED_TO_UPDATE_PERSONAL_DATA

def employer_home():
    # Visualizza la home page per l'employer corrente
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    session_db.close()
    return render_template('employer_home.html', employer=employer, organization=organization)

def employer_update_personal_data():
    # Gestisce l'aggiornamento dei dati personali dell'employer
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    form = UpdateEmployerForm()

    if request.method == 'GET':
        if not employer:
            flash(EMPLOYER_NOT_FOUND, 'error')
            return redirect(url_for('employer_home_route'))
        
        # Popola il modulo con i dati dell'employer
        form.name.data = employer.name
        form.surname.data = employer.surname
        form.email.data = employer.email
        form.username.data = employer.username
        form.password.data = employer.password
        form.confirm_password.data = employer.password
        
        return render_template('employer_update_personal_data.html', form=form, employer=employer)   
    
    if request.method == 'POST' and form.validate_on_submit():
        other_employers = session_db.query(Employer).filter(Employer.id != employer.id).all()

        # Verifica se il nome utente è già in uso
        if any(form.username.data.lower() == e.username for e in other_employers):
            flash(USERNAME_ALREADY_IN_USE, 'wrong_username')
            return render_template('employer_update_personal_data.html', form=form, employer=employer)

        # Verifica se l'email è già in uso
        if any(form.email.data.lower() == e.email for e in other_employers):
            flash(EMAIL_ALREADY_IN_USE, 'wrong_email')
            return render_template('employer_update_personal_data.html', form=form, employer=employer)

        if employer:
            # Aggiorna i dati dell'employer
            employer.name = form.name.data
            employer.surname = form.surname.data
            employer.email = form.email.data.lower()
            employer.username = form.username.data.lower()

            if form.password.data:
                employer.password = generate_password_hash(form.password.data)

            session_db.commit()
            session['username'] = employer.username  # Aggiorna l'username nella sessione
            flash(DATA_UPDATED_SUCCESSFULLY, 'success')
            return redirect(url_for('employer_home_route'))
    
        else:
            flash(FAILED_TO_UPDATE_PERSONAL_DATA, 'error')
            return redirect(url_for('employer_home_route'))
    
    return render_template('employer_update_personal_data.html', form=form, employer=employer)