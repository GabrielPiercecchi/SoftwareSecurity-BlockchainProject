from flask import render_template, session, redirect, url_for, flash, request
import logging
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
from database.migration import CoinRequest
from algorithms.coins_algorithm import update_organization_coins_on_blockchain
from middlewares.validation import LengthValidator
from utilities.utilities import get_db_session, get_organization_by_id, get_employer_by_username, get_organization_by_employer
from messages.messages import REQUEST_ID_REQUIRED, NOT_ENOUGH_COINS, COIN_REQUEST_ACCEPTED, ERROR_ACCEPTING_COIN_REQUEST

class AcceptCoinRequestForm(FlaskForm):
    request_id = IntegerField('Request ID', validators=[DataRequired()])
    submit = SubmitField('Accept')

class CoinRequestForm(FlaskForm):
    coin = IntegerField('Coin', validators=[DataRequired(message='You must digit an Integer number'), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')], 
        render_kw={'placeholder': '100'})
    submit = SubmitField('Submit')

def view_coin_requests():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    form = AcceptCoinRequestForm()

    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)

    coin_request_made = session_db.query(CoinRequest).filter_by(id_requesting_organization=organization.id).all()
    coin_requests_received = session_db.query(CoinRequest).filter(CoinRequest.id_requesting_organization != organization.id).filter_by(status='pending').all()

    coin_request_made_with_details = []
    for request in coin_request_made:
        providing_org = get_organization_by_id(session_db, request.id_providing_organization)
        providing_org_name = providing_org.name if providing_org else "TBD"
        coin_request_made_with_details.append({
            'request': request,
            'requesting_org_name': organization.name,
            'providing_org_name': providing_org_name,
        })

    coin_requests_received_with_details = []
    for request in coin_requests_received:
        requesting_org = get_organization_by_id(session_db, request.id_requesting_organization)
        coin_requests_received_with_details.append({
            'request': request,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': 'TBD',
        })

    session_db.close()

    return render_template('employer_view_coin_requests.html', form=form, organization=organization, 
        coin_requests_made=coin_request_made_with_details, coin_requests_received=coin_requests_received_with_details)

def view_accepted_coin_requests():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))

    session_db = get_db_session()

    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)

    coin_request_accepted = session_db.query(CoinRequest).filter_by(id_providing_organization=organization.id).filter_by(status='approved').all()

    coin_request_accepted_with_details = []
    for request in coin_request_accepted:
        requesting_org = get_organization_by_id(session_db, request.id_requesting_organization)
        coin_request_accepted_with_details.append({
            'request': request,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': organization.name,
        })

    session_db.close()

    return render_template('employer_view_accepted_coin_requests.html', organization=organization, 
        coin_requests_accepted=coin_request_accepted_with_details)

def create_coin_request():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))

    session_db = get_db_session()
    form = CoinRequestForm()

    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    
    if request.method == 'GET':
        session_db.close()
        return render_template('employer_create_coin_request.html', organization=organization, form=form)

    if request.method == 'POST' and form.validate_on_submit():
        coin = request.form['coin']
        coin_request = CoinRequest(id_requesting_organization=organization.id, coin=coin)
        session_db.add(coin_request)
        session_db.commit()
        session_db.close()
        return redirect(url_for('view_coin_requests_route'))

    session_db.close()

    return render_template('employer_create_coin_request.html', organization=organization, form=form)

def accept_coin_request():
    username = session.get('username')
    if not username or not session.get('user_type') == 'employer':
        return redirect(url_for('login_route'))

    session_db = get_db_session()

    request_id = request.form['request_id']
    if not request_id:
        flash(REQUEST_ID_REQUIRED, 'error')
        return redirect(url_for('view_coin_requests_route'))

    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_employer(session_db, employer)
    organization_requesting = get_organization_by_id(session_db, request_id)

    if request.method == 'GET':
        session_db.close()
        return redirect(url_for('view_coin_requests_route'))

    if request.method == 'POST':
        try:
            coin_request = session_db.query(CoinRequest).filter_by(id=request_id).first()

            if not update_organization_coins_on_blockchain(organization, organization_requesting, coin_request, session_db):
                flash(NOT_ENOUGH_COINS, 'error')
                session_db.close()
                return redirect(url_for('view_coin_requests_route'))
            else:
                flash(COIN_REQUEST_ACCEPTED, 'success')
                return redirect(url_for('view_coin_requests_route'))
        except Exception as e:
            flash(ERROR_ACCEPTING_COIN_REQUEST, 'error')
            session_db.close()
            logging.error(f'Error accepting coin request: {e}')
            return redirect(url_for('view_coin_requests_route'))

    session_db.close()

    return redirect(url_for('view_coin_requests_route'))