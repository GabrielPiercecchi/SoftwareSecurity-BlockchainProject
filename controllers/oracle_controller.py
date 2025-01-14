from flask import flash, request, session, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired
from database.database import DBIsConnected
from database.migration import Oracle, Organization

class CoinTransferForm(FlaskForm):
    target_organization = SelectField('Select Target Organization', validators=[DataRequired()])
    amount = FloatField('Amount to Transfer', validators=[DataRequired()], render_kw={'placeholder': '100.0'})

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
        amount = form.amount.data

        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        source_organization = session_db.query(Organization).filter_by(id=organization_id).first()
        target_organization = session_db.query(Organization).filter_by(id=target_organization_id).first()

        if amount > source_organization.coin:
            flash('Amount exceeds available coins.', 'too_much')
        elif source_organization.coin - amount < 20:
            flash('Insufficient coins for transfer. The organization must retain at least 20 coins.', 'insufficient_coins')
        else:
            source_organization.coin -= amount
            target_organization.coin += amount
            session_db.commit()
            flash('Coins transferred successfully!', 'success')
            session_db.close()
            return redirect(url_for('oracle_view_organizations_route'))

        session_db.close()
        return redirect(url_for('oracle_coin_transfer_route', organization_id=organization_id))

    return render_template('oracle_coin_transfer.html', organization=organization, form=form, organizations={org.id: org.coin for org in organizations})