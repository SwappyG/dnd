class Feature(object):
    def __init__(self, name, this_uuid, description, effects=None, prereq_features=None, unlock_level=0):
        self._uuid = this_uuid  # uuid
        self._name = name  # string
        self._description = description  # string
        self._effects = [] if effects is None else effects  # list of effect uuids
        self._prereq_features = [] if prereq_features is None else prereq_features  # list of feature uuids
        self._unlock_level = unlock_level  # uint

    def GetDict(self):
        return self.__str__

    def GetUUID(self):
        return self._uuid

    def GetName(self):
        return self._name

    def GetDescription(self):
        return self._description

    def GetEffects(self):
        return self._effects

    def GetPrereqFeatures(self):
        return self._prereq_features

    def GetUnlockLevel(self):
        return self._unlock_level

    def IsUnlocked(self, level, already_learned_features):
        """
        Returns T/F if this feature would be unlocked given level + known features
        
        Parameters
            level {unsigned int} -- current level of character
            already_learned_features {list of uuid} -- all features the character knows already
        """
        if level < self._unlock_level:
            return False

        return set(self._prereq_features).issubset(already_learned_features)

    def AsDict(self):
        """
        Puts all instance members into a dict and returns it 
        """
        return {
            'uuid': str(self._uuid),
            'name': self._name,
            'description': self._description,
            'effects': self._effects,
            'prereq_features': self._prereq_features,
            'unlock_level': self._unlock_level
        }
