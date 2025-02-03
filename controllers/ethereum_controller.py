import os
from web3 import Web3
from flask import redirect, url_for, session, flash, render_template
from database.migration import Organization
from dotenv import load_dotenv
from contract.deploy import ContractInteractions

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configura la connessione a Web3
w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_URL')))

def generate_ethereum_address():
    # Genera un nuovo indirizzo Ethereum
    account = w3.eth.account.create()
    return account.address

def assign_addresses_to_organizations(session_db):
    # Assegna indirizzi Ethereum alle organizzazioni che non ne hanno uno
    organizations = session_db.query(Organization).all()
    for organization in organizations:
        if not organization.blockchain_address:
            address = generate_ethereum_address()
            organization.blockchain_address = address
            print(f"Assigned address {address} to organization {organization.name}")
    session_db.commit()

def deploy_contract():
    # Distribuisce il contratto sulla blockchain
    contract_interactions = ContractInteractions()
    contract_address = contract_interactions.deploy_contract()
    print(f'Contract deployed at address: {contract_address}')