from flask import flash, session, redirect, url_for, render_template
from web3 import Web3
from database.database import DBIsConnected
from contract.deploy import ContractInteractions
from database.migration import Organization, Employer
import os
from datetime import datetime

NONCE_FILE = './algorithms/nonce.txt'

class CoinsAlgorithm:
    def __init__(self):
        self.contract_interactions = ContractInteractions()
        self.coin_contract = self.initialize_contract()
        self.nonce = self._initialize_nonce()

    def initialize_contract(self):

        # Leggi l'indirizzo del contratto distribuito
        try:
            with open('contract/contract_address.txt', 'r') as file:
                contract_address = file.read().strip()
                contract_address = Web3.to_checksum_address(contract_address)  # Converti l'indirizzo in formato checksum
        except FileNotFoundError:
            print("Contract address file not found. Ensure the contract is deployed.")
            raise Exception("Contract address file not found. Ensure the contract is deployed.")
        except ValueError as e:
            print(f"Invalid contract address: {e}")
            raise Exception(f"Invalid contract address: {e}")

        # Ottieni l'istanza del contratto
        print(f'Contract address: {contract_address}')
        return self.contract_interactions.get_contract(contract_address)

        # Mantieni traccia del nonce
        # nonce = contract_interactions.w3.eth.get_transaction_count(contract_interactions.my_address, 'pending')
    
    def _initialize_nonce(self):
        nonce = self.read_nonce()
        if nonce is None:
            nonce = self.contract_interactions.w3.eth.get_transaction_count(self.contract_interactions.my_address, 'pending')
            self.write_nonce(nonce)
        return nonce
    
    @staticmethod
    def read_nonce():
        if os.path.exists(NONCE_FILE):
            with open(NONCE_FILE, 'r') as file:
                return int(file.read().strip())
        return None

    @staticmethod
    def write_nonce(nonce):
        with open(NONCE_FILE, 'w') as file:
            file.write(str(nonce))

    ########################################################################################
    def get_coins_from_blockchain(self, blockchain_address):
        try:
            coins = self.coin_contract.functions.getBalance(blockchain_address).call()
            print(f"Balance on blockchain for {blockchain_address}: {coins}")
            return coins
        except Exception as e:
            print(f'Error getting coins from blockchain: {e}')
            raise
    ########################################################################################

    def increment_nonce(self):
        self.nonce += 1
        self.write_nonce(self.nonce)

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
        # Converti il valore dei coin in un intero
        coin_value = int(organization.coin)
        # Invia una transazione al contratto intelligente per inizializzare i coin
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
            manager.increment_nonce()  # Incrementa il nonce
            print(f'Organization coins initialized successfully: {tx_hash.hex()}')
            return True
        else:
            print('Failed to initialize organization coins')
            return False
    except Exception as e:
        print(f'Error initializing organization coins: {e}')
        return False

def coins_algorithm(co2_emission, co2_limit, organization, session_db):
    manager = CoinsAlgorithm()
    print("coins_algorithm called")
    try:
        # Ottieni il valore dei coin dalla blockchain
        blockchain_coins = manager.get_coins_from_blockchain(organization.blockchain_address)
        print(f'Blockchain coins: {blockchain_coins}, Database coins: {organization.coin}')

        # Confronta il valore dei coin nel database con quello sulla blockchain
        if int(organization.coin) != int(blockchain_coins):
            flash('Coin discrepancy detected between database and blockchain', 'error')
            print('Coin discrepancy detected between database and blockchain')
            return False

        # Invia una transazione al contratto intelligente
        print(f'Nonce: {manager.nonce}')
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
        print(f'Transaction: {tx}')
        signed_tx = manager.contract_interactions.w3.eth.account.sign_transaction(tx, private_key=manager.contract_interactions.private_key)
        print(f'Signed transaction: {signed_tx}')
        tx_hash = manager.contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f'Transaction hash: {tx_hash.hex()}')
        receipt = manager.contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Transaction receipt: {receipt}')
        if receipt.status == 1:
            print(f'Transaction successful: {tx_hash.hex()}')
            manager.increment_nonce()  # Incrementa il nonce

            # Aggiorna i valori nel database
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
            manager.increment_nonce()  # Incrementa il nonce
            return False

        # if co2_emission > co2_limit:
        #     malus_coin = int(co2_emission - co2_limit)
        #     organization.coin -= malus_coin
        #     if organization.coin < 0:
        #         flash(f'CO2 emission exceeds the limit. You need { (organization.coin*-1) } more coin', 'error_co2')
        #         return False
        #     else:
        #         session_db.add(organization)
        #         # Invia una transazione al contratto intelligente
        #         print(f'Nonce: {nonce}')
        #         tx = coin_contract.functions.updateCoins(organization.blockchain_address, -malus_coin).build_transaction({
        #             'chainId': contract_interactions.chain_id,
        #             'gas': 2000000,
        #             'gasPrice': contract_interactions.w3.eth.gas_price,
        #             'nonce': nonce,
        #         })
        #         print(f'Transaction: {tx}')
        #         signed_tx = contract_interactions.w3.eth.account.sign_transaction(tx, private_key=contract_interactions.private_key)
        #         print(f'Signed transaction: {signed_tx}')
        #         tx_hash = contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        #         print(f'Transaction hash: {tx_hash.hex()}')
        #         receipt = contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        #         print(f'Transaction receipt: {receipt}')
        #         if receipt.status == 1:
        #             print(f'Transaction successful: {tx_hash.hex()}')
        #             nonce += 1  # Incrementa il nonce
        #             return True
        #         else:
        #             flash('Transaction failed', 'error')
        #             return False
        # else:
        #     bonus_coin = int(co2_limit - co2_emission)
        #     organization.coin += bonus_coin
        #     session_db.add(organization)
        #     # Invia una transazione al contratto intelligente
        #     print(f'Nonce: {nonce}')
        #     tx = coin_contract.functions.updateCoins(organization.blockchain_address, bonus_coin).build_transaction({
        #         'chainId': contract_interactions.chain_id,
        #         'gas': 2000000,
        #         'gasPrice': contract_interactions.w3.eth.gas_price,
        #         'nonce': nonce,
        #     })
        #     print(f'Transaction: {tx}')
        #     signed_tx = contract_interactions.w3.eth.account.sign_transaction(tx, private_key=contract_interactions.private_key)
        #     print(f'Signed transaction: {signed_tx}')
        #     tx_hash = contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        #     print(f'Transaction hash: {tx_hash.hex()}')
        #     receipt = contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
        #     print(f'Transaction receipt: {receipt}')
        #     if receipt.status == 1:
        #         print(f'Transaction successful: {tx_hash.hex()}')
        #         nonce += 1  # Incrementa il nonce
        #         return True
        #     else:
        #         flash('Transaction failed', 'error')
        #         return False
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        print(f'An error occurred: {str(e)}')
        return False
    
def update_organization_coins_on_blockchain(organization, organization_requesting, coin_request, session_db):
    manager = CoinsAlgorithm()
    try:
        # Ottieni il valore dei coin dalla blockchain
        blockchain_coins_org_del = manager.get_coins_from_blockchain(organization.blockchain_address)
        print(f'Blockchain coins: {blockchain_coins_org_del}, Database coins: {organization.coin}')

        blockchain_coins_org_req = manager.get_coins_from_blockchain(organization_requesting.blockchain_address)
        print(f'Blockchain coins: {blockchain_coins_org_req}, Database coins: {organization_requesting.coin}')

        # Confronta il valore dei coin nel database con quello sulla blockchain
        if int(organization.coin) != int(blockchain_coins_org_del):
            flash(f'Coin discrepancy detected between database and blockchain for {organization.name}', 'error')
            print(f'Coin discrepancy detected between database and blockchain for delivering organization')
            return False

        # Confronta il valore dei coin nel database con quello sulla blockchain
        if int(organization_requesting.coin) != int(blockchain_coins_org_req):
            flash(f'Coin discrepancy detected between database and blockchain for {organization_requesting.name}', 'error')
            print(f'Coin discrepancy detected between database and blockchain for requesting organization')
            return False

        # Aggiorna i coin dell'organizzazione che fornisce
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
            manager.increment_nonce() # Incrementa il nonce
            flash('Coins updated successfully for providing organization', 'success')
            print(f'Coins updated successfully for providing organization: {tx_hash.hex()}')
        else:
            flash('Failed to update coins for providing organization', 'error')
            print('Failed to update coins for providing organization')
            manager.increment_nonce()  # Incrementa il nonce
            return False

        # Aggiorna i coin dell'organizzazione richiedente
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
            manager.increment_nonce()  # Incrementa il nonce
            flash('Coins updated successfully for requesting organization', 'success')
            print(f'Coins updated successfully for requesting organization: {tx_hash.hex()}')

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
            print('Failed to update coins for requesting organization')
            manager.increment_nonce()  # Incrementa il nonce
            return False
    except Exception as e:
        flash(f'Error updating organization coins on blockchain: {e}', 'error')
        print(f'Error updating organization coins on blockchain: {e}')
        return False

def view_transactions():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    manager = CoinsAlgorithm()
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    
    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()

    try:
        orgs, amounts, timestamps = manager.coin_contract.functions.getTransactions(organization.blockchain_address).call()
        transactions = []
        for i in range(len(orgs)):
            transactions.append({
                'organization': orgs[i],
                'amount': amounts[i],
                'timestamp': timestamps[i]
            })
        return render_template('employer_view_transactions.html', transactions=transactions, organization=organization)
    except Exception as e:
        session_db.close()
        flash('Error while getting transactions', 'error')
        print(f'Error: {e}')
        return redirect(url_for('view_transactions_route'))   