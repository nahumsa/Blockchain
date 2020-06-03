from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transaction, timestamp, previous_hash):
        """Constructor of Block class, the block
        is the foundation of the blockchain.

        Parameters
        ------------------------------------------
        index(int): ID of the block.
        transaction(list): List of transactions.
        timestamp(float): Time of generation of the block.
        previous_hash(string): Previous hash of the block.

        """

        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.previous_hash = previous_hash
    
    def compute_hash(self):
        """ Returns the hash from a JSON
        
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        """ Construct of blockchain class
        
        """
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """ Creates the first block of the blockchain
        and appends to the chain.
        
        """
        genesis_block = Block(index=0, transaction=[], 
                              timestamp=time.time(), previous_hash="0")

        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        
    @property
    def last_block(self):
        """ Returns the last block

        """
        return self.chain[-1]


if __name__ == "__main__":
    A = Blockchain()
    print(A.last_block.index)