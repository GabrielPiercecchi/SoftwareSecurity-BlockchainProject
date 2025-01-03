from flask import Flask
from flask_talisman import Talisman
from database.migration import init_db
from database.seeder import run_seeders
from controllers.logging_controller import setup_logging
from controllers.home_controller import home, initialize_database
from controllers.organizations_controller import organization_detail, get_all_organizations
from controllers.products_controller import product_detail, get_all_products

# Configura il logging
app_logger = setup_logging()

app = Flask(__name__)
Talisman(app)

@app.before_request
def log_request_info():
    app_logger.info('Request received')

@app.route("/")
def home_route():
    return home()

@app.route("/organizations")
def organizations_route():
    return get_all_organizations()

@app.route("/organization/<int:id>")
def organization_detail_route(id):
    return organization_detail(id)

@app.route("/products")
def products_route():
    return get_all_products()

@app.route("/product/<int:id>")
def product_detail_route(id):
    return product_detail(id)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)