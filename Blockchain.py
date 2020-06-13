from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transaction, 
                 timestamp, previous_hash):
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
    def __init__(self, debugging=False):
        """ Construct of blockchain class
        """
        self.chain = []
        self.unconfirmed_transactions = []
        self.create_genesis_block()
        self.debugging = debugging

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

    difficulty = 1

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
            if self.debugging:
                print(f'Block nonce: {block.nonce}')
            block.nonce += 1
            compute_hash = block.compute_hash()

        return compute_hash

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
        
        if not self.is_valid_proof(block, proof):
            return False

        # Add the hash after the PoW
        block.hash = proof
        
        # Add block to the chain
        self.chain.append(block)
        
        return True

    def is_valid_proof(self, block, block_hash):
        """Test if the proof of work is valid.

        Args:
            block: Block of the Blockchain.
            proof: Proof of work.
        """
        return ( block_hash.startswith('0' * Blockchain.difficulty) and
                 block_hash == block.compute_hash()
                )

    def add_new_transaction(self, transaction):
        """ Add a new transaction to the blockchain.

        Args:
            transaction (JSON): New transaction to be added to
                                the blockchain.
        """

        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block

        new_block = Block(index= last_block.index +1,
                          transaction=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash
                          )
        
        if self.debugging:
            print('New block constructed!')
        
        # Do the proof of work of the new block
        proof = self.proof_of_work(new_block)
        
        if self.debugging:
            print('New block constructed!')
        
        # Add the block
        self.add_block(new_block, proof)
        
        # Reset the unconfirmed transactions
        self.unconfirmed_transactions = []

        return new_block.index

    def check_chain_validity(cls, chain):
        
        result = True
        previous_hash = "0"

        # Iterate through every block

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block.hash) or \
                previous_hash != block.previous_hash:
                result = False
                break
            
            block.hash, previous_hash = block_hash, block_hash
        
            return result