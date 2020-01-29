from Character import Character
from Job import Job
from Feature import Feature
from Option import Option
from Library import Library
import uuid
import unittest
import numpy as np
from pprint import pprint


class CharacterTests(unittest.TestCase):

    def setUp(self):
        self.character = Character("Alpha", uuid.uuid4(), 25, "M", "Neutral Neutral", {}, 20, 15)

    def test_UpdateHpAc(self):
        print("Testing get set HP\n")
        self.character.SetHP(14)
        self.assertTrue(14 == self.character.GetHP())  # get set hp
        self.assertTrue(20 == self.character.GetMaxHP())  # get set hp
        self.character.SetHP(7)
        self.assertTrue(7 == self.character.GetHP())  # get set hp
        self.assertTrue(20 == self.character.GetMaxHP())  # get set hp
        self.character.SetHP(-5)
        self.assertTrue(0 == self.character.GetHP())  # get set hp clip bottom
        self.assertTrue(20 == self.character.GetMaxHP())  # get set hp
        self.character.SetHP(22)
        self.assertTrue(20 == self.character.GetHP())  # get set hp clip top
        self.assertTrue(20 == self.character.GetMaxHP())  # get set hp

        print("Testing get set AC\n")
        self.character.SetAC(43)
        self.assertTrue(43 == self.character.GetAC())  # get set AC
        self.character.SetAC(34324)
        self.assertTrue(34324 == self.character.GetAC())  # get set AC
        self.character.SetAC(-5)
        self.assertTrue(0 == self.character.GetAC())  # get set AC clip below

        print("Testing get set Max HP\n")
        self.character.SetHP(14)
        self.character.SetMaxHP(23)
        self.assertTrue(23 == self.character.GetMaxHP())  # get set max hp
        self.assertTrue(14 == self.character.GetHP())  # get set max hp
        self.character.SetHP(22)
        self.assertTrue(22 == self.character.GetHP())  # get set max hp
        self.character.SetHP(24)
        self.assertTrue(23 == self.character.GetHP())  # get set max hp

        self.character.SetMaxHP(5)
        self.assertTrue(5 == self.character.GetMaxHP())  # get set max hp
        self.assertTrue(5 == self.character.GetHP())  # get set max hp

        self.character.SetMaxHP(-4)
        self.assertTrue(0 == self.character.GetMaxHP())  # get set max hp
        self.assertTrue(0 == self.character.GetHP())  # get set max hp

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
            self.assertTrue(self.character.AddToInventory(items[ii], qty_to_add))  # add
            self.assertTrue(qty[ii] == self.character.GetInventoryQuantity(items[ii]))  # retrieve

        self.assertTrue(0 == self.character.GetInventoryQuantity('bogus_item'))

        print("remove qty of existing item\n")
        for ii in range(4):
            qty_to_remove = np.random.randint(3)
            qty[ii] = qty[ii] - qty_to_remove
            self.assertTrue(self.character.RemoveFromInventory(items[ii], qty_to_remove))  # remove
            self.assertTrue(qty[ii] == self.character.GetInventoryQuantity(items[ii]))  # retrieve

        self.assertFalse(self.character.RemoveFromInventory('alpha', -5))  # can't remove negative qty
        self.assertTrue(qty[0] == self.character.GetInventoryQuantity(items[0]))  # check val hasnt changed

        self.assertTrue(self.character.RemoveFromInventory('bogus', 4))  # remove works for not added items

        print("remove all qty of item\n")
        self.assertTrue(self.character.RemoveFromInventory(items[0]))  # no args removes all
        self.assertTrue(0 == self.character.GetInventoryQuantity(items[0]))

    def test_EquipUnequip(self):

        print("equip test if not in inventory\n")
        self.assertFalse(self.character.Equip('alpha', 3))  # equip fails if not in inventory
        self.assertFalse(self.character.Equip('alpha', 0))  # equip fails if not in inventory

        print("adding items to inventory\n")
        items = ['alpha', 'beta', 'gamma', 'delta']
        qty = [5, 7, 8, 10]
        for ii in range(4):
            self.assertTrue(self.character.AddToInventory(items[ii], qty[ii]))

        print("equip fail if neg qty\n")
        self.assertFalse(self.character.Equip('alpha', -1))  # equip fails if qty is negative

        print("equiping some items  \n")
        equip_qty = [0, 0, 0, 0]
        for ii in range(4):
            equip_qty[ii] = np.random.randint(1, 4)
            qty[ii] -= equip_qty[ii]
            self.assertTrue(self.character.Equip(items[ii], equip_qty[ii]))
            print("inventory <{}> : <{}>".format(qty[ii], self.character.GetInventoryQuantity(items[ii])))
            print("equiped <{}> : <{}>".format(equip_qty[ii], self.character.GetEquippedQuantity(items[ii])))
            self.assertTrue(qty[ii] == self.character.GetInventoryQuantity(items[ii]))
            self.assertTrue(equip_qty[ii] == self.character.GetEquippedQuantity(items[ii]))

    def test_IncrementLevel(self):

        print("Testing Increment Level\n\n")
        print("Setting up the library\n\n")

        # Make a test features dict (0 - 4 are normal feautres, 5 - 11 are for options)
        feat_uuids = [uuid.uuid4() for _ in range(12)]
        feat_dict = {
            feat_uuids[0]: Feature("feat_apple", feat_uuids[0], "red apples"),
            feat_uuids[1]: Feature("feat_banana", feat_uuids[1], "yellow bananas", unlock_level=3),
            feat_uuids[2]: Feature("feat_carrot", feat_uuids[2], "n/a", prereq_features=[feat_uuids[0], feat_uuids[1]]),
            feat_uuids[3]: Feature("feat_durian", feat_uuids[3], "stinky durians",
                                   prereq_features=[feat_uuids[1]], unlock_level=5),
            feat_uuids[4]: Feature("feat_elderberry", feat_uuids[4], "exotic berries", unlock_level=3),
            feat_uuids[5]: Feature("feat_fig", feat_uuids[5], "go figure"),
            feat_uuids[6]: Feature("feat_guava", feat_uuids[6], "best fruit"),
            feat_uuids[7]: Feature("feat_kiwi", feat_uuids[7], "tingly"),
            feat_uuids[8]: Feature("feat_lime", feat_uuids[8], "zest"),
            feat_uuids[9]: Feature("feat_mango", feat_uuids[9], "big ass red ants"),
            feat_uuids[10]: Feature("feat_olive", feat_uuids[10], "maybe if i piss on it"),
            feat_uuids[11]: Feature("feat_papaya", feat_uuids[11], "meh"),
        }

        # Make a test options dict
        opt_uuids = [uuid.uuid4() for _ in range(2)]
        opt_dict = {
            opt_uuids[0]: Option("opt_artichoke", opt_uuids[0], "best dip", feat_uuids[5:8], [1, 2, 3]),
            opt_uuids[1]: Option("opt_beans", opt_uuids[1], "all carbs", feat_uuids[8:], [4, 4, 5, 6],
                                 prereq_features=[feat_uuids[3]]),
        }

        # Make a jobs dict
        job_uuid = uuid.uuid4()
        job_dict = {
            job_uuid: Job("simple_job", job_uuid, "simple_job_description", feat_uuids[:5], opt_uuids)
        }

        # Create our library
        library = Library()
        library.SetValidDicts(['features', 'options', 'jobs'])
        library.AddToDict('features', feat_dict)
        library.AddToDict('options', opt_dict)
        library.AddToDict('jobs', job_dict)

        # Create our character
        print("Creating a character\n\n")
        test_stats = {'STR': 10, 'DEX': 10, 'CON': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
        character = Character("beta", job_uuid, 20, "M", "Neutral Neutral", test_stats, 13, 17)

        print("Getting the Options when advancing from Level 0 to Level 1\n\n")
        self.assertTrue(character.GetLevel() == 0)  # make sure we start at level 0
        unlock_options = character.GetNextLevelOptions(library)  # get our options for level 1
        self.assertTrue(len(unlock_options) == 1)  # make sure we only got one opt unlocked
        self.assertTrue(opt_uuids[0] in unlock_options)  # opt 0 has an unlock at level 1
        self.assertTrue(unlock_options[opt_uuids[0]]['num_options'] == 1)  # opt 0 has 1 unlock at level 1
        # The available options should be indices (5,6,7)
        self.assertTrue( set(unlock_options[opt_uuids[0]]['feature_uuids']) == set(feat_uuids[5:8]) )
        self.assertFalse( 1 in Character.stat_buff_levels )  # level 1 has no stats buffs

        print("Making sure increment level rejects bad selections\n\n")
        self.assertFalse(character.IncrementLevel(library, {}))
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[8]]}))  # feat not in opt
        # Only 1 feature was unlocked for this option, so sending two should fail
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[5], feat_uuids[6]]}))
        # level 1 has no stats buffs, so specifying one should be rejected
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[5]]}, ['STR']))

        print("Making sure increment level accepts valid selection\n\n")
        selected_options = {
            opt_uuids[0]: [feat_uuids[6]]
        }
        self.assertTrue(character.IncrementLevel(library, selected_options))

        print("Checking if we're at level 1, and we've learned the specified feature\n\n")
        self.assertTrue(character.GetLevel() == 1)
        self.assertTrue( sorted(character.GetLearnedFeatures()) == sorted([feat_uuids[0], feat_uuids[6]]))

        print("Getting options for level 2\n\n")
        unlock_options = character.GetNextLevelOptions(library)  # get our options for level 2
        pprint(unlock_options)
        self.assertTrue(len(unlock_options) == 1)  # make sure we only got one opt unlocked
        self.assertTrue(opt_uuids[0] in unlock_options)  # opt 0 has an unlock at level 2
        self.assertTrue(unlock_options[opt_uuids[0]]['num_options'] == 1)  # opt 0 has 1 unlock at level 2
        # The available indices should be only 5 and 7 since we already picked 6
        self.assertTrue(set(unlock_options[opt_uuids[0]]['feature_uuids']) == set([feat_uuids[ii] for ii in (5, 7)]))
        self.assertFalse(2 in Character.stat_buff_levels)  # level 2 has no stats buffs

        print("Incrementing to Level 2 after trying some invalid args\n\n")
        self.assertFalse(character.IncrementLevel(library, {}))  # empty shouldn't work
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[6]]}))  # we already know 6
        # level 2 has no stats buffs, so specifying one should be rejected
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[7]]}, ['STR']))
        selected_options = {
            opt_uuids[0]: [feat_uuids[7]]
        }
        self.assertTrue(character.IncrementLevel(library, selected_options))  # 7 is a valid opt, this should work

        print("Checking if we're at level 2, and we've learned the specified feature\n\n")
        self.assertTrue(character.GetLevel() == 2)
        self.assertTrue(sorted(character.GetLearnedFeatures()) == sorted([feat_uuids[0], feat_uuids[6], feat_uuids[7]]))

        print("Getting options for level 3\n\n")
        unlock_options = character.GetNextLevelOptions(library)  # get our options for level 3
        pprint(unlock_options)
        self.assertTrue(len(unlock_options) == 1)  # make sure we only got one opt unlocked
        self.assertTrue(opt_uuids[0] in unlock_options)  # opt 0 has an unlock at level 3
        self.assertTrue(unlock_options[opt_uuids[0]]['num_options'] == 1)  # opt 0 has 1 unlock at level 3
        # The available indices should be only 5 since we already picked 6 and 7
        self.assertTrue(set(unlock_options[opt_uuids[0]]['feature_uuids']) == set([feat_uuids[ii] for ii in (5,)]))
        self.assertFalse(3 in Character.stat_buff_levels)  # level 3 has no stats buffs

        print("Incrementing to Level 3 after trying some invalid args\n\n")
        self.assertFalse(character.IncrementLevel(library, {}))  # empty shouldn't work
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[6]]}))  # we already know 6
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[7]]}))  # we already know 7
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[1]: [feat_uuids[5]]}))  # opt 1 is not unlocked
        # level 2 has no stats buffs, so specifying one should be rejected
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[5]]}, ['STR']))
        selected_options = {
            opt_uuids[0]: [feat_uuids[5]]
        }
        self.assertTrue(character.IncrementLevel(library, selected_options))  # 5 is a valid opt, this should work

        print("Checking if we're at level 3, and we've learned the specified feature\n\n")
        self.assertTrue(character.GetLevel() == 3)
        expected_learned_features = [
            feat_uuids[0], feat_uuids[7], feat_uuids[5], feat_uuids[6], feat_uuids[1], feat_uuids[2], feat_uuids[4]
        ]
        self.assertTrue(sorted(character.GetLearnedFeatures()) == sorted(expected_learned_features))

        print("Getting options for level 4\n\n")
        unlock_options = character.GetNextLevelOptions(library)  # get our options for level 3
        self.assertTrue(unlock_options == {})  # Because we haven't unlocked feat 3, there are no options unlocked
        self.assertTrue(4 in Character.stat_buff_levels)  # level 4 has stat buffs

        print("Incrementing to Level 3 after trying some invalid args\n\n")
        self.assertFalse(character.IncrementLevel(library, {}))  # we have to provide stat buffs
        self.assertFalse(character.IncrementLevel(library, {}, []))  # empty list is invalid
        self.assertFalse(character.IncrementLevel(library, {}), ['STR', 'DEX', 'CHA'])  # list can only be 1 or 2 long
        self.assertFalse(character.IncrementLevel(library, {}), ['not_a_stat'])  # keys must be valid
        # We have no options, so empty dict should work
        self.assertTrue(character.IncrementLevel(library, {}, ['STR', 'DEX']))

        print("Checking if we're at level 4, and we've learned the specified feature\n\n")
        self.assertTrue(character.GetLevel() == 4)
        expected_learned_features = [
            feat_uuids[0], feat_uuids[7], feat_uuids[5], feat_uuids[6], feat_uuids[1], feat_uuids[2], feat_uuids[4]
        ]
        self.assertTrue(sorted(character.GetLearnedFeatures()) == sorted(expected_learned_features))
        self.assertTrue(character.GetStats()['STR'] == 11)
        self.assertTrue(character.GetStats()['DEX'] == 11)
        self.assertTrue(character.GetStats()['CON'] == 10)
        self.assertTrue(character.GetStats()['INT'] == 10)
        self.assertTrue(character.GetStats()['WIS'] == 10)
        self.assertTrue(character.GetStats()['CHA'] == 10)

        print("Getting options for level 5\n\n")
        unlock_options = character.GetNextLevelOptions(library)  # get our options for level 5
        self.assertTrue(len(unlock_options) == 1)  # We've now unlocked feat 3, there are opt 1 should be avail
        self.assertTrue(opt_uuids[1] in unlock_options)  # opt 1 has an unlocks now
        # opt 1 has 1 unlock at level 5, and 2 unlocks at level 4 which we didn't unlock before because of prereq
        self.assertTrue(unlock_options[opt_uuids[1]]['num_options'] == 3)
        # The available indices should be (8,9,10,11)
        self.assertTrue(set(unlock_options[opt_uuids[1]]['feature_uuids']) == set(feat_uuids[8:]))
        self.assertFalse(5 in Character.stat_buff_levels)  # level 5 has no stats buffs

        print("Incrementing to Level 5 after trying some invalid args\n\n")
        self.assertFalse(character.IncrementLevel(library, {}))  # empty shouldn't work
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[1]: [feat_uuids[8]]}))  # list needs to be len 3
        self.assertFalse(character.IncrementLevel(library, {
            opt_uuids[0]: [feat_uuids[8], feat_uuids[9], feat_uuids[10]]
        }))  # Wrong opt, should be opt 1 not 0
        self.assertFalse(character.IncrementLevel(
            library, {opt_uuids[1]: [feat_uuids[8], feat_uuids[9], feat_uuids[10]]}, ['STR']
        ))  # no stat unlocks this time
        selected_options = {
            opt_uuids[1]: [feat_uuids[8], feat_uuids[9], feat_uuids[11]]
        }
        self.assertTrue(character.IncrementLevel(library, selected_options))  # this should work

        print("Checking if we're at level 5, and we've learned the specified feature\n\n")
        self.assertTrue(character.GetLevel() == 5)
        expected_learned_features = [
            feat_uuids[0], feat_uuids[7], feat_uuids[5], feat_uuids[6], feat_uuids[1], feat_uuids[2], feat_uuids[4],
            feat_uuids[8], feat_uuids[9], feat_uuids[11], feat_uuids[3]
        ]
        self.assertTrue(sorted(character.GetLearnedFeatures()) == sorted(expected_learned_features))
        self.assertTrue(character.GetStats()['STR'] == 11)
        self.assertTrue(character.GetStats()['DEX'] == 11)
        self.assertTrue(character.GetStats()['CON'] == 10)
        self.assertTrue(character.GetStats()['INT'] == 10)
        self.assertTrue(character.GetStats()['WIS'] == 10)
        self.assertTrue(character.GetStats()['CHA'] == 10)

        print("Getting options for level 6\n\n")
        unlock_options = character.GetNextLevelOptions(library)  # get our options for level 6
        self.assertTrue(len(unlock_options) == 1)  # only one opt to unlock at level 6
        self.assertTrue(opt_uuids[1] in unlock_options)  # opt 1 has an unlocks now
        # opt 1 has 1 unlock at level 6
        self.assertTrue(unlock_options[opt_uuids[1]]['num_options'] == 1)
        # Only index 10 is left
        self.assertTrue(unlock_options[opt_uuids[1]]['feature_uuids'] == [feat_uuids[10]])
        self.assertFalse(6 in Character.stat_buff_levels)  # level 6 has no stats buffs

        print("Incrementing to Level 6 after trying some invalid args\n\n")
        self.assertFalse(character.IncrementLevel(library, {}))  # empty shouldn't work
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[1]: [feat_uuids[8]]}))  # we already know 8
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[0]: [feat_uuids[10]]}))  # Wrong opt index
        # no stat unlocks this time
        self.assertFalse(character.IncrementLevel(library, {opt_uuids[1]: [feat_uuids[10]]}, ['STR']))
        selected_options = {
            opt_uuids[1]: [feat_uuids[10]]
        }
        self.assertTrue(character.IncrementLevel(library, selected_options))  # this should work

        print("Checking if we're at level 6, and we've learned the specified feature\n\n")
        self.assertTrue(character.GetLevel() == 6)
        expected_learned_features = [
            feat_uuids[0], feat_uuids[7], feat_uuids[5], feat_uuids[6], feat_uuids[1], feat_uuids[2], feat_uuids[4],
            feat_uuids[8], feat_uuids[9], feat_uuids[11], feat_uuids[3], feat_uuids[10]
        ]
        self.assertTrue(sorted(character.GetLearnedFeatures()) == sorted(expected_learned_features))
        self.assertTrue(character.GetStats()['STR'] == 11)
        self.assertTrue(character.GetStats()['DEX'] == 11)
        self.assertTrue(character.GetStats()['CON'] == 10)
        self.assertTrue(character.GetStats()['INT'] == 10)
        self.assertTrue(character.GetStats()['WIS'] == 10)
        self.assertTrue(character.GetStats()['CHA'] == 10)

        print("Increment Level test complete")


if __name__ == "__main__":
    unittest.main()
