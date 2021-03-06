from Effect import Effect

class Feature(object):
    def __init__(self, name, this_uuid, description, effects, prereq_features, unlock_level = None):
        self._uuid = this_uuid # uuid
        self._name = name # string 
        self._description = description # string
        self._effects = effects # name strings only
        self._prereq_features = prereq_features # list of name strings
        self._unlock_level = unlock_level # uint

    def GetDict(self):
        return self.__str__()

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
        Returns T/F if this feature would be unlocked givem level + known features
        """
        if level < self._unlock_level:
            return False

        if not all(self._prereq_features in already_learned_features):
            return False

        return True
        
    def __str__(self):
        """
        Puts all instance members into a dict and returns it 
        """
        return {
            'uuid' : str(self._uuid),
            'name' : self._name,
            'description' : self._description,
            'effects' : self._effects,
            'prereq_features' : self._prereq_features,
            'unlock_level' : self._unlock_level
        }