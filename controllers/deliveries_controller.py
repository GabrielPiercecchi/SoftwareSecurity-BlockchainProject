from flask import render_template, session, redirect, url_for
from database.database import DBIsConnected
from database.migration import Product, Delivery, Organization, Employer
from utilities.utilities import get_db_session, get_employer_by_username, get_organization_by_employer, get_delivery_details

def employer_view_deliveries():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()
    
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    deliveries = session_db.query(Delivery).filter_by(id_deliver_organization=organization.id).all()
    receivers = session_db.query(Delivery).filter_by(id_receiver_organization=organization.id).all()

    deliveries_with_orgs = [get_delivery_details(session_db, delivery) for delivery in deliveries]
    receivers_with_orgs = [get_delivery_details(session_db, receiver) for receiver in receivers]

    return render_template('employer_view_deliveries.html', deliveries=deliveries_with_orgs, receivers=receivers_with_orgs, organization=organization)

def carrier_view_deliveries():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()

    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    carriers = session_db.query(Delivery).filter_by(id_carrier_organization=organization.id).all()

    carriers_with_orgs = [get_delivery_details(session_db, carrier) for carrier in carriers]

    return render_template('carrier_view_deliveries.html', carriers=carriers_with_orgs, organization=organization)
