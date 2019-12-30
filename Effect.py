from copy import deepcopy

class Effect(object):
    def __init__(self, name, this_uuid, effect_type, duration, description):
        self._uuid = this_uuid # uuid
        self._name = name # string
        self._effect_type = effect_type # string
        self._duration = duration # string
        self._description = description # string

    def GetDict(self):
        return self.__str__()

    def GetUUID(self):
        return self._uuid

    def GetName(self):
        return self._name

    def GetType(self):
        return self._effect_type

    def GetDuration(self):
        return self._duration

    def GetDescription(self):
        return self._description

    def __str__(self):
        """
        Puts all instance members into a dict and returns it 
        """
        return {
            "name" : self._name,
            "uuid" : str(self._uuid)
            "effect_type": self._effect_type,
            "duration": self._duration,
            "description": self._description
        }
