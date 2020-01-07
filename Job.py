from Feature import Feature
from Option import Option
from pprint import pprint

class Job(object):
    def __init__(self, name, this_uuid, description, features, options):
        self._uuid = this_uuid # uuid
        self._name = name # string
        self._description = description # string
        self._features = features # uuids only
        self._options = options # uuids only 

    def GetDict(self):
        return self.__str__()

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

    def __str__(self):
        """
        Puts all instance members into a dict and returns it 
        """
        return {
            'uuid' : self._uuid,
            'name' : self._name,
            'description' : self._description,
            'features' : self._features,
            'options' : self._options
        }
        