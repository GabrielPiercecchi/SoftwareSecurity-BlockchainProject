import json
import os
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

class ContractInteractions:

    def __init__(self):
        load_dotenv()
        self.node_address = os.getenv("BLOCKCHAIN_URL")
        self.w3 = Web3(Web3.HTTPProvider(self.node_address))
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)  # Aggiungi il middleware POA
        self.chain_id = 1337
        self.my_address = Web3.to_checksum_address(os.getenv("ADMIN_ADDRESS"))        
        self.private_key = os.getenv("ADMIN_PRIVATE_KEY")
        self.CoinContract = None

        # Verifica che l'indirizzo sia valido
        if not self.w3.is_address(self.my_address):
            print(f"Invalid Ethereum address: {self.my_address}")
            raise ValueError(f"Invalid Ethereum address: {self.my_address}")

        # Compila il contratto se non è già stato compilato
        if not os.path.exists("./contract/compiled_code.json"):
            self.compile_contract()

        # Carica il contratto compilato
        self.load_contract()

    def compile_contract(self):
        try:
            with open("./contract/CoinContract.sol", "r", encoding="utf-8") as file:
                coin_contract_file = file.read()

            install_solc("0.8.0")

            compiled_sol = compile_standard(
                {
                    "language": "Solidity",
                    "sources": {"CoinContract.sol": {"content": coin_contract_file}},
                    "settings": {
                        "outputSelection": {
                            "*": {
                                "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                            }
                        }
                    },
                },
                solc_version="0.8.0",
            )

            with open("./contract/compiled_code.json", "w", encoding="utf-8") as file:
                json.dump(compiled_sol, file)
            print("Contract compiled successfully.")
        except Exception as e:
            print(f"Error compiling contract: {e}")
            raise

    def load_contract(self):
        try:
            with open("./contract/compiled_code.json", "r", encoding="utf-8") as file:
                compiled_sol = json.load(file)
            abi = json.loads(compiled_sol["contracts"]["CoinContract.sol"]["CoinContract"]["metadata"])["output"]["abi"]
            bytecode = compiled_sol["contracts"]["CoinContract.sol"]["CoinContract"]["evm"]["bytecode"]["object"]
            self.CoinContract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
            print("Contract loaded successfully.")
        except Exception as e:
            print(f"Error loading contract: {e}")
            raise

    def deploy_contract(self):
        try:
            # Verifica se il contratto è già stato distribuito
            if os.path.exists("./contract/contract_address.txt"):
                with open("./contract/contract_address.txt", "r", encoding="utf-8") as file:
                    contract_address = file.read().strip()
                print(f"Contract already deployed at address: {contract_address}")
                return contract_address

            nonce = self.w3.eth.get_transaction_count(self.my_address, 'pending')
            transaction = self.CoinContract.constructor().build_transaction(
                {
                    "chainId": self.chain_id,
                    "gasPrice": self.w3.eth.gas_price,
                    "from": self.my_address,
                    "nonce": nonce,
                }
            )

            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            contract_address = tx_receipt.contractAddress
            with open("./contract/contract_address.txt", "w", encoding="utf-8") as file:
                file.write(contract_address)
            print(f"Contract deployed at address: {contract_address}")
            return contract_address
        except Exception as e:
            print(f"Error deploying contract: {e}")
            raise

    def get_contract(self, contract_address):
        try:
            with open("./contract/compiled_code.json", "r", encoding="utf-8") as file:
                compiled_sol = json.load(file)
            abi = json.loads(compiled_sol["contracts"]["CoinContract.sol"]["CoinContract"]["metadata"])["output"]["abi"]
            return self.w3.eth.contract(address=contract_address, abi=abi)
        except Exception as e:
            print(f"Error getting contract: {e}")
            raise