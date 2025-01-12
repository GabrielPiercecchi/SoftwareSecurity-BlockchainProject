from flask import render_template, session, redirect, url_for, flash, request
import datetime
from wtforms import StringField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from database.database import DBIsConnected
from database.migration import Product, Organization, Employer, ProductRequest

class CreateProductRequestForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])

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

    return render_template('employer_menage_product_requests.html', organization=organization, providing_product_requests=providing_requests_with_details, requesting_product_requests=requesting_requests_with_details)

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