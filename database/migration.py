from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relationship
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import psycopg2
import os
from .database import DBIsConnected

load_dotenv()

Base = declarative_base()

def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname='postgres',
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT')
    )
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {os.getenv('DATABASE_NAME')}")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {os.getenv('DATABASE_NAME')} already exists.")
    cursor.close()
    conn.close()

class Oracle(Base):
    __tablename__ = 'oracle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Type(Base):
    __tablename__ = 'type'
    id_type = Column(Enum('farmer', 'seller', 'producer', 'carrier', name='type_enum'), primary_key=True)
    default_co2_value = Column(Float, nullable=False, unique=True)
    standard = Column(Float, nullable=False)

class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    ragione_sociale = Column(String, nullable=False)
    description = Column(String, nullable=False)
    partita_iva = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    cap = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    type = Column(Enum('farmer', 'seller', 'producer', 'carrier', name='type_enum'), ForeignKey('type.id_type'), nullable=False)
    coin = Column(Float, nullable=False)
    
class Employer(Base):
    __tablename__ = 'employer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    id_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum('raw material', 'end product', name='product_type_enum'), nullable=False)
    quantity = Column(Integer, nullable=False)
    id_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)

class Delivery(Base):
    __tablename__ = 'delivery'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    co2_emission = Column(Float, nullable=False)
    id_deliver_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    id_receive_organization = Column(Integer, ForeignKey('organization.id'), nullable=False)
    date_timestamp = Column(DateTime, nullable=False, default=datetime.now)

def init_db():
    create_database_if_not_exists()
    db_instance = DBIsConnected.get_instance()
    Base.metadata.create_all(bind=db_instance.engine)