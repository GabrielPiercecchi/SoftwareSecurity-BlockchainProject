import os
from web3 import Web3
from database.migration import Organization
from dotenv import load_dotenv

load_dotenv()

# Configura la connessione a Web3
w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_URL')))

def generate_ethereum_address():
    account = w3.eth.account.create()
    return account.address

def assign_addresses_to_organizations(session):
    organizations = session.query(Organization).all()
    for organization in organizations:
        if not organization.blockchain_address:
            address = generate_ethereum_address()
            organization.blockchain_address = address
            print(f"Assigned address {address} to organization {organization.name}")
    session.commit()