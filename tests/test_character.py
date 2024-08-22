import unittest
import sys, os 
sys.path.append(os.path.abspath('..'))
from ursina import *
from prototype.character import Character
from prototype.actions.actor import Actor

class TestCharacter(unittest.TestCase):
    
    def test_interface(self):
        self.assertTrue(issubclass(Character, Actor))