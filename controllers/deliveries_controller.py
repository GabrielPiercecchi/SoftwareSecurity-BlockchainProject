from flask import render_template, session, redirect, url_for, flash
from database.migration import Delivery
from utilities.utilities import get_db_session, get_employer_by_username, get_organization_by_employer, get_delivery_details
from messages.messages import LOGIN_REQUIRED

def employer_view_deliveries():
    # Visualizza le consegne per l'organizzazione dell'utente corrente (employer)
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()
    
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    
    # Ottiene le consegne effettuate e ricevute dall'organizzazione
    deliveries = session_db.query(Delivery).filter_by(id_deliver_organization=organization.id).all()
    receivers = session_db.query(Delivery).filter_by(id_receiver_organization=organization.id).all()

    # Ottiene i dettagli delle consegne
    deliveries_with_orgs = [get_delivery_details(session_db, delivery) for delivery in deliveries]
    receivers_with_orgs = [get_delivery_details(session_db, receiver) for receiver in receivers]

    return render_template('employer_view_deliveries.html', deliveries=deliveries_with_orgs, receivers=receivers_with_orgs, organization=organization)

def carrier_view_deliveries():
    # Visualizza le consegne per l'organizzazione dell'utente corrente (carrier)
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()

    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    
    # Ottiene le consegne effettuate dall'organizzazione come carrier
    carriers = session_db.query(Delivery).filter_by(id_carrier_organization=organization.id).all()

    # Ottiene i dettagli delle consegne
    carriers_with_orgs = [get_delivery_details(session_db, carrier) for carrier in carriers]

    return render_template('carrier_view_deliveries.html', carriers=carriers_with_orgs, organization=organization)