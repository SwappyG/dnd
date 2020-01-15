from Character import Character
import uuid
import unittest
from collections import Counter
from pprint import pprint
import numpy as np

class CharacterTests(unittest.TestCase):

    def setUp(self):
        self.character = Character("Alpha", uuid.uuid4(), 25, "M", "Neutral Neutral", {}, 20, 15)

    def test_UpdateHpAc(self):
        print("Testing get set HP\n")
        self.character.SetHP(14)
        self.assertTrue(14 == self.character.GetHP()) # get set hp
        self.assertTrue(20 == self.character.GetMaxHP()) # get set hp
        self.character.SetHP(7)
        self.assertTrue(7 == self.character.GetHP()) # get set hp
        self.assertTrue(20 == self.character.GetMaxHP()) # get set hp
        self.character.SetHP(-5)
        self.assertTrue(0 == self.character.GetHP()) # get set hp clip bottom
        self.assertTrue(20 == self.character.GetMaxHP()) # get set hp
        self.character.SetHP(22)
        self.assertTrue(20 == self.character.GetHP()) # get set hp clip top
        self.assertTrue(20 == self.character.GetMaxHP()) # get set hp   

        print("Testing get set AC\n")
        self.character.SetAC(43)
        self.assertTrue(43 == self.character.GetAC()) # get set AC
        self.character.SetAC(34324)
        self.assertTrue(34324 == self.character.GetAC()) # get set AC
        self.character.SetAC(-5)
        self.assertTrue(0 == self.character.GetAC()) # get set AC clip below
        
        print("Testing get set Max HP\n")
        self.character.SetHP(14)
        self.character.SetMaxHP(23)
        self.assertTrue(23 == self.character.GetMaxHP()) # get set max hp
        self.assertTrue(14 == self.character.GetHP()) # get set max hp
        self.character.SetHP(22)
        self.assertTrue(22 == self.character.GetHP()) # get set max hp
        self.character.SetHP(24)
        self.assertTrue(23 == self.character.GetHP()) # get set max hp

        self.character.SetMaxHP(5)
        self.assertTrue(5 == self.character.GetMaxHP()) # get set max hp
        self.assertTrue(5 == self.character.GetHP()) # get set max hp

        self.character.SetMaxHP(-4)
        self.assertTrue(0 == self.character.GetMaxHP()) # get set max hp
        self.assertTrue(0 == self.character.GetHP()) # get set max hp

    def test_UpdateInventory(self):
        items = ['alpha', 'beta', 'gamma', 'delta']
        qty = [5, 7, 8, 10]
        
        print("Add some items to character\n")
        self.assertFalse(self.character.AddToInventory("shouldnt_work", -5))
        for ii in range(4):
            self.assertTrue(self.character.AddToInventory(items[ii], qty[ii]))

        print("Add qty to existing item\n")
        for ii in range(4):
            qty_to_add = np.random.randint(5)
            qty[ii] = qty[ii] + qty_to_add
            self.assertTrue(self.character.AddToInventory(items[ii], qty_to_add)) # add
            self.assertTrue(qty[ii] == self.character.GetInventoryQuantity(items[ii])) # retrieve

        self.assertTrue(0 == self.character.GetInventoryQuantity('bogus_item'))

        print("remove qty of existing item\n")
        for ii in range(4):
            qty_to_remove = np.random.randint(3)
            qty[ii] = qty[ii] - qty_to_remove
            self.assertTrue(self.character.RemoveFromInventory(items[ii], qty_to_remove)) # remove
            self.assertTrue(qty[ii] == self.character.GetInventoryQuantity(items[ii])) # retrieve

        self.assertFalse(self.character.RemoveFromInventory('alpha', -5)) # can't remove negative qty
        self.assertTrue(qty[0] == self.character.GetInventoryQuantity(items[0])) # check val hasnt changed

        self.assertTrue(self.character.RemoveFromInventory('bogus', 4)) # remove works for not added items

        print("remove all qty of item\n")
        self.assertTrue(self.character.RemoveFromInventory(items[0])) # no args removes all
        self.assertTrue(0 == self.character.GetInventoryQuantity(items[0]))


    def test_EquipUnequip(self):
        
        print("equip test if not in inventory\n")
        self.assertFalse(self.character.Equip('alpha', 3)) # equip fails if not in inventory
        self.assertFalse(self.character.Equip('alpha', 0)) # equip fails if not in inventory

        print("adding items to inventory\n")
        items = ['alpha', 'beta', 'gamma', 'delta']
        qty = [5, 7, 8, 10]
        for ii in range(4):
            self.assertTrue(self.character.AddToInventory(items[ii], qty[ii]))

        print("equip fail if neg qty\n")
        self.assertFalse(self.character.Equip('alpha', -1)) # equip fails if qty is negative

        print("equiping some items  \n")
        equip_qty = [0,0,0,0]
        for ii in range(4):
            equip_qty[ii] = np.random.randint(1,4)
            qty[ii] -= equip_qty[ii]
            self.assertTrue(self.character.Equip(items[ii], equip_qty[ii]))
            print("inventory <{}> : <{}>".format(qty[ii], self.character.GetInventoryQuantity(items[ii])))
            print("equiped <{}> : <{}>".format(equip_qty[ii], self.character.GetEquipedQuantity(items[ii])))
            self.assertTrue(qty[ii] == self.character.GetInventoryQuantity(items[ii]))
            self.assertTrue(equip_qty[ii] == self.character.GetEquipedQuantity(items[ii]))

        

    def test_IncrementLevel(self):
        pass

if __name__=="__main__":
    unittest.main()