import os
from flask import Flask
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from database.migration import init_db
from database.seeder import run_seeders
from controllers.logging_controller import setup_logging
from controllers.home_controller import home, initialize_database
from controllers.organizations_controller import organization_detail, get_all_organizations
from controllers.products_controller import product_detail, get_all_products
from controllers.auth_controller import login, logout, signup, add_employers_to_existing_org
from controllers.users_controller import employer_home

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configura il logging
app_logger = setup_logging()

app = Flask(__name__)
# Configura la chiave segreta per la sicurezza delle sessioni e dei token CSRF
app.secret_key = os.getenv('SECRET_KEY')  # Carica la chiave segreta dall'ambiente
# Abilita la protezione CSRF
csrf = CSRFProtect(app)
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

@app.route("/login", methods=['GET', 'POST'])
def login_route():
    return login()

@app.route("/signup", methods=['GET', 'POST'])
def signup_route():
    return signup()

@app.route("/add_employers", methods=['GET', 'POST'])
def add_employers_route():
    return add_employers_to_existing_org()

@app.route("/logout")
def logout_route():
    return logout()

@app.route("/employer/")
def employer_home_route():
    return employer_home()

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)