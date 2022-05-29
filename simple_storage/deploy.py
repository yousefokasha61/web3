import json
import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
from solcx import compile_standard, install_solc

load_dotenv()

with open("../solidity/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/e26ff630d86249528055bbb8e0dccbb8")
)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
chain_id = 4
my_address = "0x96B71a4e5Bc86b0A171528765F0C20B0eFbc1348"
private_key = os.getenv("PRIVATE_KEY")


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key)
send_store_transaction_hash = w3.eth.send_raw_transaction(
    signed_store_txn.rawTransaction
)
send_store_transaction_receipt = w3.eth.wait_for_transaction_receipt(
    send_store_transaction_hash
)
print(simple_storage.functions.retrieve().call())
