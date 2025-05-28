from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

ALCHEMY_URL = os.getenv("ALCHEMY_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
assert w3.is_connected(), "Web3 not connected!"

with open("artifacts/contracts/PatientRecordContract.sol/PatientRecordContract.json") as f:
    contract_json = json.load(f)
    abi = contract_json['abi']

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def send_txn(function_call):
    nonce = w3.eth.get_transaction_count(PUBLIC_KEY, 'pending')
    txn = function_call.build_transaction({
        'from': PUBLIC_KEY,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.to_wei('10', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Tx sent! Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Tx confirmed:", receipt.transactionHash.hex())

send_txn(contract.functions.addRecord("patient_001"))

recipient = "DIFFERENT_WALLET_ADDRESS_HERE"
send_txn(contract.functions.transferRecord(0, recipient))








