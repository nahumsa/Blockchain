import sys
sys.path.append('../')

import unittest
from Blockchain import Blockchain

class GenesisBlockTest(unittest.TestCase):
    def test(self):        
        self.assertEqual(Blockchain().last_block.index,
                         '0')



if __name__ == '__main__':
    GenesisBlockTest()