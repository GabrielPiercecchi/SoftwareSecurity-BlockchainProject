from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import psycopg2
import os
from .database import DBIsConnected
from werkzeug.security import generate_password_hash

load_dotenv()

Base = declarative_base()

def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname='postgres',
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('DATABASE_PORT_FLASK_APP')
    )
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {os.getenv('DATABASE_NAME')}")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {os.getenv('DATABASE_NAME')} already exists.")
        cursor.execute(f"DROP DATABASE {os.getenv('DATABASE_NAME')}")
        print(f"Database {os.getenv('DATABASE_NAME')} dropped.")
        cursor.execute(f"CREATE DATABASE {os.getenv('DATABASE_NAME')}")
        print(f"Database {os.getenv('DATABASE_NAME')} created.")
    cursor.close()
    conn.close()

class Oracle(Base):
    __tablename__ = 'oracle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(162), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

class Type(Base):
    __tablename__ = 'type'
    id_type = Column(Enum('farmer', 'seller', 'producer', 'carrier', name='type_enum'), primary_key=True)
    default_co2_value = Column(Integer, nullable=False, unique=True)
    standard = Column(Integer, nullable=False)

class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    ragione_sociale = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    partita_iva = Column(String(20), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    cap = Column(String(10), nullable=False)
    telephone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    type = Column(Enum('farmer', 'seller', 'producer', 'carrier', name='type_enum'), ForeignKey('type.id_type'), nullable=False)
    status = Column(Enum('active', 'inactive', name='status_enum'), nullable=False, default='inactive')
    coin = Column(Integer, nullable=False, default=100)
    blockchain_address = Column(String(42), nullable=True)  # Nuovo campo aggiunto
    
class Employer(Base):
    __tablename__ = 'employer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(162), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True) 
    status = Column(Enum('active', 'inactive', name='status_enum'), nullable=False, default='inactive')
    id_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum('raw material', 'end product', name='product_type_enum'), nullable=False)
    quantity = Column(Integer, nullable=False)
    id_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    co2_production_product = Column(Integer, nullable=False)

class ProductRequest(Base):
    __tablename__ = 'product_request'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer, ForeignKey('product.id'), nullable=False)
    id_requesting_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    id_providing_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    id_carrier_organization = Column(Integer, default=None)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected', name='request_status_enum'), nullable=False, default='pending')
    status_delivery = Column(Enum('pending', 'delivered', name='delivery_status_enum'), nullable=False, default='pending')
    date_requested = Column(DateTime, nullable=False, default=datetime.now)
    date_responded = Column(DateTime)

class CoinRequest(Base):
    __tablename__ = 'coin_request'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_requesting_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    id_providing_organization = Column(Integer, default=None)
    coin = Column(Integer, nullable=False)
    status = Column(Enum('pending', 'approved', name='coin_request_status_enum'), nullable=False, default='pending')
    date_requested = Column(DateTime, nullable=False, default=datetime.now)
    date_responded = Column(DateTime)

class Delivery(Base):
    __tablename__ = 'delivery'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    co2_emission = Column(Integer, nullable=False)
    id_deliver_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    id_receiver_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    id_carrier_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    used = Column(Enum('yes', 'no', name='used_enum'), nullable=False, default='no')
    date_timestamp = Column(DateTime, nullable=False, default=datetime.now)

class ProductOrigin(Base):
    __tablename__ = 'product_origin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_origin_product = Column(Integer, ForeignKey('product.id'), nullable=False)
    id_end_product = Column(Integer, ForeignKey('product.id'), nullable=False)
    date_timestamp = Column(DateTime, nullable=False, default=datetime.now)

def init_db():
    create_database_if_not_exists()
    db_instance = DBIsConnected.get_instance()
    Base.metadata.create_all(bind=db_instance.engine)