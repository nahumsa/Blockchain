from Blockchain import Blockchain, Block
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
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    
    if not result:
        return "No transaction to mine."
    
    else:
        # Make sure that we have the longest chain
        chain_lenght = len(blockchain.chain)
        consensus()

        if chain_lenght == len(blockchain.chain):
            announce_new_block(blockchain.last_block)
        return f"Block #{result} is mined."

@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

# Adding descentralization
# Keeping host addresses for other members
peers = set()

# Adding new peers to the network
@app.route('/register_node', metods=["POST"])
def register_new_peers():
    # The host address to the pper node
    node_address = request.get_json()["node_address"]

    if not node_address:
        return "Invalid data.", 400

    # Add the node to the peer list
    peers.add(node_address)

    # Return the blockchain of the newly register node 
    # for synchronization
    return get_chain()

@app.route('register_with', methods=['POST'])
def register_with_existing_node():

    node_address = request.get_json()["node_adress"]

    if not node_address:
        return "Invalid data.", 400
    
    data = {"node_adress": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node 
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        global blockchain
        global peers
        
        # Update chain and peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    
    else:
        return response.content, response.status_code

def create_chain_from_dump(chain_dump):
    """ 
    Internally calls the `register_node` endpoint to
    register current node with the remote node specified 
    in the request, and sync the blockchain as well with 
    the remote node.

    Args:
        chain_dump (JSON): chain dump.

    Raises:
        Exception: If the chain was tempered.

    Returns:
        Object: retrns Blockchain
    """

    blockchain = Blockchain()
    
    for index, block_data in enumerate(chain_dump):
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"])
        proof = block_data["hash"]

        # Exclude the genesis block
        if index > 0:
            added = blockchain.add_block(block, proof)

            if not added:
                raise Exception("The chain dump is tampered!!")
        
        # For the genesis block
        else:
            blockchain.chain.append(block)
    
    return blockchain

def consensus():
    """
    Simple consensus algorithm.
    If a longer valid chain is found, our chain is replaced
    with it.
    """

    global Blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = request.get(f'{node}/chain')
        lenght = request.json()['lenght']
        chain = response.json()['chain']

        if length > current_len and \
        blockchain.check_chain_validity(chain):

            current_len = lenght
            longest_chain = chain
    
    if longest_chain:
        blockchain = longest_chain
        return True
    
    return False

# Endpoint to add a block that was mined by
# someone else to the node's chain. 
# First we verify then add to the chain.

@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"])
    
    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarted by the node", 400
    
    return "Block added to the chain", 201

def announce_new_block(block):
    """Helper function to announce to the network that a 
    block has been mined. Other blocks can simply verigy the POW
    and add it to their respective chains.

    """

    for peer in peers:
        url = f'{peer}add_block'
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True)))
        
# The announce_new_block shoud be called after every block
# is mined.

app.run(debug=True, port=8000)