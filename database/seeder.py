from sqlalchemy.orm import Session
from .database import DBIsConnected
from .migration import Type, Organization, Employer, Oracle, Product, Delivery
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def seed_oracle(session: Session):
    if not session.query(Oracle).filter_by(username=os.getenv('ORACLE_USERNAME')).first():
        oracle = [
            Oracle(username=os.getenv('ORACLE_USERNAME'), password=os.getenv('ORACLE_PASSWORD')),
        ]
        session.bulk_save_objects(oracle)
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
            Organization(name='Org1', ragione_sociale='RS1', description='Desc1', partita_iva='12345678901', address='Address1', city='City1', cap='00001', telephone='1234567890', email='org1@example.com', type='farmer', coin=100.0),
            Organization(name='Org2', ragione_sociale='RS2', description='Desc2', partita_iva='12345678902', address='Address2', city='City2', cap='00002', telephone='1234567891', email='org2@example.com', type='seller', coin=200.0),
        ]
        session.bulk_save_objects(organizations)
        session.commit()

def seed_employers(session: Session):
    if not session.query(Employer).first():
        employers = [
            Employer(username='user1', password='pass1', name='Name1', surname='Surname1', id_organization=1),
            Employer(username='user2', password='pass2', name='Name2', surname='Surname2', id_organization=2),
        ]
        session.bulk_save_objects(employers)
        session.commit()

def seed_products(session: Session):
    if not session.query(Product).first():
        products = [
            Product(name='Prod1', type='raw material', quantity=100, id_organization=1),
            Product(name='Prod2', type='end product', quantity=200, id_organization=2),
        ]
        session.bulk_save_objects(products)
        session.commit()

def seed_deliveries(session: Session):
    if not session.query(Delivery).first():
        deliveries = [
            Delivery(id_product=1, quantity=50, co2_emission=5.0, id_deliver_organization=1, id_receiver_organization=2, date_timestamp=datetime.now()),
            Delivery(id_product=2, quantity=100, co2_emission=10.0, id_deliver_organization=2, id_receiver_organization=1, date_timestamp=datetime.now()),
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
        seed_deliveries(session)
        print("Database seeded successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_seeders()