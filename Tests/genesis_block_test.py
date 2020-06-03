import sys
sys.path.append('../')

import unittest
from Blockchain import *

class GenesisBlockTest(unittest.TestCase):
    def test(self):
        blockchain = Blockchain()
        #self.assertEqual()



if __name__ == '__main__':
    genesis = GenesisBlockTest()
    print(genesis.last_block())