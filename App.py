from Blockchain import Blockchain
from flask import Flask, request
import requests
import json
import time

# Initializing flask application
app = Flask(__name__)

# Initializing Blockchain object
blockchain = Blockchain()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx.data.get(field):
            return "Invalid transaction data.", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success!", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    
    return json.dumps({"length": len(chain_data),
                        "chain": chain_data})

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transaction():
    result = blockchain.mine()
    
    if not result:
        return "No transaction to mine."
    
    return f"Block #{result} is mined."

@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)