from flask import render_template, session, redirect, url_for
from database.database import DBIsConnected
from database.migration import Product, Delivery, Organization, Employer, ProductRequest

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
        deliveries_with_orgs.append({
            'delivery': delivery,
            'deliver_org_name': deliver_org.name,
            'receive_org_name': receive_org.name
        })

    receivers_with_orgs = []
    for receiver in receivers:
        deliver_org = session_db.query(Organization).get(receiver.id_deliver_organization)
        receive_org = session_db.query(Organization).get(receiver.id_receiver_organization)
        receivers_with_orgs.append({
            'receiver': receiver,
            'deliver_org_name': deliver_org.name,
            'receive_org_name': receive_org.name
        })
    session_db.close()

    return render_template('employer_view_deliveries.html', deliveries=deliveries_with_orgs, receivers=receivers_with_orgs, organization=organization)

def view_product_requests():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    
    providing_product_requests = session_db.query(ProductRequest).filter_by(id_providing_organization=organization.id).all()
    requesting_product_requests = session_db.query(ProductRequest).filter_by(id_requesting_organization=organization.id).all()
    
    providing_requests_with_details = []
    for request in providing_product_requests:
        product = session_db.query(Product).get(request.id_product)
        requesting_org = session_db.query(Organization).get(request.id_requesting_organization)
        providing_requests_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': organization.name
        })
    
    requesting_requests_with_details = []
    for request in requesting_product_requests:
        product = session_db.query(Product).get(request.id_product)
        providing_org = session_db.query(Organization).get(request.id_providing_organization)
        requesting_requests_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': organization.name,
            'providing_org_name': providing_org.name
        })
    
    session_db.close()

    return render_template('employer_view_product_requests.html', organization=organization, providing_product_requests=providing_requests_with_details, requesting_product_requests=requesting_requests_with_details)
