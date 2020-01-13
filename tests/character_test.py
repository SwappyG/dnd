from Character import Character
import uuid
import unittest
from collections import Counter
from pprint import pprint

class CharacterTests(unittest.TestCase):

    def setUp(self):
        self.character = Character("Alpha", uuid.uuid4(), 25, "M", "Neutral Neutral", {}, 20, 15)

    def test_UpdateHpAc(self):
        pass

    def test_UpdateInventory(self):
        pass

    def test_EquipUnequip(self):
        pass

    def test_IncrementLevel(self):
        pass

if __name__=="__main__":
    unittest.main()