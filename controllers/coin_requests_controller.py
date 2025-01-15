from flask import render_template, session, redirect, url_for, flash, request, jsonify
from datetime import datetime
from wtforms import StringField, RadioField, TextAreaField, IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from database.database import DBIsConnected
from database.migration import Product, Organization, Employer, ProductRequest, Delivery, Type, CoinRequest
from algorithms.coins_algorithm import coins_algorithm

class AcceptCoinRequestForm(FlaskForm):
    request_id = IntegerField('Request ID', validators=[DataRequired()])
    submit = SubmitField('Accept')

class CoinRequestForm(FlaskForm):
    coin = FloatField('Coin', validators=[DataRequired(message='You must digit a float number')], render_kw={'placeholder': '100.0'})
    submit = SubmitField('Submit')

def view_coin_requests():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    form = AcceptCoinRequestForm()

    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()

    coin_request_made = session_db.query(CoinRequest).filter_by(id_requesting_organization=organization.id).all()
    coin_requests_received = session_db.query(CoinRequest).filter(CoinRequest.id_requesting_organization!=organization.id).filter_by(status='pending').all()

    coin_request_made_with_details = []
    for request in coin_request_made:
        providing_org = session_db.query(Organization).get(request.id_providing_organization)
        if providing_org:
            providing_org_name = providing_org.name
        else:
            providing_org_name = "TBD"
        coin_request_made_with_details.append({
            'request': request,
            'requesting_org_name': organization.name,
            'providing_org_name': providing_org_name,
        })

    coin_requests_received_with_details = []
    for request in coin_requests_received:
        requesting_org = session_db.query(Organization).filter_by(id=request.id_requesting_organization).first()
        providing_org_name = 'TBD'
        coin_requests_received_with_details.append({
            'request': request,
            'requesting_org_name': requesting_org.name,
            'providing_org_name': providing_org_name,
        })

    session_db.close()

    return render_template('employer_view_coin_requests.html', form=form, organization=organization, coin_requests_made=coin_request_made_with_details, coin_requests_received=coin_requests_received_with_details)

def view_accepted_coin_requests():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()

    coin_request_accepted = session_db.query(CoinRequest).filter_by(id_providing_organization=organization.id).filter_by(status='approved').all()

    coin_request_accepted_with_details = []
    for request in coin_request_accepted:
        requesting_org = session_db.query(Organization).get(request.id_requesting_organization)
        requesting_org_name = requesting_org.name
        coin_request_accepted_with_details.append({
            'request': request,
            'requesting_org_name': requesting_org_name,
            'providing_org_name': organization.name,
        })

    session_db.close()

    return render_template('employer_view_accepted_coin_requests.html', organization=organization, coin_requests_accepted=coin_request_accepted_with_details)

def create_coin_request():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    form = CoinRequestForm()

    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    
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
    if not username:
        return redirect(url_for('login_route'))

    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()

    request_id = request.form['request_id']
    if not request_id:
        print('Request ID are required')
        flash('Request ID are required', 'error')
        return redirect(url_for('view_coin_requests_route'))

    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    organization_requesting = session_db.query(Organization).filter_by(id=request_id).first()

    if request.method == 'GET':
        session_db.close()
        return redirect(url_for('view_coin_requests_route'))

    if request.method == 'POST':
        try:
            coin_request = session_db.query(CoinRequest).filter_by(id=request_id).first()

            if float(coin_request.coin) > float(organization.coin):
                flash('You do not have enough coins to accept this request', 'error')
                session_db.close()
                return redirect(url_for('view_coin_requests_route'))
            elif float(organization.coin) - float(coin_request.coin) < 20:
                flash('You must retain at least 20 coins', 'error')
                session_db.close()
                return redirect(url_for('view_coin_requests_route'))
            else:
                coin_request.status = 'approved'
                coin_request.id_providing_organization = organization.id
                organization.coin = float(organization.coin) - float(coin_request.coin)
                organization_requesting.coin = float(organization_requesting.coin) + float(coin_request.coin)
                coin_request.date_responded = datetime.now()
                session_db.commit()
                session_db.close()
                return redirect(url_for('view_coin_requests_route'))
        except Exception as e:
            print(e)
            flash('Error accepting coin request', 'error')
            session_db.close()
            return redirect(url_for('view_coin_requests_route'))

    session_db.close()

    return redirect(url_for('view_coin_requests_route'))