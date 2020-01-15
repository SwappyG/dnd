from Library import Library
import uuid
import unittest
from Effect import Effect
from collections import Counter
from pprint import pprint
import numpy as np

class LibraryTests(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.valid_dicts = ['features', 'effects', 'options', 'jobs']

    def test_ValidDicts(self):
        # Check that Set and Get ValidDict work
        print("setting valid dicts\n")
        self.library.SetValidDicts(self.valid_dicts)
        self.assertTrue(Counter(self.valid_dicts) == Counter(self.library.GetValidDicts()))
        self.assertFalse(self.library.AddToDict('not_valid_dict', {uuid.uuid4():[], uuid.uuid4():[]}))

        # Add a new dict, check that old list doesn't match new list
        print("adding new valid dict\n")
        self.library.AddNewValidDict("fancy")
        self.assertFalse(Counter(self.valid_dicts) == Counter(self.library.GetValidDicts()))
        self.assertTrue(Counter(self.valid_dicts + ['fancy']) == Counter(self.library.GetValidDicts()))

        # Make sure adding to valid dict works
        print("adding items to dict\n")
        self.assertTrue(self.library.AddToDict('fancy', {uuid.uuid4():[], uuid.uuid4():[]}))
        self.assertTrue(self.library.AddToDict('features', {uuid.uuid4():[]}))
        self.assertTrue(self.library.AddToDict('effects', {uuid.uuid4():[], uuid.uuid4():[], uuid.uuid4():[]}))
        self.assertTrue(self.library.AddToDict('effects', {}))
        
        print("ValidDicts test end\n")

    def test_Add_Get_IsInDict(self):
        self.library.SetValidDicts(self.valid_dicts)

        entries = {}
        uuids = [uuid.uuid4() for _ in range(10)]
        val = 0
        for id in uuids:
            entries[id] = val
            val += 1
 
        # Make sure adding entries works
        print("Adding entries to dicts\n")
        self.assertTrue(self.library.AddToDict('features', entries)) # should succed first time
        self.assertTrue(self.library.AddToDict('features', {})) # empty entries dict should be fine
        self.assertFalse(self.library.AddToDict('features', entries, mode='safe')) # should fail in safe mode
        self.assertTrue(self.library.AddToDict('features', entries, mode='overwrite')) # should succeed in overwrite mode
        self.assertTrue(self.library.AddToDict('features', entries, mode='normal')) # should succeed in normal mode
        self.assertFalse(self.library.AddToDict('features', entries, mode='not_a_mode')) # should fail in invalid mode
        self.assertFalse(self.library.AddToDict('not_valid', entries)) # invalid dict should be rejected
        self.assertFalse(self.library.AddToDict('features', [3,4,56,6])) # entries should be a dict
        self.assertFalse(self.library.AddToDict('features', 3)) # entries should be a dict
        self.assertFalse(self.library.AddToDict('features', (3,6))) # entries should be a dict

        # Make sure all added id's return true for IsInDict
        print("Validating that entries are in dict\n")
        for id in uuids:
            self.assertTrue(self.library.IsInDict('features', id))

        # Make sure random id's return false
        print("Making sure random entries don't return true for IsInDict()\n")
        for _ in range(10):
            self.assertFalse(self.library.IsInDict('features', uuid.uuid4()))

        # Make sure Library.Get(...) works
        print("Testing Library.Get()\n")
        for id in uuids:
            print("<{}> , <{}>".format(entries[id], self.library.Get('features', id)))
            self.assertTrue(entries[id] is self.library.Get('features', id))
        print("\n")

        # Create entries with uuid:tuple
        entries = {}
        uuids = [uuid.uuid4() for _ in range(10)]
        vals = [ (np.random.randint(10), np.random.randint(10)) for _ in range(10)] #random tuples list
        for ii in range(10):
            entries[uuids[ii]] = vals[ii]

        # Make sure we can add them to the dict
        print("Adding tuple objects to a dict\n")
        self.assertTrue(self.library.AddToDict('options', entries)) # uuid:tuple entries should add successfully

        # Retrieve all the tuples and make sure they match
        print("Making sure added tuples can be retrieved\n")
        for id in uuids:
            print("<{}> , <{}>".format(entries[id], self.library.Get('options', id)))
            self.assertTrue(entries[id] is self.library.Get('options', id))
        print("\n")

        print("Library Add_Get_IsInDict test end\n")

    def test_GetNameUUID(self):
        self.library.SetValidDicts(self.valid_dicts)

        # add some effects to the library
        print("Adding some Effect instances to the library\n")
        uuids = [uuid.uuid4() for _ in range(4)]
        names = ['alpha', 'beta', 'gamma', 'delta']
        effects = [
            Effect(names[0], uuids[0], "attack", "instant", "alpha effect"),
            Effect(names[1], uuids[1], "attack", "delayed", "beta effect"),
            Effect(names[2], uuids[2], "attack", "persistent", "gamma effect"),
            Effect(names[3], uuids[3], "attack", "reaction", "delta effect"),
        ]
        entries = {uuids[ii]:effects[ii] for ii in range(4)}
        self.assertTrue(self.library.AddToDict('effects', entries))

        # Retrieve and check effects dict
        print("Testing GetDict from Library\n")
        effects_dict = self.library.GetDict('effects')
        print("Original entries\n")
        pprint(entries)
        print("\nRetrieved entries\n")
        pprint(effects_dict)
        self.assertTrue( len(effects_dict.keys()) == len(entries.keys()) ) # make sure the dict is the same size
        for id, eff in effects_dict.items(): # make sure each item we added is accounted for    
            self.assertTrue(id in entries.keys()) # make sure the key is in the dict
            self.assertTrue(eff in entries.values()) # make sure the Effect object is in the dict

        # Retrieve and check names
        print("Testing GetNames from Library\n")
        effect_names = self.library.GetNames('effects')
        print("Original Effect Names <{}>".format(names))
        print("Retrieved Effect Names <{}>\n".format(effect_names))
        self.assertTrue( len(names) == len(effect_names) ) # make sure the dict is the same size
        for name in names: # make sure all names match
            self.assertTrue(name in effect_names)

        # Retrieve and check uuids
        print("Testing GetUUIDs from Library\n")
        effect_uuids = self.library.GetUUIDs('effects')
        print("Original UUIDs \n<{}>\n".format(uuids))
        print("Retrieved UUIDs \n<{}>\n".format(effect_uuids))
        self.assertTrue( len(uuids) == len(effect_uuids) ) # make sure the dict is the same size
        for id in uuids: # make sure all names match
            self.assertTrue(id in effect_uuids)

        # Make sure getting uuid from name works
        print("Testing GetUUIDFromName in Library\n")
        for name in effect_names:
            uuid_from_name = self.library.GetUUIDFromName('effects', name) # get uuid from name
            effect_from_uuid = self.library.Get('effects', uuid_from_name) # get Effect instance using uuid
            name_from_effect = effect_from_uuid.GetName() # get name from the Effect instance
            self.assertTrue(name is name_from_effect) # make sure the names are the same

        # Make sure the get name uuid dict is valid
        print("Testing GetNameUUIDAsDict in Library\n")
        name_uuid_dict = self.library.GetNameUUIDAsDict('effects')
        for name, id in name_uuid_dict.items():
            effect_from_uuid = self.library.Get('effects', id)
            self.assertTrue(name is effect_from_uuid.GetName())


if __name__=="__main__":
    unittest.main()