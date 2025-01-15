from sqlalchemy.orm import Session
from .database import DBIsConnected
from .migration import Type, Organization, Employer, Oracle, Product, Delivery, ProductRequest, CoinRequest
from dotenv import load_dotenv
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

load_dotenv()

def seed_oracle(session: Session):
    if not session.query(Oracle).filter_by(username=os.getenv('ORACLE_USERNAME')).first():
        oracle = Oracle(
            username=os.getenv('ORACLE_USERNAME'),
            password=generate_password_hash(os.getenv('ORACLE_PASSWORD'))
        )
        session.add(oracle)
        session.commit()

def seed_types(session: Session):
    if not session.query(Type).first():
        types = [
            Type(id_type='farmer', default_co2_value=1.0, standard=1.0),
            Type(id_type='seller', default_co2_value=2.0, standard=2.0),
            Type(id_type='producer', default_co2_value=3.0, standard=3.0),
            Type(id_type='carrier', default_co2_value=4.0, standard=4.0),
        ]
        session.bulk_save_objects(types)
        session.commit()

def seed_organizations(session: Session):
    if not session.query(Organization).first():
        organizations = [
            Organization(name='Org1', ragione_sociale='RS1', description='Desc1', partita_iva='12345678901', address='Address1', city='City1', cap='00001', telephone='1234567890', email='org1@example.com', type='farmer', status= 'active', coin=100.0),
            Organization(name='Org2', ragione_sociale='RS2', description='Desc2', partita_iva='12345678902', address='Address2', city='City2', cap='00002', telephone='1234567891', email='org2@example.com', type='seller', status= 'active', coin=100.0),
            Organization(name='Org3', ragione_sociale='RS3', description='Desc3', partita_iva='12345678903', address='Address3', city='City3', cap='00003', telephone='1234567892', email='org3@example.com', type='carrier', status= 'active', coin=100.0),
            Organization(name='Org4', ragione_sociale='RS4', description='Desc4', partita_iva='12345678904', address='Address4', city='City4', cap='00004', telephone='1234567893', email='org4@example.com', type='carrier', status= 'active', coin=100.0),
        ]
        session.bulk_save_objects(organizations)
        session.commit()

def seed_employers(session: Session):
    if not session.query(Employer).first():
        employers_data = [
            {'username': 'user1', 'password': 'pass1', 'name': 'Name1', 'surname': 'Surname1', 'email': 'email1@example.com', 'status': 'active', 'id_organization': 1},
            {'username': 'user2', 'password': 'pass2', 'name': 'Name2', 'surname': 'Surname2', 'email': 'email2@example.com', 'status': 'active', 'id_organization': 2},
            {'username': 'user3', 'password': 'pass3', 'name': 'Name3', 'surname': 'Surname3', 'email': 'email3@example.com', 'status': 'active', 'id_organization': 3},
            {'username': 'user4', 'password': 'pass4', 'name': 'Name4', 'surname': 'Surname4', 'email': 'email4@example.com', 'status': 'active', 'id_organization': 4},
        ]
        employers = []
        for data in employers_data:
            employer = Employer(
                username=data['username'],
                name=data['name'],
                surname=data['surname'],
                email=data['email'],
                status=data['status'],
                id_organization=data['id_organization']
            )
            employer.set_password(data['password'])  # Hash the password
            employers.append(employer)
        
        session.bulk_save_objects(employers)
        session.commit()

def seed_products(session: Session):
    if not session.query(Product).first():
        products = [
            Product(name='Prod1', type='raw material', quantity=100, id_organization=1, co2_production_product=1.0),
            Product(name='Prod2', type='end product', quantity=200, id_organization=2, co2_production_product=2.0),
            Product(name='Prod3', type='raw material', quantity=100, id_organization=1, co2_production_product=100.0),
        ]
        session.bulk_save_objects(products)
        session.commit()

def seed_product_requests(session: Session):
    # Assicurati che ci siano organizzazioni e prodotti di esempio
    org_a = session.query(Organization).filter_by(name='Org1').first()
    org_b = session.query(Organization).filter_by(name='Org2').first()
    product1 = session.query(Product).filter_by(name='Prod1').first()
    product2 = session.query(Product).filter_by(name='Prod2').first()

    if org_a and org_b and product1:
        if not session.query(ProductRequest).first():
            product_requests = [
                ProductRequest(
                    id_product=product1.id,
                    id_requesting_organization=org_b.id,
                    id_providing_organization=org_a.id,
                    quantity=50,
                    status='pending',
                    date_requested=datetime.now()
                ),
                ProductRequest(
                    id_product=product1.id,
                    id_requesting_organization=org_b.id,
                    id_providing_organization=org_a.id,
                    quantity=100,
                    status='pending',
                    date_requested=datetime.now()
                ),
                ProductRequest(
                    id_product=product1.id,
                    id_requesting_organization=org_b.id,
                    id_providing_organization=org_a.id,
                    id_carrier_organization=3,
                    quantity=100,
                    status='approved',
                    date_requested=datetime.now(),
                    date_responded=datetime.now()
                ),
                ProductRequest(
                    id_product=product2.id,
                    id_requesting_organization=org_a.id,
                    id_providing_organization=org_b.id,
                    id_carrier_organization=3,
                    quantity=100,
                    status='approved',
                    date_requested=datetime.now(),
                    date_responded=datetime.now()
                )
            ]
            session.bulk_save_objects(product_requests)
            session.commit()

def seed_coin_requests(session: Session):
    if not session.query(CoinRequest).first():
        coin_requests = [
            CoinRequest(
                id_requesting_organization=1,
                id_providing_organization=2,
                coin=100.0,
                status='approved',
                date_requested=datetime.now(),
                date_responded=datetime.now()
            ),
            CoinRequest(
                id_requesting_organization=2,
                coin=150.0,
                status='pending',
                date_requested=datetime.now()
            ),
            CoinRequest(
                id_requesting_organization=3,
                id_providing_organization=1,
                coin=200.0,
                status='approved',
                date_requested=datetime.now(),
                date_responded=datetime.now()
            )
        ]
        session.bulk_save_objects(coin_requests)
        session.commit()


def seed_deliveries(session: Session):
    if not session.query(Delivery).first():
        deliveries = [
            Delivery(id_product=1, quantity=50, co2_emission=5.0, id_deliver_organization=1, id_receiver_organization=2, id_carrier_organization=3, date_timestamp=datetime.now()),
            Delivery(id_product=2, quantity=100, co2_emission=10.0, id_deliver_organization=2, id_receiver_organization=1, id_carrier_organization=3, date_timestamp=datetime.now()),
        ]
        session.bulk_save_objects(deliveries)
        session.commit()

def run_seeders():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()

    try:
        seed_oracle(session)
        seed_types(session)
        seed_organizations(session)
        seed_employers(session)
        seed_products(session)  # Seed products before deliveries
        seed_product_requests(session)
        seed_coin_requests(session)
        seed_deliveries(session)
        print("Database seeded successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_seeders()