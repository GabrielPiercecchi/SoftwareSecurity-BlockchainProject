from flask import flash, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
import logging
from database.migration import Product, Delivery, Organization, Type, ProductOrigin
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField
from algorithms.coins_algorithm import coins_algorithm
from middlewares.validation import LengthValidator
from algorithms.coins_algorithm import CoinsAlgorithm
from utilities.utilities import get_db_session, get_organization_by_id, get_employer_by_username, get_organization_by_employer, get_product_by_id

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()], render_kw={'placeholder': 'Name'})
    type = SelectField('Type', choices=[('raw material', 'Raw Material'), ('end product', 'End Product')], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')], 
        render_kw={'placeholder': '100'})
    co2_production_product = IntegerField('CO2 Production', validators=[DataRequired(), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')], 
        render_kw={'placeholder': '100'})
    co2_origin_product_list = SelectMultipleField('CO2 Origin Products', choices=[])

class UpdateProductForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('raw material', 'Raw material'), ('end product', 'End product')], 
                validators=[DataRequired()])

def product_detail(id):
    session_db = get_db_session()
    product = get_product_by_id(session_db, id)

    if not product:
        session_db.close()
        flash('Product not found.', 'danger')
        return redirect(url_for('products_route'))

    deliveries = session_db.query(Delivery).filter_by(id_product=id).all()
    organization = get_organization_by_id(session_db, product.id_organization)
    
    deliveries_with_orgs = []
    for delivery in deliveries:
        deliver_org = get_organization_by_id(session_db, delivery.id_deliver_organization)
        receive_org = get_organization_by_id(session_db, delivery.id_receiver_organization)
        carrier_org = get_organization_by_id(session_db, delivery.id_carrier_organization)
        deliveries_with_orgs.append({
            'delivery': delivery,
            'deliver_org_name': deliver_org.name,
            'receive_org_name': receive_org.name,
            'carrier_org_name': carrier_org.name
        })

    # Ottieni le transazioni di origine del prodotto dalla blockchain
    manager = CoinsAlgorithm()
    origin_products, end_products, timestamps = manager.coin_contract.functions.getProductOriginTransactions().call()
    product_origin_transactions = []
    products_made_with = []
    products_made_from = []
    for i in range(len(origin_products)):
        origin_product = get_product_by_id(session_db, origin_products[i])
        end_product = get_product_by_id(session_db, end_products[i])
        origin_product_org = get_organization_by_id(session_db, origin_product.id_organization)
        end_product_org = get_organization_by_id(session_db, end_product.id_organization)
        if origin_products[i] == id:
            products_made_with.append({
                'product': end_product,
                'organization_name': end_product_org.name
            })
        if end_products[i] == id:
            products_made_from.append({
                'product': origin_product,
                'organization_name': origin_product_org.name
            })
        product_origin_transactions.append({
            'origin_product': origin_product.name,
            'end_product': end_product.name,
            'timestamp': timestamps[i]
        })
    
    session_db.close()
    return render_template("product_detail.html", product=product, 
        deliveries=deliveries_with_orgs, organization=organization, 
        product_origin_transactions=product_origin_transactions, products_made_with=products_made_with, 
        products_made_from=products_made_from)

def get_all_products():
    session_db = get_db_session()
    products = session_db.query(Product).all()
    products_with_org = []
    for product in products:
        organization = get_organization_by_id(session_db, product.id_organization)
        products_with_org.append({
            'product': product,
            'organization_name': organization.name
        })
    session_db.close()
    return render_template("products.html", products=products_with_org)

def create_product():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)

    form = ProductForm()

    if session.get('user_org_type') == 'producer':
        form.type.choices = [('end product', 'End Product')]
        form.type.default = 'end product'

        # Popola le scelte per il campo co2_origin_product_list
        deliveries = session_db.query(Delivery).filter_by(id_receiver_organization=organization.id, used='no').all()

        # Ottieni tutti i prodotti e le organizzazioni in una sola query
        product_ids = [delivery.id_product for delivery in deliveries]
        products = session_db.query(Product).filter(Product.id.in_(product_ids)).all()
        products_dict = {product.id: product.name for product in products}

        organization_ids = [delivery.id_deliver_organization for delivery in deliveries]
        organizations = session_db.query(Organization).filter(Organization.id.in_(organization_ids)).all()
        organizations_dict = {org.id: org.name for org in organizations}

        # Popola le scelte per il campo co2_origin_product_list
        form.co2_origin_product_list.choices = [
            (str(delivery.id_product), f"{products_dict[delivery.id_product]} ({organizations_dict[delivery.id_deliver_organization]})")
            for delivery in deliveries
        ]
        session_db.close()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        type = form.type.data
        quantity = int(form.quantity.data)
        co2_production_product = int(form.co2_production_product.data)
        co2_origin_product_list = form.co2_origin_product_list.data

        if session.get('user_org_type') == 'producer' and not co2_origin_product_list:
            flash('At least one origin product must be selected.', 'error')
            return render_template('employer_create_products.html', form=form, organization=organization)

        session_db = get_db_session()
    
        try:
            default_co2_value = session_db.query(Type).filter_by(id_type=organization.type).first().default_co2_value
            co2_standard = session_db.query(Type).filter_by(id_type=organization.type).first().standard
            co2_limit = default_co2_value + co2_standard*quantity

            if not coins_algorithm(co2_production_product, co2_limit, organization, session_db):
                session_db.rollback()
                return redirect(url_for('create_product_route'))

            new_prod = Product(  
            name=name,
            type=type,
            quantity=quantity,
            id_organization=organization.id,
            co2_production_product=co2_production_product
            )    
            session_db.add(new_prod)
            session_db.commit()

            # Aggiorna il campo used a 'yes' e popola la tabella ProductOrigin
            manager = CoinsAlgorithm()
            for origin_product_id in co2_origin_product_list:
                delivery = session_db.query(Delivery).filter_by(id_product=origin_product_id, id_receiver_organization=organization.id).first()
                if delivery:
                    delivery.used = 'yes'
                    product_origin = ProductOrigin(
                        id_origin_product=origin_product_id,
                        id_end_product=new_prod.id
                    )
                    session_db.add(product_origin)

                    # Registra l'aggiornamento sulla blockchain
                    tx = manager.coin_contract.functions.registerProductOrigin(
                        int(origin_product_id),
                        int(new_prod.id)
                    ).build_transaction({
                        'chainId': manager.contract_interactions.chain_id,
                        'gas': 2000000,
                        'gasPrice': manager.contract_interactions.w3.eth.gas_price,
                        'nonce': manager.nonce,
                    })
                    signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
                    tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                    receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
                    if receipt.status == 1:
                        manager.increment_nonce()  # Incrementa il nonce
                    else:
                        session_db.rollback()
                        manager.increment_nonce()  # Incrementa il nonce
                        flash('Failed to register product origin on blockchain.', 'error')
                        return redirect(url_for('create_product_route'))

            session_db.commit()
            session_db.close()
            print('Product added successfully!')
        except Exception as e:
            session_db.rollback()
            print(f'Error: {str(e)}')
            logging.error(f'Error: {str(e)}')
            flash('Failed to add product: intero fuori dall\'intervallo', 'error')
            return redirect(url_for('create_product_route'))
            
        return redirect(url_for('employer_home_route'))
    
    return render_template('employer_create_products.html', form=form, organization=organization)

def employer_view_products():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    session_db = get_db_session()
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    products = session_db.query(Product).filter_by(id_organization=organization.id).all()
    session_db.close()
    
    return render_template('employer_view_products.html', products=products, organization=organization)

def update_product(product_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    product = get_product_by_id(session_db, product_id)
    session_db.close()

    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('employer_view_products_route'))

    if product.id_organization != session.get('user_org_id'):
        flash('Unauthorized access.', 'error')
        return redirect(url_for('permission_denied_route'))
    
    form = UpdateProductForm()

    if session.get('user_org_type') == 'producer':
        form.type.choices = [('end product', 'End Product')]
        form.type.default = 'end product'
    
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
        session_db = get_db_session()
        product = get_product_by_id(session_db, product_id)
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