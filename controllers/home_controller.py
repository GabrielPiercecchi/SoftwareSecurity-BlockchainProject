from flask import render_template
from database.migration import init_db
from database.seeder import run_seeders
from database.database import DBIsConnected
from database.migration import Organization, Product
from sqlalchemy.sql import func

def home():
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    organizations = session_db.query(Organization).filter_by(status='active').order_by(func.random()).limit(10).all()
    products = session_db.query(Product).order_by(func.random()).limit(10).all()

    products_with_details = []
    for product in products:
        product_with_details = {
            "id": product.id,
            "name": product.name,
            'type': product.type,
            "organization_name": session_db.query(Organization).filter_by(id=product.id_organization).first().name,
        }
        products_with_details.append(product_with_details)

    session_db.close()
    return render_template("home.html", organizations=organizations, products_with_details=products_with_details)

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