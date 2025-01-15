from flask import render_template, session, redirect, url_for, flash, request, jsonify
from datetime import datetime
from wtforms import StringField, RadioField, TextAreaField, IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from database.database import DBIsConnected
from database.migration import Product, Organization, Employer, ProductRequest, Delivery, Type
from algorithms.coins_algorithm import coins_algorithm

class CreateProductRequestForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])

class DenyProductRequestForm(FlaskForm):
    rejectedButton = SubmitField('Reject Request')

class AcceptProductRequestForm(FlaskForm):
    carrier_id = SelectField('Carrier Organization', choices=[], validators=[DataRequired()])
    acceptButton = SubmitField('Accept Request')

class CarrierAcceptRequestAndCreateDEliveryForm(FlaskForm):
    co2_emission = FloatField('CO2 Emission', validators=[DataRequired()])
    acceptButton = SubmitField('Accept Request')

def menage_product_requests():
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
        carrier_org = session_db.query(Organization).get(request.id_carrier_organization)
        if carrier_org:
            carrier_org_name = carrier_org.name
        else:
            carrier_org_name = "TBD"
        providing_requests_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': organization.name,
            'carrier_org_name': carrier_org_name
        })
    
    requesting_requests_with_details = []
    for request in requesting_product_requests:
        product = session_db.query(Product).get(request.id_product)
        providing_org = session_db.query(Organization).get(request.id_providing_organization)
        carrier_org = session_db.query(Organization).get(request.id_carrier_organization)
        if carrier_org:
            carrier_org_name = carrier_org.name
        else:
            carrier_org_name = "TBD"
        requesting_requests_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': organization.name,
            'providing_org_name': providing_org.name,
            'carrier_org_name': carrier_org_name
        })

    carriers = session_db.query(Organization).filter_by(type='carrier').all()
    
    session_db.close()
    form=DenyProductRequestForm()

    return render_template('employer_menage_product_requests.html', organization=organization, 
                           providing_product_requests=providing_requests_with_details, 
                           requesting_product_requests=requesting_requests_with_details, carriers=carriers, form=form)

def view_other_products():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    employer = session_db.query(Employer).filter_by(username=username).first()

    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()

    # Retrieve products from other organizations
    other_products = session_db.query(Product).filter(Product.id_organization != organization.id).all()
    other_organizations = session_db.query(Organization).filter(Organization.id != organization.id).all()
    
    products_with_org = []
    for product in other_products:
        org = session_db.query(Organization).get(product.id_organization)
        products_with_org.append({
            'product': product,
            'organization_name': org.name
        })

    session_db.close()

    return render_template('employer_view_other_products.html', products=products_with_org, organizations=other_organizations)

def create_product_requests(product_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    
    form = CreateProductRequestForm()

    if request.method == 'GET':
        product = session_db.query(Product).get(product_id)
        if not product:
            session_db.close()
            flash('Product not found.', 'danger')
            return redirect(url_for('view_other_products'))

        org = session_db.query(Organization).get(product.id_organization)
        product_with_org = {
            'product': product,
            'organization_name': org.name
        }

        form.quantity.data = product.quantity

        session_db.close()
        return render_template('employer_create_product_requests.html', form=form, product=product_with_org)
    
    if request.method == 'POST' and form.validate_on_submit():
        quantity = form.quantity.data

        employer = session_db.query(Employer).filter_by(username=username).first()
        organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
        
        product = session_db.query(Product).get(product_id)
        
        if quantity > product.quantity:
            flash('Requested quantity exceeds available quantity.', 'danger')
            product_with_org = {
                'product': product,
                'organization_name': organization.name
            }
            session_db.close()
            return render_template('employer_create_product_requests.html', form=form, product=product_with_org)

        new_request = ProductRequest(
            id_product=product_id,
            id_requesting_organization=organization.id,
            id_providing_organization=product.id_organization,
            quantity=quantity,
            status='pending',
        )

        session_db.add(new_request)
        session_db.commit()
        session_db.close()
        flash('Failed to update product.', 'error')

        return redirect(url_for('menage_product_requests_route'))
    
    session_db.close()
    return render_template('employer_create_product_requests.html', form=form, product=product_with_org)

def deny_product_request():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    request_id = request.form.get('request_id')
    if not request_id:
        print('Request ID is required')
        flash('Request ID is required', 'error')
        return redirect(url_for('menage_product_requests_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    
    try:
        product_request = session_db.query(ProductRequest).get(request_id)
        if not product_request:
            print('Product request not found')
            flash('Product request not found', 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        product_request.status = 'rejected'
        product_request.date_responded = datetime.now()
        session_db.commit()
        print('Product request denied successfully')
        flash('Product request denied successfully', 'success')
    except Exception as e:
        session_db.rollback()
        print(f'Error: {str(e)}')
        flash(f'Error: {str(e)}', 'error')
    finally:
        session_db.close()
    
    return redirect(url_for('menage_product_requests_route'))

def accept_product_request():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    request_id = request.form.get('request_id')
    carrier_id = request.form.get('carrier_id')
    if not request_id or not carrier_id:
        print('Request ID and Carrier ID are required')
        flash('Request ID and Carrier ID are required', 'error')
        return redirect(url_for('menage_product_requests_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    
    try:
        product_request = session_db.query(ProductRequest).get(request_id)
        if not product_request:
            print('Product request not found')
            flash('Product request not found', 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        product = session_db.query(Product).get(product_request.id_product)
        if not product:
            print('Product not found')
            flash('Product not found', 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        if product.quantity < product_request.quantity:
            print('Insufficient product quantity')
            flash('Insufficient product quantity', 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        product.quantity -= product_request.quantity
        
        product_request.status = 'approved'
        product_request.id_carrier_organization = carrier_id
        product_request.date_responded = datetime.now()
        session_db.commit()
        print('Product request accepted successfully')
        flash('Product request accepted successfully', 'success')
    except Exception as e:
        session_db.rollback()
        print(f'Error: {str(e)}')
        flash(f'Error: {str(e)}', 'error')
    finally:
        session_db.close()
    
    return redirect(url_for('menage_product_requests_route'))

def carrier_menage_product_requests():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    carring_product_request = session_db.query(ProductRequest).filter_by(id_carrier_organization=organization.id).all()

    carring_request_with_details = []
    for request in carring_product_request:
        product = session_db.query(Product).get(request.id_product)
        requesting_org = session_db.query(Organization).get(request.id_requesting_organization)
        providing_org = session_db.query(Organization).get(request.id_providing_organization)
        carring_request_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': providing_org.name,
            'carrier_org_name': organization.name,
        })
    
    session_db.close()
    form=CarrierAcceptRequestAndCreateDEliveryForm()

    return render_template('carrier_menage_product_requests.html', organization=organization, 
                           carring_product_request=carring_request_with_details, form=form)

def carrier_accept_and_create_delivery():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    request_id = request.form.get('request_id')
    co2_emission = float(request.form.get('co2_emission'))
    if not request_id or not co2_emission:
        print('Request ID and CO2 Emission are required')
        flash('Request ID and CO2 Emission are required', 'error')
        return redirect(url_for('carrier_menage_product_requests_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    
    try:
        product_request = session_db.query(ProductRequest).filter_by(id=request_id).first()
        if not product_request:
            print('Product request not found')
            flash('Product request not found', 'error')
            return redirect(url_for('carrier_menage_product_requests_route'))
        
        organization = session_db.query(Organization).filter_by(id=product_request.id_carrier_organization).first()
        default_co2_value = session_db.query(Type).filter_by(id_type=organization.type).first().default_co2_value
        co2_standard = session_db.query(Type).filter_by(id_type=organization.type).first().standard
        co2_limit = default_co2_value + co2_standard*product_request.quantity

        if not coins_algorithm(co2_emission, co2_limit, organization, session_db):
            session_db.rollback()
            print('CO2 emission exceeds the limit')
            return redirect(url_for('carrier_menage_product_requests_route'))

        delivery = Delivery(
            id_product=product_request.id_product,
            quantity=product_request.quantity,
            co2_emission=co2_emission,
            id_deliver_organization=product_request.id_providing_organization,
            id_receiver_organization=product_request.id_requesting_organization,
            id_carrier_organization=product_request.id_carrier_organization,
            date_timestamp=datetime.now()
        )
        
        session_db.add(delivery)
        product_request.status_delivery = 'delivered'
        session_db.commit()
        print('Delivery created successfully')
        flash('Delivery created successfully', 'success')
        session_db.close()
    except Exception as e:
        session_db.rollback()
        print(f'Error: {str(e)}')
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('carrier_menage_product_requests_route'))
    
    return redirect(url_for('carrier_menage_product_requests_route'))