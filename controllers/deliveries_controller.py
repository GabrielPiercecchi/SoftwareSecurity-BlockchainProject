from flask import render_template, session, redirect, url_for
from database.database import DBIsConnected
from database.migration import Product, Delivery, Organization, Employer

def employer_view_deliveries():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    
    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    deliveries = session_db.query(Delivery).filter_by(id_deliver_organization=organization.id).all()
    receivers = session_db.query(Delivery).filter_by(id_receiver_organization=organization.id).all()

    deliveries_with_orgs = []
    for delivery in deliveries:
        deliver_org = session_db.query(Organization).get(delivery.id_deliver_organization)
        receive_org = session_db.query(Organization).get(delivery.id_receiver_organization)
        carrier_org = session_db.query(Organization).get(delivery.id_carrier_organization)
        deliveries_with_orgs.append({
            'delivery': delivery,
            'deliver_org_name': deliver_org.name,
            'receive_org_name': receive_org.name,
            'carrier_org_name': carrier_org.name
        })

    receivers_with_orgs = []
    for receiver in receivers:
        deliver_org = session_db.query(Organization).get(receiver.id_deliver_organization)
        receive_org = session_db.query(Organization).get(receiver.id_receiver_organization)
        carrier_org = session_db.query(Organization).get(receiver.id_carrier_organization)
        receivers_with_orgs.append({
            'receiver': receiver,
            'deliver_org_name': deliver_org.name,
            'receive_org_name': receive_org.name,
            'carrier_org_name': carrier_org.name
        })

    return render_template('employer_view_deliveries.html', deliveries=deliveries_with_orgs, receivers=receivers_with_orgs, organization=organization)

def carrier_view_deliveries():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    carriers = session_db.query(Delivery).filter_by(id_carrier_organization=organization.id).all()

    carriers_with_orgs = []
    for carrier in carriers:
        deliver_org = session_db.query(Organization).get(carrier.id_deliver_organization)
        receive_org = session_db.query(Organization).get(carrier.id_receiver_organization)
        carrier_org = session_db.query(Organization).get(carrier.id_carrier_organization)
        carriers_with_orgs.append({
            'carrier': carrier,
            'deliver_org_name': deliver_org.name,
            'receive_org_name': receive_org.name,
            'carrier_org_name': carrier_org.name
        })


    return render_template('carrier_view_deliveries.html', carriers=carriers_with_orgs, organization=organization)
