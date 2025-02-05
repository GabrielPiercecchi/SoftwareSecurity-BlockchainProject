from flask import flash, session, redirect, url_for, render_template
from web3 import Web3
from contract.deploy import ContractInteractions
from database.migration import Organization
from datetime import datetime
from utilities.utilities import read_nonce, write_nonce, get_db_session, get_organization_by_id, get_employer_by_username, epoch_to_datetime
import logging
from messages.messages import (
    CONTRACT_ADDRESS_FILE_NOT_FOUND, INVALID_CONTRACT_ADDRESS, ERROR_GETTING_COINS,
    COIN_DISCREPANCY_DETECTED, CO2_EMISSION_EXCEEDS_LIMIT, TRANSACTION_FAILED, ERROR_IN_COINS_ALGORITHM,
    FAILED_TO_UPDATE_COINS_PROVIDING, FAILED_TO_UPDATE_COINS_REQUESTING, ERROR_UPDATING_COINS, ERROR_GETTING_TRANSACTIONS
)

class CoinsAlgorithm:
    def __init__(self):
        self.contract_interactions = ContractInteractions()
        self.coin_contract = self.initialize_contract()
        self.nonce = self._initialize_nonce()

    def initialize_contract(self):
        try:
            # Legge l'indirizzo del contratto dal file e lo converte in checksum address
            with open('contract/contract_address.txt', 'r') as file:
                contract_address = file.read().strip()
                contract_address = Web3.to_checksum_address(contract_address)
        except FileNotFoundError:
            logging.error(CONTRACT_ADDRESS_FILE_NOT_FOUND)
            raise Exception(CONTRACT_ADDRESS_FILE_NOT_FOUND)
        except ValueError as e:
            logging.error(INVALID_CONTRACT_ADDRESS.format(e))
            raise Exception(INVALID_CONTRACT_ADDRESS.format(e))

        # Ottiene il contratto utilizzando l'indirizzo letto
        return self.contract_interactions.get_contract(contract_address)

    def _initialize_nonce(self):
        # Legge il nonce dal file, se non esiste lo ottiene dalla blockchain e lo scrive nel file
        nonce = read_nonce()
        if nonce is None:
            nonce = self.contract_interactions.w3.eth.get_transaction_count(self.contract_interactions.my_address, 'pending')
            write_nonce(nonce)
        return nonce

    def get_coins_from_blockchain(self, blockchain_address):
        try:
            # Ottiene il saldo di coin dall'indirizzo blockchain
            coins = self.coin_contract.functions.getBalance(blockchain_address).call()
            return coins
        except Exception as e:
            logging.error(ERROR_GETTING_COINS.format(e))
            raise Exception(ERROR_GETTING_COINS.format(e))

    def increment_nonce(self):
        # Incrementa il nonce e lo scrive nel file
        self.nonce += 1
        write_nonce(self.nonce)

# Inizializza i coin per tutte le organizzazioni nel database
def initialize_organization_coins_for_all(session_db):
    manager = CoinsAlgorithm()
    organizations = session_db.query(Organization).all()
    for org in organizations:
        if not initialize_organization_coins(manager, org):
            print(f'Failed to initialize coins for organization {org.name}')
        else:
            print(f'Coins initialized for organization {org.name}')

# Inizializza i coin per una singola organizzazione
def initialize_organization_coins(manager, organization):
    manager = CoinsAlgorithm()
    try:
        coin_value = int(organization.coin)
        
        # Costruisce la transazione per aggiornare i coin
        tx = manager.coin_contract.functions.updateCoins(organization.blockchain_address, coin_value).build_transaction({
            'chainId': manager.contract_interactions.chain_id,
            'gas': 2000000,
            'gasPrice': manager.contract_interactions.w3.eth.gas_price,
            'nonce': manager.nonce,
        })
        # Firma e invia la transazione
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            manager.increment_nonce()
            return True
        else:
            manager.increment_nonce()
            return False
    except Exception as e:
        logging.error(f'Error initializing organization coins: {e}')
        print(f'Error initializing organization coins: {e}')
        return False

# Algoritmo per aggiornare i coin basato sulle emissioni di CO2
def coins_algorithm(co2_emission, co2_limit, organization, session_db, product_name, product_quantity):
    manager = CoinsAlgorithm()
    try:
        # Ottiene il saldo di coin dalla blockchain e lo confronta con il database
        blockchain_coins = manager.get_coins_from_blockchain(organization.blockchain_address)
        if int(organization.coin) != int(blockchain_coins):
            organization.coin = int(blockchain_coins)
            session_db.add(organization)
            session_db.commit()
            flash(COIN_DISCREPANCY_DETECTED, 'error')
            return False

        # Costruisce la transazione per aggiornare i coin basato sulle emissioni di CO2
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
        # Firma e invia la transazione
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            manager.increment_nonce()
            if co2_emission > co2_limit:
                malus_coin = int(co2_emission - co2_limit)
                organization.coin -= malus_coin
                if organization.coin < 0:
                    flash(CO2_EMISSION_EXCEEDS_LIMIT.format((organization.coin*-1)), 'error_co2')
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
            manager.increment_nonce()
            flash(TRANSACTION_FAILED.format(int((organization.coin - co2_emission + co2_limit)*-1)), 'error')
            register_rejected_transaction(manager, organization, int(co2_emission - co2_limit), "Transaction failed", product_name, product_quantity, co2_emission)
            return False
    except Exception as e:
        logging.error(ERROR_IN_COINS_ALGORITHM.format(e))
        flash(ERROR_IN_COINS_ALGORITHM.format(e), 'error')
        return False

# Aggiorna i coin tra due organizzazioni sulla blockchain
def update_organization_coins_on_blockchain(organization, organization_requesting, coin_request, session_db):
    manager = CoinsAlgorithm()
    try:
        # Ottiene il saldo di coin dalla blockchain e lo confronta con il database
        blockchain_coins_org_del = manager.get_coins_from_blockchain(organization.blockchain_address)
        blockchain_coins_org_req = manager.get_coins_from_blockchain(organization_requesting.blockchain_address)

        if int(organization.coin) != int(blockchain_coins_org_del):
            organization.coin = int(blockchain_coins_org_del)
            session_db.add(organization)
            session_db.commit()
            flash(COIN_DISCREPANCY_DETECTED.format(organization.name), 'error')
            return False

        if int(organization_requesting.coin) != int(blockchain_coins_org_req):
            organization_requesting.coin = int(blockchain_coins_org_req)
            session_db.add(organization_requesting)
            session_db.commit()
            flash(COIN_DISCREPANCY_DETECTED.format(organization_requesting.name), 'error')
            return False

        # Costruisce la transazione per aggiornare i coin dell'organizzazione che fornisce
        tx = manager.coin_contract.functions.updateCoins(organization.blockchain_address, -int(coin_request.coin)).build_transaction({
            'chainId': manager.contract_interactions.chain_id,
            'gas': 2000000,
            'gasPrice': manager.contract_interactions.w3.eth.gas_price,
            'nonce': manager.nonce,
        })
        # Firma e invia la transazione
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            manager.increment_nonce()
        else:
            flash(FAILED_TO_UPDATE_COINS_PROVIDING, 'error')
            manager.increment_nonce()
            return False

        # Costruisce la transazione per aggiornare i coin dell'organizzazione che riceve
        tx = manager.coin_contract.functions.updateCoins(organization_requesting.blockchain_address, int(coin_request.coin)).build_transaction({
            'chainId': manager.contract_interactions.chain_id,
            'gas': 2000000,
            'gasPrice': manager.contract_interactions.w3.eth.gas_price,
            'nonce': manager.nonce,
        })
        # Firma e invia la transazione
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
            flash(FAILED_TO_UPDATE_COINS_REQUESTING, 'error')
            manager.increment_nonce()
            return False
    except Exception as e:
        logging.error(ERROR_UPDATING_COINS.format(e))
        flash(ERROR_UPDATING_COINS.format(e), 'error')
        return False

# Visualizza le transazioni per l'organizzazione dell'utente corrente
def view_transactions():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    manager = CoinsAlgorithm()
    session_db = get_db_session()
    
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_id(session_db, employer.id_organization)

    try:
        # Ottiene le transazioni dalla blockchain
        orgs, amounts, timestamps, txHashes = manager.coin_contract.functions.getTransactions(organization.blockchain_address).call()
        transactions = []
        for i in range(len(orgs)):
            transactions.append({
                'organization': orgs[i],
                'amount': amounts[i],
                'timestamp': epoch_to_datetime(timestamps[i]),
                'txHash': txHashes[i]
            })
        session_db.close()
        return render_template('employer_view_transactions.html', transactions=transactions, organization=organization)
    except Exception as e:
        session_db.close()
        logging.error(ERROR_GETTING_TRANSACTIONS.format(e))
        flash(ERROR_GETTING_TRANSACTIONS.format(e), 'error')
        return redirect(url_for('employer_home_route'))

# Registra una transazione rifiutata sulla blockchain
def register_rejected_transaction(manager, organization, amount, reason, product_name, product_quantity, co2_emission):
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    manager = CoinsAlgorithm()

    # Costruisce la transazione per registrare la transazione rifiutata
    tx = manager.coin_contract.functions.registerRejectedTransaction(
        organization.blockchain_address,
        amount,
        reason,
        product_name,
        product_quantity,
        co2_emission
    ).build_transaction({
        'chainId': manager.contract_interactions.chain_id,
        'gas': 2000000,
        'gasPrice': manager.contract_interactions.w3.eth.gas_price,
        'nonce': manager.nonce,
    })
    # Firma e invia la transazione
    signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
    manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    manager.increment_nonce()

# Visualizza le transazioni rifiutate per l'organizzazione dell'utente corrente
def view_rejected_transactions():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    manager = CoinsAlgorithm()
    session_db = get_db_session()
    
    employer = get_employer_by_username(session_db, username)
    organization = get_organization_by_id(session_db, employer.id_organization)

    try:
        # Ottiene i dettagli delle transazioni rifiutate dalla blockchain
        rejected_orgs, rejected_amounts, rejected_timestamps, rejected_reasons = manager.coin_contract.functions.getRejectedTransactionDetails1(organization.blockchain_address).call()
        rejected_product_names, rejected_product_quantities, rejected_co2_emissions, rejected_tx_hashes = manager.coin_contract.functions.getRejectedTransactionDetails2(organization.blockchain_address).call()
        
        rejected_transactions = []
        for i in range(len(rejected_orgs)):
            rejected_transactions.append({
                'organization': rejected_orgs[i],
                'amount': rejected_amounts[i],
                'timestamp': epoch_to_datetime(rejected_timestamps[i]),
                'reason': rejected_reasons[i],
                'product_name': rejected_product_names[i],
                'product_quantity': rejected_product_quantities[i],
                'co2_emission': rejected_co2_emissions[i],
                'tx_hash': rejected_tx_hashes[i]
            })
        session_db.close()
        return render_template('employer_view_rejected_transactions.html', rejected_transactions=rejected_transactions, organization=organization)
    except Exception as e:
        session_db.close()
        logging.error(ERROR_GETTING_TRANSACTIONS.format(e))
        flash(ERROR_GETTING_TRANSACTIONS.format(e), 'error')
        return redirect(url_for('employer_home_route'))