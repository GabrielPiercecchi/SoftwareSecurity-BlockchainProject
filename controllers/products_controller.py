from flask import render_template, session, redirect, url_for
from database.database import DBIsConnected
from database.migration import Product, Delivery, Organization, Employer

def product_detail(id):
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    product = session.query(Product).get(id)
    deliveries = session.query(Delivery).filter_by(id_product=id).all()
    organization = session.query(Organization).get(product.id_organization)
    
    deliveries_with_orgs = []
    for delivery in deliveries:
        deliver_org = session.query(Organization).get(delivery.id_deliver_organization)
        receive_org = session.query(Organization).get(delivery.id_receiver_organization)
        deliveries_with_orgs.append({
            'delivery': delivery,
            'deliver_org_name': deliver_org.name,
            'receive_org_name': receive_org.name
        })
    
    session.close()
    return render_template("product_detail.html", product=product, deliveries=deliveries_with_orgs, organization=organization)

def get_all_products():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    products = session.query(Product).all()
    products_with_org = []
    for product in products:
        organization = session.query(Organization).get(product.id_organization)
        products_with_org.append({
            'product': product,
            'organization_name': organization.name
        })
    session.close()
    return render_template("products.html", products=products_with_org)

def employer_view_products():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    products = session_db.query(Product).filter_by(id_organization=organization.id).all()
    session_db.close()
    return render_template('employer_view_products.html', products=products, organization=organization)
