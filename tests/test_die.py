import unittest
import sys, os 
sys.path.append(os.path.abspath('..'))
from prototype.die import Die

class TestDie(unittest.TestCase):

    def test_update(self):
        self.assertTrue(False, "no test written yet")

if __name__ == '__main__':
    unittest.main()