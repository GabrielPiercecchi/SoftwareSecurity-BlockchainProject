from flask import flash, request, session, redirect, url_for, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from database.database import DBIsConnected
from database.migration import Oracle, Organization, Employer
from middlewares.validation import LengthValidator
import os
from algorithms.coins_algorithm import CoinsAlgorithm

NONCE_FILE = os.getenv('NONCE_FILE')

class CoinTransferForm(FlaskForm):
    target_organization = SelectField('Select Target Organization', validators=[DataRequired()])
    amount = IntegerField('Amount to Transfer', validators=[DataRequired(), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')], 
        render_kw={'placeholder': '100'})

def oracle_home():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    oracle_user = session_db.query(Oracle).filter_by(username=username).first()
    session_db.close()
    return render_template('oracle_home.html', oracle=oracle_user)

def oracle_view_organizations():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    organizations = session_db.query(Organization).filter_by(status = 'active').all()
    session_db.close()
    return render_template('oracle_view_organizations.html', organizations=organizations)

def oracle_coin_transfer(organization_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    form = CoinTransferForm()

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    organization = session_db.query(Organization).filter_by(id=organization_id).first()
    organizations = session_db.query(Organization).filter(Organization.id !=organization_id).filter_by(status = 'active').all()

    form.target_organization.choices = [(org.id, org.name) for org in organizations]
    session_db.close()

    if form.validate_on_submit():
        target_organization_id = form.target_organization.data
        amount = int(form.amount.data)

        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        source_organization = session_db.query(Organization).filter_by(id=organization_id).first()
        target_organization = session_db.query(Organization).filter_by(id=target_organization_id).first()

        if amount > int(source_organization.coin):
            flash('Amount exceeds available coins.', 'too_much')
        elif source_organization.coin - amount < 20:
            flash('Insufficient coins for transfer. The organization must retain at least 20 coins.', 'insufficient_coins')
        else:
            # Esegui la transazione sulla blockchain
            manager = CoinsAlgorithm()
            tx = manager.coin_contract.functions.transferCoins(
                source_organization.blockchain_address,
                target_organization.blockchain_address,
                amount
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
                source_organization.coin -= amount
                target_organization.coin += amount
                session_db.commit()
                flash('Coins transferred successfully!', 'success')
            else:
                manager.increment_nonce()  # Incrementa il nonce
                flash('Failed to transfer coins on blockchain.', 'error')
            session_db.close()
            return redirect(url_for('oracle_view_organizations_route'))
        session_db.close()
        return redirect(url_for('oracle_coin_transfer_route', organization_id=organization_id))

    return render_template('oracle_coin_transfer.html', organization=organization, form=form, organizations={org.id: org.coin for org in organizations})

def view_organization_inactive():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    pending_organizations = session_db.query(Organization).filter_by(status='inactive').all()
    session_db.close()
    return render_template('oracle_view_organization_inactive.html', pending_organizations=pending_organizations)

def manage_organization_registration(organization_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    organization = session_db.query(Organization).filter_by(id=organization_id, status='inactive').first()
    if not organization:
        flash('Organization not found or not inactive.', 'danger')
        return redirect(url_for('view_organization_inactive_route'))
    
    employers = session_db.query(Employer).filter_by(id_organization=organization_id).all()
    session_db.close()
    return render_template('oracle_manage_organization_registration.html', organization=organization, employers=employers)

def approve_organization(organization_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))

    if request.method == 'POST':
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        
        organization = session_db.query(Organization).get(organization_id)
        if organization:
            organization.status = 'active'
            # Aggiorna lo stato degli employer associati a 'active'
            session_db.query(Employer).filter_by(id_organization=organization_id).update({'status': 'active'})
            session_db.commit()
            message = 'Organization and associated employers approved and activated.'
            flash(message, 'success')
        else:
            message = 'Organization not found.'
            flash(message, 'danger')
        
        session_db.close()
        return jsonify({'message': message, 'redirect_url': url_for('view_organization_inactive_route')})
    
def reject_organization(organization_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    if request.method == 'POST':
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        
        organization = session_db.query(Organization).get(organization_id)
        if organization:
            # Elimina prima gli employer associati
            session_db.query(Employer).filter_by(id_organization=organization_id).delete()
            session_db.delete(organization)
            session_db.commit()
            message = 'Organization registration rejected and deleted.'
            flash(message, 'success')
        else:
            message = 'Organization not found.'
            flash(message, 'danger')
        
        session_db.close()
        return jsonify({'message': message, 'redirect_url': url_for('view_organization_inactive_route')})
    
def view_employer_inactive():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    pending_employers = session_db.query(Employer).join(Organization).filter(
        Employer.status == 'inactive',
        Organization.status == 'active'
    ).all()

    employer_data = []
    for employer in pending_employers:
        employer_info = {
            'id': employer.id,
            'name': employer.name,
            'surname': employer.surname,
            'username': employer.username,
            'email': employer.email,
            'organization_name': session_db.query(Organization).filter_by(id=employer.id_organization).first().name,
            'organization_id': employer.id_organization,
        }
        employer_data.append(employer_info)

    session_db.close()

    return render_template('oracle_view_employer_inactive.html', pending_employers=employer_data)

def manage_employer_registration(employer_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    
    employer = session_db.query(Employer).filter_by(id=employer_id, status='inactive').first()
    if not employer:
        flash('Employer not found or not inactive.', 'danger')
        return redirect(url_for('view_employer_inactive_route'))
    
    employer_info = {
        'id': employer.id,
        'name': employer.name,
        'surname': employer.surname,
        'username': employer.username,
        'email': employer.email,
        'organization_name': session_db.query(Organization).filter_by(id=employer.id_organization).first().name,
        'organization_id': employer.id_organization,
    }

    session_db.close()
    return render_template('oracle_manage_employer_registration.html', employer=employer_info)

def approve_employer(employer_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    if request.method == 'POST':
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        
        employer = session_db.query(Employer).get(employer_id)
        if employer:
            employer.status = 'active'
            session_db.commit()
            message = 'Employer approved and activated.'
            flash(message, 'success')
        else:
            message = 'Employer not found.'
            flash(message, 'danger')
        
        session_db.close()
        return jsonify({'message': message, 'redirect_url': url_for('view_employer_inactive_route')})

def reject_employer(employer_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    if request.method == 'POST':
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        
        employer = session_db.query(Employer).get(employer_id)
        if employer:
            session_db.delete(employer)
            session_db.commit()
            message = 'Employer registration rejected and deleted.'
            flash(message, 'success')
        else:
            message = 'Employer not found.'
            flash(message, 'danger')
        
        session_db.close()
        return jsonify({'message': message, 'redirect_url': url_for('view_employer_inactive_route')})