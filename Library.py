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

    def AddToDict(self, dict_name, entries, mode = 'normal'):
        """Add new entries to a dict in the library
        
        Arguments:
            dict_name {string} -- must be a valid dict name
            entries {dict of uuid:object} -- new key/value pairs to add to specified dictionary. Validity of values must be ensured by caller
        
        Returns:
            bool -- Depends on Mode: 'normal' mode adds all non duplicate entries (of existing keys), true if no exceptions are thrown
                                     'overwrite' mode adds all entries, overwriting any already existing keys, true if no exceptions are thrown
                                     'safe' mode only updates if all entries are non duplicate of existing keys, true if entries added
        """        
        if not (dict_name in self._dicts):
            print("Can't add new entries to dict <{}> because it isn't in the library".format(dict_name))
            return False

        # If mode is overwrite, don't worry about existing keys, just overwrite them with the new entries
        if mode == 'overwrite':
            try:
                self._dicts[dict_name].update(entries)
                return True
            except Exception as e:
                print("Caught exception while tried to update dict <{}> with entries <{}>, got <{}>".format(dict_name, entries, e))
                return False

        # If mode is normal, go through each key and make sure every key it's new before making a decision
        elif mode == 'normal':
            try:
                entries_to_add = {}
                for key in entries:
                    if key in self._dicts[dict_name]:
                        print("Got existing key in AddToDict <{}>, will skip".format(key))
                        continue
                    else:
                        entries_to_add[key] = entries[key]
                self._dicts[dict_name].update(entries_to_add) # add only the vetted entries
                return True
            except Exception as e:
                print("Caught exception while tried to update dict <{}> with entries <{}>, got <{}>".format(dict_name, entries, e))
                return False
            
        # If mode is safe, then every entry is new, or reject all of them
        elif mode == 'safe':
            try:
                for key in entries:
                    if key in self._dicts[dict_name]:
                        print("Got duplicate key in AddToDict with mode set to safe <{}>".format(key))
                        return False
                self._dicts[dict_name].update(entries) # all entries were good, add em
            except Exception as e:
                print("Caught exception while tried to update dict <{}> with entries <{}>, got <{}>".format(dict_name, entries, e))
                return False

        else:
            print("Got invalid mode <{}> in AddToDict".format(mode))
            return False

    def SetValidDicts(self, names):
        """This will delete any items in the library, and create empty dicts with the specified names
        
        Arguments:
            names {list of string} -- names of all dicts which will be valid in this dict library

        Returns:
            bool -- True if successfully updated, false otherwise
        """
        try:
            new_dicts = {}
            for name in names:
                new_dicts[name] = {}
        except Exception as e:
            print("Caught exception while trying to set new valid dicts <{}> for library, got <{}>".format(names, e))
            return False

        self._dicts.clear()
        self._dicts = new_dicts
        return True
        
    def AddNewValidDict(self, name):
        """Adds a new dict name to the allowed dicts in the library
        
        Arguments:
            name {string} -- name of the new dict
        
        Returns:
            bool -- True if name already exists or successfully added, false otherwise
        """
        if name in self._dicts.keys():
            print("Can't add new dict <{}> to library, already exists".format(name))
            return True

        try:
            self._dicts[name] = {}
            return True
        except ValueError as e:
            print("Failed to add new valid dict with name <{}>, got <{}>".format(name, e))
            return False

    def IsInDict(self, dict_name, this_uuid):
        """
        Returns true if dict_name exists and this_uuid exists in that dict
        """
        return (this_uuid in self.GetDict(dict_name))

    def Get(self, dict_name, this_uuid):
        """Retrieves the specified object from the library
        
        Arguments:
            dict_name {string} -- name of the dictionary to look into
            this_uuid {uuid} -- uuid of the object to retrieve
        
        Returns:
            Object or None -- object if found, None if not
        """
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