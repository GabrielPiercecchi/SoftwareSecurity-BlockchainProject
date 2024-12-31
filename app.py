from flask import Flask, render_template
from flask_talisman import Talisman
from database.migration import init_db
from database.seeder import run_seeders
from database.database import DBIsConnected
from database.migration import Organization, Product, Employer, Delivery

app = Flask(__name__)
Talisman(app)

@app.route("/")
def home():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    organizations = session.query(Organization).limit(10).all()
    products = session.query(Product).limit(10).all()
    session.close()
    return render_template("home.html", organizations=organizations, products=products)

@app.route("/organization/<int:id>")
def organization_detail(id):
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    organization = session.query(Organization).get(id)
    employers = session.query(Employer).filter_by(id_organization=id).all()
    session.close()
    return render_template("organization_detail.html", organization=organization, employers=employers)

@app.route("/product/<int:id>")
def product_detail(id):
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    product = session.query(Product).get(id)
    deliveries = session.query(Delivery).filter_by(id_product=id).all()
    organization = session.query(Organization).get(product.id_organization)
    session.close()
    return render_template("product_detail.html", product=product, deliveries=deliveries, organization=organization)

if __name__ == "__main__":
    try:
        # Initialize the database (drop and create tables)
        init_db()
        print("Database and tables initialized!")

        # Run seeders to populate the database with initial data
        run_seeders()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error: {e}")
    app.run(debug=True)
