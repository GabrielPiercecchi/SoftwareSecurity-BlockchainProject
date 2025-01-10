from flask import render_template, request, redirect, url_for, flash, session
from database.database import DBIsConnected
from database.migration import Product, Delivery, Employer, Organization

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

def create_product():
    if request.method == 'POST':
        # Logica per creare un prodotto
        pass
    return render_template('create_product.html')

def update_product():
    if request.method == 'POST':
        # Logica per aggiornare un prodotto
        pass
    return render_template('update_product.html')

def view_products():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    products = session.query(Product).filter_by(owner_id=session['user_id']).all()
    session.close()
    return render_template('view_products.html', products=products)

def create_product_request():
    if request.method == 'POST':
        # Logica per creare una richiesta di prodotto
        pass
    return render_template('create_product_request.html')


#def manage_product_requests():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    requests = session.query(ProductRequest).filter_by(receiver_id=session['user_id']).all()
    session.close()
    return render_template('manage_product_requests.html', requests=requests)

def view_deliveries():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    deliveries = session.query(Delivery).filter_by(organization_id=session['user_id']).all()
    session.close()
    return render_template('view_deliveries.html', deliveries=deliveries)

def create_delivery():
    if request.method == 'POST':
        # Logica per creare una consegna
        pass
    return render_template('create_delivery.html')

