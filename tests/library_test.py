from Library import Library
import uuid
import unittest
from collections import Counter
from pprint import pprint

class LibraryTests(unittest.TestCase):

    def setUp(self):
        self.library = Library()

    def test_ValidDicts(self):
        valid_library_dicts = ['features', 'effects', 'options', 'jobs']
        
        # Check that Set and Get ValidDict work
        self.library.SetValidDicts(valid_library_dicts)
        self.assertTrue(Counter(valid_library_dicts) == Counter(self.library.GetValidDicts()))
        self.assertFalse(self.library.AddToDict('not_valid_dict', {uuid.uuid4():[], uuid.uuid4():[]}))

        # Add a new dict, check that old list doesn't match new list
        self.library.AddNewValidDict("fancy")
        self.assertFalse(Counter(valid_library_dicts) == Counter(self.library.GetValidDicts()))
        self.assertTrue(Counter(valid_library_dicts + ['fancy']) == Counter(self.library.GetValidDicts()))

        # Make sure adding to valid dict works
        self.assertTrue(self.library.AddToDict('fancy', {uuid.uuid4():[], uuid.uuid4():[]}))
        self.assertTrue(self.library.AddToDict('features', {uuid.uuid4():[]}))
        self.assertTrue(self.library.AddToDict('effects', {uuid.uuid4():[], uuid.uuid4():[], uuid.uuid4():[]}))
        self.assertTrue(self.library.AddToDict('effects', {}))

    def test_AddPeekGetDict(self):
        pass

    def test_GetNameUUID(self):
        pass

if __name__=="__main__":
    unittest.main()