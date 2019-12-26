from Feature import Feature
from Option import Option
from Effect import Effect
from Item import Item

class Library(object):
    def __init__(self, dicts = {}):
        """
        Parameter:
            dicts (name string, dict): all dictionaries held in this library. The keys for all the individual
                                        dict objects should be UUIDs, and the values can be anything.
                                        The keys of the dicts object (highest level) should be name strings
        """
        self._dicts = dicts # dict of dicts
    
    def GetDict(self, dict_name):
        try:
            return self._dicts[dict_name.lower()]
        except KeyError:
            return {}

    def AddDict(self, name, new_dict):
        if name in self._dicts:
            print("Can't add new dict with name <{}> because it already exists in library".format(name))
            return False
        
        self._dicts[name] = new_dict

    def Get(self, dict_name, this_uuid):
        try:
            return self.GetDict(dict_name)[this_uuid]
        except KeyError:
            print("Key <{}> not found in dict <{}>".format(this_uuid, dict_name))
            return None

    def Peek(self, dict_name, this_uuid):
        return (this_uuid in self.GetDict(dict_name))

    def GetUUIDFromName(self, dict_name, name):
        try:
            name_dict = self.GetNameUUIDAsDict(dict_name)
            return name_dict[name]
        except:
            print("Either the name <{}> or dict_name <{}> was not in library".format(name, dict_name))
            return None

    def GetUUIDs(self, dict_name):
        return [this_uuid for this_uuid in self.GetDict(dict_name)]
    
    def GetNames(self, dict_name):
        this_dict = self.GetDict(dict_name)
        return [this_dict[this_uuid].GetName() for this_uuid in this_dict]

    def GetNameUUIDAsDict(self, dict_name):
        this_dict = self.GetDict(dict_name)
        return {this_dict[this_uuid].GetName():this_uuid for this_uuid in this_dict}