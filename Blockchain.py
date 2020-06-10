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
        """Creates the first block of the blockchain
        and appends to the chain.
        """
        
        genesis_block = Block(index=0, transaction=[], 
                              timestamp=time.time(), previous_hash="0")

        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        
    @property
    def last_block(self):        
        """ Returns the last block

        Returns:
            int: Return the chain.
        """
        return self.chain[-1]

    difficulty = 2

    def proof_of_work(self, block):
        """Run the hash until it satisfies the constraints
        that we imposed, that is 0 times the difficulty of 
        our proof of work. This exploits the asymetry of 
        computing the hash function.

        Args:
            block: Blockchain block.
        """
        block.nonce = 0

        compute_hash = block.compute_hash()

        while not compute_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
    
    def add_block(self, block, proof):
        """Adds block to the chain after verifying 
        if satisfies our proof of work and if the 
        previous_hash of the block is equivalent to 
        the hash of the previous block.

        Args:
            block ([type]): [description]
            proof ([type]): [description]
        """
        
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False
        
        if not Blockchain.is_valid_proof(block, proof):
            return False

        # Add the hash after the PoW
        block.hash = proof
        
        # Add block to the chain
        self.chain.append(block)
        
        return True

    def is_valid_proof(self, block, proof):
        """[summary]

        Args:
            block: Block of the Blockchain.
            proof: Proof of work.
        """
        return ( block_hash.starstwith('0' * Blockchain.difficulty) and
                 block_hash == block.comput_hash()
                )

    def add_new_transaction(self, transaction):
        """ Add a new transaction to the blockchain.

        Args:
            transaction (JSON): New transaction to be added to
                                the blockchain.
        """

        self.unconfirmed_transaction.append(transaction)