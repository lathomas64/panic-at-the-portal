import unittest
import sys, os 
sys.path.append(os.path.abspath('..'))
from ursina import *
from prototype.die import Die

class TestDie(unittest.TestCase):

    def test_initialization(self):
        die = Die("d4")
        self.assertEqual(die.size, 4)
        die = Die("d6")
        self.assertEqual(die.size, 6)
        die = Die("d8")
        self.assertEqual(die.size, 8)
        die = Die("d10")
        self.assertEqual(die.size, 10)
        die = Die("d12")
        self.assertEqual(die.size, 12)
        die = Die("3", True)
        self.assertEqual(die.size, 3)
        die = Die("5", True)
        self.assertEqual(die.size, 5)
        die = Die("7", True)
        self.assertEqual(die.size, 7)
        die = Die("9", True)
        self.assertEqual(die.size, 9)
    
    def test_create_pool(self):
        app = Ursina()
        pool = Die.create_pool([])
        self.assertEqual(len(pool), 0)
        for i in range(32):
            dice = ['d6' for x in range(i)]
            pool = Die.create_pool(dice)
            self.assertEqual(len(pool), i)
            if i > 0:
                self.assertEqual(pool[0].size, 6)

    def test_update(self):
        die = Die("d6")
        self.assertEqual(die.visible, True)
        die.update()
        self.assertEqual(die.visible, False)
        die.used = False 
        die.update()
        self.assertEqual(die.visible, True)
        self.assertEqual(die.texture, load_texture("d6"))
        die.clicked()
        die.update()
        self.assertEqual(die.texture, load_texture("d6_hover"))
    
    def test_consume(self):
        app = Ursina()
        die = Die("d6")
        die.roll()
        die.clicked()
        self.assertEqual(die.used, False)
        self.assertNotEqual(die.value, None)
        self.assertEqual(die, Die.selected)
        self.assertNotEqual(die.text.text, "x")

        die.consume()

        self.assertEqual(die.used, True)
        self.assertEqual(die.value, None)
        self.assertEqual(Die.selected, None)
        self.assertEqual(die.text.text, "x")

    def test_roll(self):
        app = Ursina()
        die = Die("d6")
        die.roll()
        self.assertEqual(die.used, False)
        self.assertNotEqual(die.value, None)
        self.assertLessEqual(die.value, die.size)
        self.assertGreaterEqual(die.value, 1)
        self.assertEqual(die.text.text, str(die.value))
        die = Die("7", True)
        die.roll() 
        self.assertEqual(die.value, 7)
        self.assertEqual(die.size, 7)

    def test_clicked(self):
        app = Ursina()
        die = Die("d6")
        self.assertEqual(Die.selected, None)
        die.clicked()
        self.assertEqual(Die.selected, die)