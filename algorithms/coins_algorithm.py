from flask import flash, session, redirect, url_for, render_template
from web3 import Web3
from contract.deploy import ContractInteractions
from database.migration import Organization
from datetime import datetime
from utilities.utilities import read_nonce, write_nonce, get_db_session, get_organization_by_id, get_employer_by_username
import logging

class CoinsAlgorithm:
    def __init__(self):
        self.contract_interactions = ContractInteractions()
        self.coin_contract = self.initialize_contract()
        self.nonce = self._initialize_nonce()

    def initialize_contract(self):
        try:
            with open('contract/contract_address.txt', 'r') as file:
                contract_address = file.read().strip()
                contract_address = Web3.to_checksum_address(contract_address)
        except FileNotFoundError:
            logging.error("Contract address file not found. Ensure the contract is deployed.")
            raise Exception("Contract address file not found. Ensure the contract is deployed.")
        except ValueError as e:
            logging.error(f"Invalid contract address: {e}")
            raise Exception(f"Invalid contract address: {e}")

        return self.contract_interactions.get_contract(contract_address)

    def _initialize_nonce(self):
        nonce = read_nonce()
        if nonce is None:
            nonce = self.contract_interactions.w3.eth.get_transaction_count(self.contract_interactions.my_address, 'pending')
            write_nonce(nonce)
        return nonce

    def get_coins_from_blockchain(self, blockchain_address):
        try:
            coins = self.coin_contract.functions.getBalance(blockchain_address).call()
            return coins
        except Exception as e:
            logging.error(f'Error getting coins from blockchain: {e}')
            raise Exception(f'Error getting coins from blockchain: {e}')

    def increment_nonce(self):
        self.nonce += 1
        write_nonce(self.nonce)

def initialize_organization_coins_for_all(session_db):
    manager = CoinsAlgorithm()
    organizations = session_db.query(Organization).all()
    for org in organizations:
        if not initialize_organization_coins(manager, org):
            print(f'Failed to initialize coins for organization {org.name}')
        else:
            print(f'Coins initialized for organization {org.name}')

def initialize_organization_coins(manager, organization):
    try:
        coin_value = int(organization.coin)
        tx = manager.coin_contract.functions.updateCoins(organization.blockchain_address, coin_value).build_transaction({
            'chainId': manager.contract_interactions.chain_id,
            'gas': 2000000,
            'gasPrice': manager.contract_interactions.w3.eth.gas_price,
            'nonce': manager.nonce,
        })
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            manager.increment_nonce()
            return True
        else:
            return False
    except Exception as e:
        logging.error(f'Error initializing organization coins: {e}')
        print(f'Error initializing organization coins: {e}')
        return False

def coins_algorithm(co2_emission, co2_limit, organization, session_db):
    manager = CoinsAlgorithm()
    try:
        blockchain_coins = manager.get_coins_from_blockchain(organization.blockchain_address)
        if int(organization.coin) != int(blockchain_coins):
            flash('Coin discrepancy detected between database and blockchain', 'error')
            return False

        tx = manager.coin_contract.functions.updateCoinsBasedOnEmission(
            organization.blockchain_address,
            int(co2_emission),
            int(co2_limit)
        ).build_transaction({
            'chainId': manager.contract_interactions.chain_id,
            'gas': 2000000,
            'gasPrice': manager.contract_interactions.w3.eth.gas_price,
            'nonce': manager.nonce,
        })
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            manager.increment_nonce()
            if co2_emission > co2_limit:
                malus_coin = int(co2_emission - co2_limit)
                organization.coin -= malus_coin
                if organization.coin < 0:
                    flash(f'CO2 emission exceeds the limit. You need { (organization.coin*-1) } more coin', 'error_co2')
                    return False
                else:
                    session_db.add(organization)
                    session_db.commit()
            else:
                bonus_coin = int(co2_limit - co2_emission)
                organization.coin += bonus_coin
                session_db.add(organization)
                session_db.commit()
            return True
        else:
            flash(f'Transaction failed: CO2 emission exceeds the limit. You need { int((organization.coin - co2_emission + co2_limit)*-1) } more coin', 'error')
            manager.increment_nonce()
            return False
    except Exception as e:
        logging.error(f'Error in coins algorithm: {e}')
        flash(f'An error occurred: {str(e)}', 'error')
        return False

def update_organization_coins_on_blockchain(organization, organization_requesting, coin_request, session_db):
    manager = CoinsAlgorithm()
    try:
        blockchain_coins_org_del = manager.get_coins_from_blockchain(organization.blockchain_address)
        blockchain_coins_org_req = manager.get_coins_from_blockchain(organization_requesting.blockchain_address)

        if int(organization.coin) != int(blockchain_coins_org_del):
            flash(f'Coin discrepancy detected between database and blockchain for {organization.name}', 'error')
            return False

        if int(organization_requesting.coin) != int(blockchain_coins_org_req):
            flash(f'Coin discrepancy detected between database and blockchain for {organization_requesting.name}', 'error')
            return False

        tx = manager.coin_contract.functions.updateCoins(organization.blockchain_address, -int(coin_request.coin)).build_transaction({
            'chainId': manager.contract_interactions.chain_id,
            'gas': 2000000,
            'gasPrice': manager.contract_interactions.w3.eth.gas_price,
            'nonce': manager.nonce,
        })
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            manager.increment_nonce()
        else:
            flash('Failed to update coins for providing organization', 'error')
            manager.increment_nonce()
            return False

        tx = manager.coin_contract.functions.updateCoins(organization_requesting.blockchain_address, int(coin_request.coin)).build_transaction({
            'chainId': manager.contract_interactions.chain_id,
            'gas': 2000000,
            'gasPrice': manager.contract_interactions.w3.eth.gas_price,
            'nonce': manager.nonce,
        })
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            manager.increment_nonce()
            coin_request.status = 'approved'
            coin_request.id_providing_organization = organization.id
            organization.coin = int(organization.coin) - int(coin_request.coin)
            organization_requesting.coin = int(organization_requesting.coin) + int(coin_request.coin)
            coin_request.date_responded = datetime.now()
            session_db.commit()
            session_db.close()
            return True
        else:
            flash('Failed to update coins for requesting organization', 'error')
            manager.increment_nonce()
            return False
    except Exception as e:
        logging.error(f'Error updating organization coins on blockchain: {e}')
        flash(f'Error updating organization coins on blockchain: {e}', 'error')
        return False

def view_transactions():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    manager = CoinsAlgorithm()
    session_db = get_db_session()
    
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_id(session_db, employer.id_organization)

    try:
        orgs, amounts, timestamps, txHashes = manager.coin_contract.functions.getTransactions(organization.blockchain_address).call()
        transactions = []
        for i in range(len(orgs)):
            transactions.append({
                'organization': orgs[i],
                'amount': amounts[i],
                'timestamp': timestamps[i],
                'txHash': txHashes[i]
            })
        session_db.close()
        return render_template('employer_view_transactions.html', transactions=transactions, organization=organization)
    except Exception as e:
        session_db.close()
        logging.error(f'Error while getting transactions: {e}')
        flash(f'Error while getting transactions: {e}', 'error')
        return redirect(url_for('view_transactions_route'))