from copy import deepcopy

class Effect(object):
    def __init__(self, name, this_uuid, effect_type, duration, description):
        self._uuid = this_uuid
        self._name = name
        self._effect_type = effect_type
        self._duration = duration
        self._description = description

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
        return {
            "name" : self._name,
            "effect_type": self._effect_type,
            "duration": self._duration,
            "description": self._description
        }
