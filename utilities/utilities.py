from database.database import DBIsConnected
from database.migration import Organization, Employer, Oracle, Product
from sqlalchemy.sql import func
import time
from flask import session
import os

NONCE_FILE = os.getenv('NONCE_FILE')

##########################################################################
# Utilities di auth_controller.py
##########################################################################

# Dizionario per tenere traccia dei tentativi di login falliti
login_attempts = {}

def get_db_session():
    db_instance = DBIsConnected.get_instance()
    return db_instance.get_session()

def get_organization_by_id(session, org_id):
    return session.query(Organization).filter_by(id=org_id).first()

def get_employer_by_username(session, username):
    return session.query(Employer).filter_by(username=username).first()

def get_oracle_by_username(session, username):
    return session.query(Oracle).filter_by(username=username).first()

def check_login_attempts(username):
    if username in login_attempts:
        attempts, last_attempt_time = login_attempts[username]
        if attempts >= 3 and time.time() - last_attempt_time < 30:
            return False
    return True

def update_login_attempts(username):
    if username in login_attempts:
        attempts, last_attempt_time = login_attempts[username]
        login_attempts[username] = (attempts + 1, time.time())
    else:
        login_attempts[username] = (1, time.time())

def reset_login_attempts(username):
    if username in login_attempts:
        del login_attempts[username]

def is_logged_in():
    return session.get('username') is not None

def is_oracle():
    return session.get('user_type') == 'oracle'

##########################################################################
# Utilities di coins_algorithm.py
##########################################################################

# Riusati get_db_session, get_organization_by_id, get_employer_by_username

def get_organization_by_employer(session, employer):
    return session.query(Organization).filter_by(id=employer.id_organization).first()

##########################################################################
# Utilities di deliveries_controller.py
##########################################################################

# Riusati get_db_session, get_organization_by_id, get_employer_by_username, get_organization_by_employer

def get_delivery_details(session, delivery):
    deliver_org = session.query(Organization).get(delivery.id_deliver_organization)
    receive_org = session.query(Organization).get(delivery.id_receiver_organization)
    carrier_org = session.query(Organization).get(delivery.id_carrier_organization)
    return {
        'delivery': delivery,
        'deliver_org_name': deliver_org.name,
        'receive_org_name': receive_org.name,
        'carrier_org_name': carrier_org.name,
        'deliver_org': deliver_org,
        'receive_org': receive_org,
        'carrier_org': carrier_org
    }

##########################################################################
# Utilities di employers_controller.py
##########################################################################

# Riusati get_db_session, get_organization_by_id, get_employer_by_username, get_organization_by_employer

##########################################################################
# Utilities di home_controller.py
##########################################################################

# Riusati get_db_session

def get_random_organizations(session, limit=10):
    return session.query(Organization).filter_by(status='active').order_by(func.random()).limit(limit).all()

def get_random_products(session, limit=10):
    return session.query(Product).order_by(func.random()).limit(limit).all()

def get_product_details(session, product):
    organization_name = session.query(Organization).filter_by(id=product.id_organization).first().name
    return {
        "id": product.id,
        "name": product.name,
        'type': product.type,
        "organization_name": organization_name,
    }

##########################################################################
# Utilities di oracle_controller.py
##########################################################################

# Riusati get_db_session, get_organization_by_id, get_organization_by_employer

def get_employer_by_id(session, emp_id):
    return session.query(Employer).filter_by(id=emp_id).first()

##########################################################################
# Utilities di organizations_controller.py
##########################################################################

# Riusati get_db_session, get_organization_by_id,

def get_employers_by_organization_id(session, org_id):
    return session.query(Employer).filter_by(id_organization=org_id).filter_by(status='active').all()

##########################################################################
# Utilities di products_requests_controller.py
##########################################################################

# Riusati get_db_session, get_organization_by_id, get_employer_by_username, get_organization_by_employer

def get_product_by_id(session, product_id):
    return session.query(Product).filter_by(id=product_id).first()

##########################################################################
# Utilities di products_controller.py
##########################################################################

# Riusati get_db_session, get_organization_by_id, get_employer_by_username, get_organization_by_employer, get_product_by_id

##########################################################################
# Utilities di coin_algorithm.py
##########################################################################

# Riusati get_db_session, get_organization_by_id, get_employer_by_username

def read_nonce():
    if os.path.exists(NONCE_FILE):
        with open(NONCE_FILE, 'r') as file:
            return int(file.read().strip())
    return None

def write_nonce(nonce):
    with open(NONCE_FILE, 'w') as file:
        file.write(str(nonce))