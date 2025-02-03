from flask import render_template, session, redirect, url_for, flash, request
from datetime import datetime
import logging
from database.migration import Product, Organization, ProductRequest, Delivery, Type
from algorithms.coins_algorithm import coins_algorithm
from models.product_requests_model import CreateProductRequestForm, DenyProductRequestForm, CarrierAcceptRequestAndCreateDeliveryForm
from utilities.utilities import get_db_session, get_organization_by_id, get_employer_by_username, get_organization_by_employer, get_product_by_id
from messages.messages import (
    LOGIN_REQUIRED, PRODUCT_NOT_FOUND, UNAUTHORIZED_ACCESS, REQUESTED_QUANTITY_EXCEEDS_AVAILABLE,
    PRODUCT_REQUEST_CREATED_SUCCESSFULLY, REQUEST_ID_REQUIRED, PRODUCT_REQUEST_NOT_FOUND,
    PRODUCT_REQUEST_DENIED_SUCCESSFULLY, INSUFFICIENT_PRODUCT_QUANTITY, PRODUCT_REQUEST_ACCEPTED_SUCCESSFULLY,
    DELIVERY_CREATED_SUCCESSFULLY, ERROR_OCCURRED
)

def menage_product_requests():
    # Gestisce le richieste di prodotti
    username = session.get('username')
    if not username:
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    
    # Ottiene le richieste di prodotti fornite e richieste dall'organizzazione
    providing_product_requests = session_db.query(ProductRequest).filter_by(id_providing_organization=organization.id).all()
    requesting_product_requests = session_db.query(ProductRequest).filter_by(id_requesting_organization=organization.id).all()
    
    providing_requests_with_details = []
    for request in providing_product_requests:
        product = get_product_by_id(session_db, request.id_product)
        requesting_org = get_organization_by_id(session_db, request.id_requesting_organization)
        carrier_org = get_organization_by_id(session_db, request.id_carrier_organization)
        carrier_org_name = carrier_org.name if carrier_org else "TBD"
        providing_requests_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': organization.name,
            'carrier_org_name': carrier_org_name
        })
    
    requesting_requests_with_details = []
    for request in requesting_product_requests:
        product = get_product_by_id(session_db, request.id_product)
        providing_org = get_organization_by_id(session_db, request.id_providing_organization)
        carrier_org = get_organization_by_id(session_db, request.id_carrier_organization)
        carrier_org_name = carrier_org.name if carrier_org else "TBD"
        requesting_requests_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': organization.name,
            'providing_org_name': providing_org.name,
            'carrier_org_name': carrier_org_name
        })

    carriers = session_db.query(Organization).filter_by(type='carrier').all()
    
    session_db.close()
    form = DenyProductRequestForm()

    return render_template('employer_menage_product_requests.html', organization=organization, 
        providing_product_requests=providing_requests_with_details, 
        requesting_product_requests=requesting_requests_with_details, carriers=carriers, form=form)

def view_other_products():
    # Visualizza i prodotti di altre organizzazioni
    username = session.get('username')
    if not username:
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)

    # Recupera i prodotti di altre organizzazioni
    other_products = session_db.query(Product).filter(Product.id_organization != organization.id).all()
    other_organizations = session_db.query(Organization).filter(Organization.id != organization.id).all()
    
    products_with_org = []
    for product in other_products:
        org = get_organization_by_id(session_db, product.id_organization)
        products_with_org.append({
            'product': product,
            'organization_name': org.name
        })

    session_db.close()

    return render_template('employer_view_other_products.html', products=products_with_org, organizations=other_organizations)

def create_product_requests(product_id):
    # Crea una nuova richiesta di prodotto
    username = session.get('username')
    if not username:
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    
    form = CreateProductRequestForm()

    if request.method == 'GET':
        product = get_product_by_id(session_db, product_id)

        if not product:
            session_db.close()
            flash(PRODUCT_NOT_FOUND, 'danger')
            return redirect(url_for('view_other_products_route'))
        
        if product.id_organization == get_employer_by_username(session_db, username).id_organization:
            session_db.close()
            flash(UNAUTHORIZED_ACCESS, 'error')
            return redirect(url_for('permission_denied_route'))

        org = get_organization_by_id(session_db, product.id_organization)
        product_with_org = {
            'product': product,
            'organization_name': org.name
        }

        form.quantity.data = product.quantity

        session_db.close()
        return render_template('employer_create_product_requests.html', form=form, product=product_with_org)
    
    if request.method == 'POST' and form.validate_on_submit():
        quantity = form.quantity.data

        employer = get_employer_by_username(session_db, username)
        organization = get_organization_by_employer(session_db, employer)
        
        product = get_product_by_id(session_db, product_id)
        
        if quantity > product.quantity:
            flash(REQUESTED_QUANTITY_EXCEEDS_AVAILABLE, 'danger')
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
        flash(PRODUCT_REQUEST_CREATED_SUCCESSFULLY, 'success')

        return redirect(url_for('menage_product_requests_route'))
    
    session_db.close()
    return render_template('employer_create_product_requests.html', form=form, product=product_with_org)

def deny_product_request():
    # Rifiuta una richiesta di prodotto
    username = session.get('username')
    if not username:
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    request_id = request.form.get('request_id')
    if not request_id:
        flash(REQUEST_ID_REQUIRED, 'error')
        return redirect(url_for('menage_product_requests_route'))

    session_db = get_db_session()
    
    try:
        product_request = session_db.query(ProductRequest).get(request_id)
        if not product_request:
            flash(PRODUCT_REQUEST_NOT_FOUND, 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        product_request.status = 'rejected'
        product_request.date_responded = datetime.now()
        session_db.commit()
        flash(PRODUCT_REQUEST_DENIED_SUCCESSFULLY, 'success')
    except Exception as e:
        session_db.rollback()
        logging.error(f'Error: {str(e)}')
        flash(ERROR_OCCURRED.format(str(e)), 'error')
    finally:
        session_db.close()
    
    return redirect(url_for('menage_product_requests_route'))

def accept_product_request():
    # Accetta una richiesta di prodotto
    username = session.get('username')
    if not username:
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    request_id = request.form.get('request_id')
    carrier_id = request.form.get('carrier_id')
    if not request_id or not carrier_id:
        flash(REQUEST_ID_REQUIRED, 'error')
        return redirect(url_for('menage_product_requests_route'))

    session_db = get_db_session()
    
    try:
        product_request = session_db.query(ProductRequest).get(request_id)
        if not product_request:
            flash(PRODUCT_REQUEST_NOT_FOUND, 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        product = get_product_by_id(session_db, product_request.id_product)
        if not product:
            flash(PRODUCT_NOT_FOUND, 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        if product.quantity < product_request.quantity:
            flash(INSUFFICIENT_PRODUCT_QUANTITY, 'error')
            return redirect(url_for('menage_product_requests_route'))
        
        product.quantity -= product_request.quantity
        
        product_request.status = 'approved'
        product_request.id_carrier_organization = carrier_id
        product_request.date_responded = datetime.now()
        session_db.commit()
        flash(PRODUCT_REQUEST_ACCEPTED_SUCCESSFULLY, 'success')
    except Exception as e:
        session_db.rollback()
        logging.error(f'Error: {str(e)}')
        flash(ERROR_OCCURRED.format(str(e)), 'error')
    finally:
        session_db.close()
    
    return redirect(url_for('menage_product_requests_route'))

def carrier_menage_product_requests():
    # Gestisce le richieste di prodotti per il carrier
    username = session.get('username')
    if not username:
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()

    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    carring_product_request = session_db.query(ProductRequest).filter_by(id_carrier_organization=organization.id).all()

    carring_request_with_details = []
    for request in carring_product_request:
        product = get_product_by_id(session_db, request.id_product)
        requesting_org = get_organization_by_id(session_db, request.id_requesting_organization)
        providing_org = get_organization_by_id(session_db, request.id_providing_organization)
        carring_request_with_details.append({
            'request': request,
            'product_name': product.name,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': providing_org.name,
            'carrier_org_name': organization.name,
        })
    
    session_db.close()
    form = CarrierAcceptRequestAndCreateDeliveryForm()

    return render_template('carrier_menage_product_requests.html', organization=organization, 
        carring_product_request=carring_request_with_details, form=form)

def carrier_accept_and_create_delivery():
    # Accetta una richiesta di prodotto e crea una consegna
    username = session.get('username')
    if not username:
        flash(LOGIN_REQUIRED, 'error')
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()
    
    form = CarrierAcceptRequestAndCreateDeliveryForm()

    if request.method == 'POST' and form.validate_on_submit():
        request_id = form.request_id.data
        co2_emission = int(form.co2_emission.data)
        
        try:
            product_request = session_db.query(ProductRequest).filter_by(id=request_id).first()
            if not product_request:
                flash(PRODUCT_REQUEST_NOT_FOUND, 'error')
                return redirect(url_for('carrier_menage_product_requests_route'))
            
            organization = get_organization_by_id(session_db, product_request.id_carrier_organization)
            product = get_product_by_id(session_db, product_request.id_product)
            default_co2_value = session_db.query(Type).filter_by(id_type=organization.type).first().default_co2_value
            co2_standard = session_db.query(Type).filter_by(id_type=organization.type).first().standard
            co2_limit = default_co2_value + co2_standard * product_request.quantity

            if not coins_algorithm(co2_emission, co2_limit, organization, session_db, product.name, product_request.quantity):
                session_db.rollback()
                session_db.close()
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
            flash(DELIVERY_CREATED_SUCCESSFULLY, 'success')
            session_db.close()
        except Exception as e:
            session_db.rollback()
            logging.error(f'Error: {str(e)}')
            flash(ERROR_OCCURRED.format(str(e)), 'error')
            return redirect(url_for('carrier_menage_product_requests_route'))
        
    else:
        return redirect(url_for('carrier_menage_product_requests_route'))

    return redirect(url_for('carrier_menage_product_requests_route'))