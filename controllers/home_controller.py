from flask import render_template
from database.migration import init_db
from database.seeder import run_seeders
from sqlalchemy.sql import func
import logging
from controllers.ethereum_controller import assign_addresses_to_organizations
from algorithms.coins_algorithm import initialize_organization_coins_for_all
from controllers.ethereum_controller import deploy_contract
from utilities.utilities import get_db_session, get_random_organizations, get_random_products, get_product_details

def home():
    # Visualizza la home page con organizzazioni e prodotti casuali
    session_db = get_db_session()
    organizations = get_random_organizations(session_db)
    products = get_random_products(session_db)

    # Ottiene i dettagli dei prodotti
    products_with_details = [get_product_details(session_db, product) for product in products]

    session_db.close()
    return render_template("home.html", organizations=organizations, products_with_details=products_with_details)

def initialize_database():
    # Inizializza il database e popola con dati iniziali
    try:
        # Inizializza il database (drop e create tabelle)
        init_db()
        print("Database and tables initialized!")

        # Esegui i seeders per popolare il database con dati iniziali
        run_seeders()
        print("Database seeded successfully!")

        # Distribuisci il contratto
        deploy_contract()
        print('Contract deployed successfully!')

        session_db = get_db_session()

        # Assegna indirizzi Ethereum alle organizzazioni
        assign_addresses_to_organizations(session_db)
        # Inizializza i coin delle organizzazioni sulla blockchain
        initialize_organization_coins_for_all(session_db)

        session_db.close()
    except Exception as e:
        logging.error(f"Error : {e}")
        print(f"Error: {e}")