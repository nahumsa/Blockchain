from hashlib import sha256
import json

class Block:
    def __init__(index, transaction, timestamp):
        """Constructor of Block class, the block
        is the foundation of the blockchain.

        Parameters
        ------------------------------------------
        index(int): ID of the block.
        transaction(list): List of transactions.
        timestamp(float): Time of generation of the block.

        """
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
    



    