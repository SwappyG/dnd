from Feature import Feature
from Option import Option
from pprint import pprint

class Job(object):
    def __init__(self, name, this_uuid, description, features, options):
        self._uuid = this_uuid
        self._name = name
        self._description = description
        self._features = features # uuids only
        self._options = options # uuids only 

    def GetDict(self):
        job_dict = {}
        job_dict['uuid'] = self._uuid
        job_dict['name'] = self._name
        job_dict['description'] = self._description
        job_dict['features'] = self._features
        job_dict['options'] = self._options
        return job_dict

    def GetUUID(self):
        return self._uuid

    def GetName(self):
        return self._name
    
    def GetDescription(self):
        return self._description

    def GetAllOptions(self):
        return self._options

    def GetAllFeatures(self):
        return self._features

    def GetUnlockedFeatures(self, library, level):
        return [name for name in self._features if (level == library.Get("features", name).GetUnlockLevel())]

    def GetUnlockedOptions(self, library, level, already_selected_features):
        unlocked_options = {}
        for option_uuid in self._options:
            this_option = library.Get('options', option_uuid)
            if (this_option == None):
                print("Failed to get an option out of the library with uuid <{}>".format(option_uuid))
                continue

            this_option_features = this_option.GetOptions(level, already_selected_features)
            if (this_option_features != None):
                unlocked_options[option_uuid] = this_option_features
            
        return unlocked_options