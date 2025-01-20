from flask import flash
from web3 import Web3
from database.database import DBIsConnected
from contract.deploy import ContractInteractions

# Variabili globali
contract_interactions = None
coin_contract = None
nonce = None

def initialize_contract():
    global contract_interactions, coin_contract, nonce
    contract_interactions = ContractInteractions()

    # Leggi l'indirizzo del contratto distribuito
    try:
        with open('contract/contract_address.txt', 'r') as file:
            contract_address = file.read().strip()
            contract_address = Web3.to_checksum_address(contract_address)  # Converti l'indirizzo in formato checksum
    except FileNotFoundError:
        raise Exception("Contract address file not found. Ensure the contract is deployed.")
    except ValueError as e:
        raise Exception(f"Invalid contract address: {e}")

    # Ottieni l'istanza del contratto
    print(f'Contract address: {contract_address}')
    coin_contract = contract_interactions.get_contract(contract_address)

    # Mantieni traccia del nonce
    nonce = contract_interactions.w3.eth.get_transaction_count(contract_interactions.my_address, 'pending')

def coins_algorithm(co2_emission, co2_limit, organization, session_db):
    global nonce  # Usa la variabile globale nonce
    if contract_interactions is None or coin_contract is None or nonce is None:
        initialize_contract()
    try:
        if co2_emission > co2_limit:
            malus_coin = int(co2_emission - co2_limit)
            organization.coin -= malus_coin
            if organization.coin < 0:
                flash(f'CO2 emission exceeds the limit. You need { (organization.coin*-1) } more coin', 'error_co2')
                return False
            else:
                session_db.add(organization)
                # Invia una transazione al contratto intelligente
                print(f'Nonce: {nonce}')
                tx = coin_contract.functions.updateCoins(organization.blockchain_address, -malus_coin).build_transaction({
                    'chainId': contract_interactions.chain_id,
                    'gas': 2000000,
                    'gasPrice': contract_interactions.w3.eth.gas_price,
                    'nonce': nonce,
                })
                print(f'Transaction: {tx}')
                signed_tx = contract_interactions.w3.eth.account.sign_transaction(tx, private_key=contract_interactions.private_key)
                print(f'Signed transaction: {signed_tx}')
                tx_hash = contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                print(f'Transaction hash: {tx_hash.hex()}')
                receipt = contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
                print(f'Transaction receipt: {receipt}')
                if receipt.status == 1:
                    nonce += 1  # Incrementa il nonce
                    return True
                else:
                    flash('Transaction failed', 'error')
                    return False
        else:
            bonus_coin = int(co2_limit - co2_emission)
            organization.coin += bonus_coin
            session_db.add(organization)
            # Invia una transazione al contratto intelligente
            print(f'Nonce: {nonce}')
            tx = coin_contract.functions.updateCoins(organization.blockchain_address, bonus_coin).build_transaction({
                'chainId': contract_interactions.chain_id,
                'gas': 2000000,
                'gasPrice': contract_interactions.w3.eth.gas_price,
                'nonce': nonce,
            })
            print(f'Transaction: {tx}')
            signed_tx = contract_interactions.w3.eth.account.sign_transaction(tx, private_key=contract_interactions.private_key)
            print(f'Signed transaction: {signed_tx}')
            tx_hash = contract_interactions.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f'Transaction hash: {tx_hash.hex()}')
            receipt = contract_interactions.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f'Transaction receipt: {receipt}')
            if receipt.status == 1:
                print(f'Transaction successful: {tx_hash.hex()}')
                nonce += 1  # Incrementa il nonce
                return True
            else:
                flash('Transaction failed', 'error')
                return False
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return False
