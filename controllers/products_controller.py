from flask import flash, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from database.database import DBIsConnected
from database.migration import Employer, Product, Delivery, Organization
from wtforms.validators import DataRequired
from wtforms import RadioField, StringField, FloatField, IntegerField, SelectField

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('raw material', 'Raw Material'), ('end product', 'End Product')], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
from flask import render_template, session, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired
from database.database import DBIsConnected
from database.migration import Product, Delivery, Organization, Employer

class UpdateProductForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('raw material', 'Raw material'), ('end product', 'End product')], validators=[DataRequired()])

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

def create_product():
    username = session['username']

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).get(employer.id_organization)
    session_db.close()


    form = ProductForm()
    form.organization = organization.id


    if request.method == 'POST' and form.validate():
        name = form.name.data
        type = form.type.data
        quantity = form.quantity.data

        session_db = db_instance.get_session()
    
        try:
            new_prod = Product(  
            name=name,
            type=type,
            quantity=quantity,
            id_organization=organization.id
            )    
            session_db.add(new_prod)

            session_db.commit()
            print('Product added successfully!')
        except Exception as e:
            session_db.rollback()
            print(f'Error: {str(e)}')
        finally:
            session_db.close()

        return redirect(url_for('home_route'))
    
    return render_template('create_products.html', form=form, organization=organization)
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

def update_product(product_id):
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    product = session_db.query(Product).filter_by(id=product_id).first()
    session_db.close()
    
    form = UpdateProductForm()
    
    if request.method == 'GET':
        # Fetch the product from the database
        
        if not product:
            flash('Product not found.', 'error')
            return redirect(url_for('employer_view_products_route'))
        
        # Populate the form with the product data
        form.name.data = product.name
        form.type.data = product.type
        
        return render_template('employer_update_product.html', form=form, product=product)
    
    if request.method == 'POST' and form.validate_on_submit():
        product = session_db.query(Product).filter_by(id=product_id).first()
        if product:
            product.name = form.name.data
            product.type = form.type.data
            session_db.commit()
            session_db.close()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('employer_view_products_route'))
        else:
            session_db.close()
            flash('Failed to update product.', 'error')
            return redirect(url_for('employer_view_products_route'))
    
    return render_template('employer_update_product.html', form=form, product=product)
