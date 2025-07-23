import os
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version

# Load environment variables
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")
CHAIN_ID = int(os.getenv("CHAIN_ID"))

# Connect to Infura
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network")

# Install and set Solidity compiler version
install_solc('0.8.0')
set_solc_version('0.8.0')

# Read and compile the Solidity contract
with open('MemeCoin.sol', 'r') as file:
    contract_source_code = file.read()

compiled_sol = compile_source(contract_source_code, output_values=['abi', 'bin'])
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# Build contract instance
MemeCoin = web3.eth.contract(abi=abi, bytecode=bytecode)

def deploy_contract(token_name, token_symbol, initial_supply):
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)
    tx = MemeCoin.constructor(token_name, token_symbol, initial_supply).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': CHAIN_ID,
        'gas': web3.eth.estimate_gas({
            'from': WALLET_ADDRESS,
            'data': MemeCoin.constructor(token_name, token_symbol, initial_supply).data_in_transaction
        }),
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = receipt.contractAddress
    contract_instance = web3.eth.contract(address=contract_address, abi=abi)
    return contract_instance

def check_balance(contract_instance):
    return contract_instance.functions.balanceOf(WALLET_ADDRESS).call()

def transfer_tokens(contract_instance, recipient, amount):
    amount_wei = amount * 10 ** 18
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)
    tx = contract_instance.functions.transfer(recipient, amount_wei).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': CHAIN_ID,
        'gas': web3.eth.estimate_gas({
            'from': WALLET_ADDRESS,
            'to': contract_instance.address,
            'data': contract_instance.functions.transfer(recipient, amount_wei).data_in_transaction
        }),
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return True