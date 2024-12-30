from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import psycopg2
import os

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

def init_db():
    create_database_if_not_exists()
    DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)   