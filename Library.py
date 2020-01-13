from Feature import Feature
from Option import Option
from Effect import Effect
from Item import Item

class Library(object):
    def __init__(self, dicts = {}):
        """
        Args:
            dicts: [name string, dict] all dictionaries held in this library. The keys for all the individual
                                        dict objects should be UUIDs, and the values can be anything.
                                        The keys of the dicts object (highest level) should be name strings
        """
        self._dicts = dicts # dict of dicts

    def AddToDict(self, dict_name, entries):
        """
        Add new entries to a dict in the library

        Parameters:
            dict_name (string): must be a valid dict name
            entries (dict of uuid:object): new key/value pairs to add to specified dictionary. Validity
                of values must be ensured by caller 
        """
        if not (dict_name in self._dicts):
            print("Can't add new entries to dict <{}> because it isn't in the library".format(dict_name))
            return False

        self._dicts[dict_name].update(entries)
        return True

    def SetValidDicts(self, names):
        """
        This will delete any items in the library, and create empty dicts with the specified names
        """
        self._dicts.clear()
        
        for name in names:
            self._dicts[name] = {}
        
    def AddNewValidDict(self, name):
        if name in self._dicts.keys():
            print("Can't add new dict <{}> to library, already exists".format(name))
            return False

        self._dicts[name] = {}

    def Peek(self, dict_name, this_uuid):
        """
        Returns true if dict_name exists and this_uuid exists in that dict
        """
        return (this_uuid in self.GetDict(dict_name))

    def Get(self, dict_name, this_uuid):
        try:
            return self.GetDict(dict_name)[this_uuid]
        except KeyError:
            print("Key <{}> not found in dict <{}>".format(this_uuid, dict_name))
            return None

    def GetValidDicts(self):
        return self._dicts.keys()

    def GetDict(self, dict_name):
        """
        Always returns a dict, empty dict if dict_name is invalid
        """
        try:
            return self._dicts[dict_name.lower()]
        except KeyError:
            return {}

    def GetUUIDFromName(self, dict_name, name):
        """
        Return the UUID of an object given dict_name and object_name (reverse lookup)
        """
        try:
            name_dict = self.GetNameUUIDAsDict(dict_name)
            return name_dict[name]
        except:
            print("Either the name <{}> or dict_name <{}> was not in library".format(name, dict_name))
            return None

    def GetUUIDs(self, dict_name):
        return self.GetDict(dict_name).keys()
    
    def GetNames(self, dict_name):
        this_dict = self.GetDict(dict_name)
        return [this_dict[this_uuid].GetName() for this_uuid in this_dict]

    def GetNameUUIDAsDict(self, dict_name):
        """
        Returns a dict with [name:uuid] entries of the specified dict 
        """
        this_dict = self.GetDict(dict_name)
        return {this_dict[this_uuid].GetName():this_uuid for this_uuid in this_dict}