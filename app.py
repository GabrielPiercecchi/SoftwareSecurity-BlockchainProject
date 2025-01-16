import os
from flask import Flask, request
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from database.migration import init_db
from database.seeder import run_seeders
from controllers.logging_controller import setup_logging
from controllers.home_controller import home, initialize_database
from controllers.organizations_controller import organization_detail, get_all_organizations
from controllers.products_controller import product_detail, get_all_products, employer_view_products, update_product
from controllers.auth_controller import login, logout, signup, add_employers_to_existing_org
from controllers.products_controller import create_product
from controllers.employers_controller import employer_home, employer_update_personal_data
from controllers.deliveries_controller import employer_view_deliveries, carrier_view_deliveries
from controllers.product_requests_controller import menage_product_requests, view_other_products, create_product_requests, deny_product_request, accept_product_request, carrier_menage_product_requests, carrier_accept_and_create_delivery
from controllers.oracle_controller import approve_employer, manage_employer_registration, oracle_home, reject_employer, view_employer_inactive, view_organization_inactive, manage_organization_registration, approve_organization, reject_organization, oracle_coin_transfer, oracle_view_organizations
from controllers.coin_requests_controller import view_coin_requests, create_coin_request, accept_coin_request, view_accepted_coin_requests

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)
# Configura la chiave segreta per la sicurezza delle sessioni e dei token CSRF
app.secret_key = os.getenv('SECRET_KEY')  # Carica la chiave segreta dall'ambiente
# Abilita la protezione CSRF
csrf = CSRFProtect(app)
Talisman(app)

# Configura il logging
setup_logging(app)

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

@app.route('/employer_update_personal_data', methods=['GET', 'POST'])
def employer_update_personal_data_route():
    return employer_update_personal_data()

@app.route("/create_products", methods=['GET', 'POST'])
def create_product_route():
    return create_product()

@app.route("/employer/view_products/")
def employer_view_products_route():
    return employer_view_products()

@app.route("/update_product/<int:product_id>", methods=['GET', 'POST'])
def update_product_route(product_id):
    return update_product(product_id)

@app.route("/employer/view_deliveries/")
def employer_view_deliveries_route():
    return employer_view_deliveries()

@app.route("/employer/menage_product_requests")
def menage_product_requests_route():
    return menage_product_requests()

@app.route("/employer/menage_product_requests/view_other_products/")
def view_other_products_route():
    return view_other_products()

@app.route("/employer/menage_product_requests/accept_product_requests", methods=['GET', 'POST'])
def accept_product_request_route():
    return accept_product_request()

@app.route("/employer/menage_product_requests/deny_product_request", methods=['GET', 'POST'])
def deny_product_request_route():
    return deny_product_request()

@app.route("/employer/menage_product_requests/view_other_products/create_product_requests/<int:product_id>", methods=['GET', 'POST'])
def create_product_requests_route(product_id):
    return create_product_requests(product_id)

@app.route("/employer/carrier_menage_product_requests")
def carrier_menage_product_requests_route():
    return carrier_menage_product_requests()

@app.route("/employer/carrier_menage_product_requests/carrier_accept_and_create_delivery", methods=['GET', 'POST'])
def carrier_accept_and_create_delivery_route():
    return carrier_accept_and_create_delivery()

@app.route("/employer/carrier_view_deliveries/")
def carrier_view_deliveries_route():
    return carrier_view_deliveries()

@app.route("/employer/view_coin_requests/")
def view_coin_requests_route():
    return view_coin_requests()

@app.route("/employer/view_coin_requests/view_accepted_coin_requests/")
def view_accepted_coin_requests_route():
    return view_accepted_coin_requests()

@app.route("/employer/view_coin_requests/create_coin_request/", methods=['GET', 'POST'])
def create_coin_request_route():
    return create_coin_request()

@app.route("/employer/view_coin_requests/accept_coin_request", methods=['GET', 'POST'])
def accept_coin_request_route():
    return accept_coin_request()

@app.route("/oracle/")
def oracle_home_route():
    return oracle_home()

@app.route("/oracle_view_organizations/")
def oracle_view_organizations_route():
    return oracle_view_organizations()

@app.route("/oracle/view_organization_inactive")
def view_organization_inactive_route():
    return view_organization_inactive()

@app.route("/oracle/view_employer_inactive")
def view_employer_inactive_route():
    return view_employer_inactive()

@app.route("/oracle/view_organization_inactive/manage_organization_registration/<int:organization_id>")
def manage_organization_registration_route(organization_id):
    return manage_organization_registration(organization_id)

@app.route("/oracle/view_organization_inactive/approve_organization/<int:organization_id>", methods=['POST'])
def approve_organization_route(organization_id):
    return approve_organization(organization_id)

@app.route("/oracle/view_organization_inactivereject_organization/<int:organization_id>", methods=['POST'])
def reject_organization_route(organization_id):
    return reject_organization(organization_id)

@app.route("/oracle/view_employer_inactive/manage_employer_registration/<int:employer_id>")
def manage_employer_registration_route(employer_id):
    return manage_employer_registration(employer_id)

@app.route("/oracle/view_employer_inactive/approve_employer/<int:employer_id>", methods=['POST'])
def approve_employer_route(employer_id):
    return approve_employer(employer_id)

@app.route("/oracle/view_employer_inactive/reject_employer/<int:employer_id>", methods=['POST'])
def reject_employer_route(employer_id):
    return reject_employer(employer_id)

@app.route("/oracle/coin_transfer/<int:organization_id>", methods=['GET', 'POST'])
def oracle_coin_transfer_route(organization_id):
    return oracle_coin_transfer(organization_id)

if __name__ == "__main__":
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        # Inizializza il database e altri setup qui
        initialize_database()
    app.run(host=(os.getenv('HOST')), port=(os.getenv('PORT')), debug=True)