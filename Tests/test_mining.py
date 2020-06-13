###################################
####### Passed on 13/06/20 ########
###################################

import sys
sys.path.append('../')

import unittest
from Blockchain import Blockchain

class TestMine(unittest.TestCase):
    def test(self):
        blockchain = Blockchain(debugging=True)    
        blockchain.add_new_transaction([]) 
        blockchain.mine()           
        self.assertEqual(blockchain.last_block.index,
                         1)



if __name__ == '__main__':
    TestMine()