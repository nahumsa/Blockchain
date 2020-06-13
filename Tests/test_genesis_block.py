""" To run the unit test python -m unittest Tests/genesis_block_test.py """
###################################
####### Passed on 10/06/20 ########
###################################

import sys
sys.path.append('../')

import unittest
from Blockchain import Blockchain

class TestGenesisBlock(unittest.TestCase):
    def test(self):                
        self.assertEqual(Blockchain().last_block.index,
                         0)



if __name__ == '__main__':
    TestGenesisBlock()