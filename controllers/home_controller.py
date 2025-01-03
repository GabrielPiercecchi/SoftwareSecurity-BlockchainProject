from flask import render_template
from database.migration import init_db
from database.seeder import run_seeders
from database.database import DBIsConnected
from database.migration import Organization, Product

def home():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    organizations = session.query(Organization).limit(10).all()
    products = session.query(Product).limit(10).all()
    session.close()
    return render_template("home.html", organizations=organizations, products=products)

def initialize_database():
    try:
        # Initialize the database (drop and create tables)
        init_db()
        print("Database and tables initialized!")

        # Run seeders to populate the database with initial data
        run_seeders()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error: {e}")